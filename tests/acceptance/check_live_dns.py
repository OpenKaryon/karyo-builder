#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise a native profile DEB in owned DNS namespaces on disposable QA VMs.

This is staged-package acceptance, not an installed graphical-session test.
The account is an explicit model; no local account or external VPN is created.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
from types import SimpleNamespace


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', type=Path, required=True)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--version', default='0.1.1-1',
                        help='Exact expected native package version')
    parser.add_argument('--installed', action='store_true',
                        help='Require matching installed payloads and execute them')
    args = parser.parse_args()
    if (os.geteuid() != 0 or socket.gethostname() not in
            {'karyo-de-acceptance', 'karyo-de-ubuntu-acceptance'}):
        raise SystemExit('Use an explicitly disposable migration QA guest as root')
    if hashlib.sha256(args.package.read_bytes()).hexdigest() != args.sha256:
        raise SystemExit('The supplied native DEB identity changed')
    metadata = subprocess.check_output(['dpkg-deb', '-f', str(args.package),
        'Package', 'Version', 'Architecture'], text=True)
    expected = ('Package: karyo-profile-accounts\nVersion: ' + args.version +
                '\nArchitecture: amd64\n')
    if metadata != expected:
        raise SystemExit('Expected the specified native profile accounts package')
    work = Path(tempfile.mkdtemp(prefix='karyo-live-dns-qa-', dir='/root'))
    stage = work / 'stage'
    subprocess.run(['dpkg-deb', '-x', str(args.package), str(stage)], check=True)
    if args.installed:
        installed = subprocess.check_output(['dpkg-query', '-W', '-f=${Version}',
            'karyo-profile-accounts'], text=True)
        if installed != args.version:
            raise SystemExit('The expected profile package is not installed')
        for item in stage.rglob('*'):
            if item.is_file():
                if item.read_bytes() != (Path('/') / item.relative_to(stage)).read_bytes():
                    raise SystemExit('Installed profile payload differs from the native DEB')
    sys.dont_write_bytecode = True
    sys.path.insert(0, '/usr/libexec/karyo/profiles' if args.installed
                    else str(stage / 'usr/libexec/karyo/profiles'))

    from karyo_profiles.credentials import LocalAccount
    from karyo_profiles.dns import DNSSeed, discover_dns
    from karyo_profiles.dns_refresh import PrivateLink, refresh_dns
    from karyo_profiles.journal import RuntimeJournal
    from karyo_profiles.journal_dns import JournalDNS, file_receipt, unit_receipt
    from karyo_profiles.journal_network import JournalNetwork, receipt, restore_network
    from karyo_profiles.logind import Session
    from karyo_profiles.networks import NetworkCommand, NetworkSpec, ProfileNetwork
    from karyo_profiles.storage import ConfigStore
    from karyo_profiles.underlay import discover_underlay

    command = NetworkCommand()
    resolver = Path('/etc/resolv.conf')
    original_dns = hashlib.sha256(resolver.read_bytes()).hexdigest()
    original_namespaces = command.run('/usr/sbin/ip', 'netns', 'list')
    account = LocalAccount('qa-dns-model', 12011, 1001, '/nonexistent', '/bin/sh')
    if any(line.split(':')[2] == str(account.uid)
           for line in Path('/etc/passwd').read_text().splitlines()):
        raise SystemExit('The explicitly modelled QA UID is already assigned')
    accounts = SimpleNamespace(by_uid=lambda uid: account)
    source = Session('c9999', 'qa-home-model', 1001, 8, True)
    store = ConfigStore(configuration=work/'configuration', legacy=work/'legacy',
                        runtime=work/'runtime')
    report = {'passed': False, 'package_sha256': args.sha256,
        'staged_native_DEB': not args.installed, 'installed_runtime': args.installed,
        'installed_files_modified': False,
        'account_is_model': True, 'client_workload': 'native sleep process',
        'external_VPN_client_tested': False, 'work': str(work)}
    journal = RuntimeJournal(work/'journal')
    network = dns = wrapped = client = None
    tunnel_index = None
    try:
        with store.locked():
            physical = discover_underlay(command)
            seed = discover_dns(physical, command)
            token = journal.begin(account, source)
            network = ProfileNetwork(store, NetworkSpec(account.uid, token), command).create()
            record = journal.record(token)
            journal.change(record, dict(record, pending=None, network=receipt(network)))
            wrapped = JournalNetwork(journal, network)
            dns = JournalDNS.start(journal, wrapped, seed, accounts=accounts)

            def identities():
                return {'files': file_receipt(dns.files),
                    'bus': unit_receipt(dns.files, 'bus', dns.services.bus),
                    'resolver': unit_receipt(dns.files, 'resolver', dns.services.resolver)}

            initial = identities()
            network.contents = 'tunnel'
            record = journal.record(token)
            journal.change(record, dict(record, network=receipt(network)))
            command.run('/usr/sbin/ip', '-n', network.name, 'link', 'add',
                        'qa-vpn0', 'type', 'wireguard')
            tunnel_index = network._inventory(inside=True)['qa-vpn0']['ifindex']
            command.run('/usr/sbin/ip', '-n', network.name, 'link', 'set', 'qa-vpn0', 'up')
            prefix = ('/usr/bin/busctl', '--address=' + dns.files.plan.bus_address,
                      '--json=short', '--timeout=2s')
            path = json.loads(command.run(*prefix, 'call', 'org.freedesktop.resolve1',
                '/org/freedesktop/resolve1', 'org.freedesktop.resolve1.Manager',
                'GetLink', 'i', str(tunnel_index)))['data'][0]
            command.run(*prefix, 'call', 'org.freedesktop.resolve1', path,
                'org.freedesktop.resolve1.Link', 'SetDNS', 'a(iay)', '1', '2', '4',
                '10', '200', '0', '53')
            command.run(*prefix, 'call', 'org.freedesktop.resolve1', path,
                'org.freedesktop.resolve1.Link', 'SetDomains', 'a(sb)', '1',
                'qa-vpn.example', 'true')

            def tunnel_dns():
                return [command.run(*prefix, 'get-property', 'org.freedesktop.resolve1',
                    path, 'org.freedesktop.resolve1.Link', name) for name in ('DNS', 'Domains')]

            tunnel_before = tunnel_dns()
            client = subprocess.Popen(['/usr/sbin/ip', 'netns', 'exec', network.name,
                '/usr/bin/sleep', '30'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            target = DNSSeed(physical, ('198.51.100.53',), ('qa.example',))
            assert client.poll() is None
            assert refresh_dns(dns, target)
            link = PrivateLink(dns)
            assert link.read('DNS') == [[2, [198, 51, 100, 53]]]
            assert link.read('Domains') == [['qa.example', False]]
            assert tunnel_dns() == tunnel_before and client.poll() is None
            assert identities() == initial and journal.snapshot()['schema'] == 8

            dns.release_handles()
            dns = None
            os.close(network.fd)
            network.fd = None
            journal.close()
            journal = RuntimeJournal(work/'journal')
            network = restore_network(store, journal.record(token), require_empty=False)
            wrapped = JournalNetwork(journal, network)
            dns = JournalDNS.restore_observers(journal, wrapped, accounts=accounts)
            assert dns.files.plan.seed == target
            assert refresh_dns(dns, seed)
            assert tunnel_dns() == tunnel_before and client.poll() is None
            assert identities() == initial
            report.update(passed=True, real_private_bus=True,
                actual_tunnel_DNS_preserved=True, live_consumer_preserved=True,
                private_service_PIDs_and_inodes_preserved=True,
                journal8_reopen=True, restored_original_seed=True)
    except Exception as error:
        report['error'] = type(error).__name__ + ': ' + str(error)
    finally:
        try:
            with store.locked():
                if client is not None:
                    if client.poll() is None:
                        client.terminate()
                    client.wait(timeout=5)
                if tunnel_index is not None and network is not None:
                    current = network._inventory(inside=True).get('qa-vpn0')
                    assert current and current['ifindex'] == tunnel_index
                    command.run('/usr/sbin/ip', '-n', network.name, 'link', 'delete', 'qa-vpn0')
                if dns is not None:
                    dns.close()
                    dns.release_handles()
                if wrapped is not None and network is not None:
                    wrapped.close()
                if network is not None and network.fd is not None:
                    os.close(network.fd)
                    network.fd = None
        except Exception as error:
            report.update(passed=False, cleanup_error=type(error).__name__ + ': ' + str(error))
        journal.close()
        report['host_resolver_preserved'] = hashlib.sha256(resolver.read_bytes()).hexdigest() == original_dns
        report['original_namespaces_preserved'] = command.run('/usr/sbin/ip', 'netns', 'list') == original_namespaces
        report['passed'] = (report['passed'] and report['host_resolver_preserved']
                            and report['original_namespaces_preserved'])
        (work/'result.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())

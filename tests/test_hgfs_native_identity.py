# SPDX-License-Identifier: GPL-3.0-or-later
"""Never count a foreign-base package as native HGFS acceptance."""
import copy
import importlib.util
from pathlib import Path
import unittest
import subprocess

spec=importlib.util.spec_from_file_location('hgfs_gate',Path(__file__).with_name('acceptance')/'check-vmware-shared-folders.py')
gate=importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class NativeHgfsIdentity(unittest.TestCase):
    def test_target_identity_and_success_must_match_before_guest_operations(self):
        package={'status':'success','recipe':{'resolved':{'package':{'name':'karyo-vmware-shared-folders','architecture':'amd64'}}},
                 'validation':{'ctest':'passed','dpkg_deb':'passed'},
                 'environment':{'distribution':{'ID':'debian','VERSION_ID':'13','VERSION_CODENAME':'trixie'}}}
        gate.validate_native_package(package,'debian')
        with self.assertRaises(ValueError):gate.validate_native_package(package,'ubuntu')
        for section,key,value in [('validation','ctest','failed'),('validation','dpkg_deb','failed'),
                                  ('environment','distribution',{'ID':'debian','VERSION_ID':'12','VERSION_CODENAME':'bookworm'})]:
            changed=copy.deepcopy(package);changed[section][key]=value
            with self.subTest(section=section,key=key), self.assertRaises(ValueError):
                gate.validate_native_package(changed,'debian')
        changed=copy.deepcopy(package);changed['recipe']['resolved']['package']['name']='unrelated'
        with self.assertRaises(ValueError):gate.validate_native_package(changed,'debian')

    def test_failed_share_cleanup_still_disables_and_restores_runtime(self):
        for failure in ('timeout','exit'):
            calls=[]
            def vix(*args,**kwargs):
                calls.append(args)
                if args[0]=='removeSharedFolder':
                    if failure=='timeout':raise subprocess.TimeoutExpired('removeSharedFolder',1)
                    return subprocess.CompletedProcess(args,1,stdout='')
                return subprocess.CompletedProcess(args,0,stdout='TRUE\n')
            result=gate.restore_host(vix,'qa.vmx','dummy',True,True,True)
            self.assertTrue(result['runtime_restored'])
            self.assertTrue(result['errors'])
            self.assertEqual([row[0] for row in calls],['removeSharedFolder','disableSharedFolders','writeVariable','readVariable'])

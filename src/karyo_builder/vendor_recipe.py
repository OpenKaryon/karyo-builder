# SPDX-License-Identifier: GPL-3.0-or-later
"""Capture checksummed vendor data; no upstream control script enters output."""
import hashlib
import json
import os
from pathlib import Path
import re
import stat

from .recipe import fields, text, validate_package

MAX_INPUT = 512 * 1024 * 1024


def payload_path(value, package=None):
    text(value, 'payload path')
    if (len(value) > 512 or re.fullmatch(r'[A-Za-z0-9_+./-]+', value) is None
            or any(p in {'', '.', '..'} for p in value.split('/'))):
        raise ValueError('Payload files need canonical relative Linux paths')
    roots = ('usr/bin/', 'usr/libexec/', 'usr/share/pixmaps/', 'usr/share/icons/hicolor/')
    if package is not None:
        roots = ('usr/share/doc/' + package + '/',)
    if not value.startswith(roots):
        raise ValueError('Vendor payload must contain explicit binaries, icons or package licenses only')
    return value


def unique(pairs):
    value = {}
    for key, item in pairs:
        if key in value: raise ValueError('Duplicate vendor recipe field: ' + key)
        value[key] = item
    return value


def validate_recipe(recipe):
    fields(recipe, ('schema', 'package', 'inputs', 'licenses', 'source_date_epoch'), 'vendor recipe')
    if type(recipe['schema']) is not int or recipe['schema'] != 1:
        raise ValueError('Only vendor recipe schema 1 is supported')
    validate_package(recipe['package'], allow_scripts=False, relationships=('provides', 'conflicts'))
    if type(recipe['source_date_epoch']) is not int or not 0 <= recipe['source_date_epoch'] <= 253402300799:
        raise ValueError('A supported non-negative source epoch is required')
    for key in ('inputs', 'licenses'):
        if not isinstance(recipe[key], list) or not 1 <= len(recipe[key]) <= 16:
            raise ValueError('Vendor ' + key + ' needs one to sixteen explicit inputs')
    selected = set()
    for item in recipe['inputs']:
        fields(item, ('path', 'sha256', 'package', 'version', 'architecture', 'files'), 'vendor input')
        for key in ('path', 'package', 'version', 'architecture'): text(item[key], 'vendor input ' + key)
        if item['architecture'] != 'amd64' or not re.fullmatch(r'[a-z0-9][a-z0-9+.-]+', item['package']):
            raise ValueError('Vendor inputs must name amd64 Debian packages')
        if not isinstance(item['files'], list) or not 1 <= len(item['files']) <= 256:
            raise ValueError('Select a bounded non-empty list of exact vendor files')
        for path in item['files']:
            payload_path(path)
            if path in selected: raise ValueError('Duplicate vendor destination: ' + path)
            selected.add(path)
    for item in recipe['licenses']:
        fields(item, ('path', 'sha256', 'destination'), 'license input')
        payload_path(item['destination'], recipe['package']['name'])
        if item['destination'] in selected: raise ValueError('Duplicate license destination')
        selected.add(item['destination'])
    for item in [*recipe['inputs'], *recipe['licenses']]:
        text(item['path'], 'input path')
        if not isinstance(item['sha256'], str) or not re.fullmatch(r'[a-f0-9]{64}', item['sha256']):
            raise ValueError('Every input requires a lowercase SHA256')


def capture_file(source, target, expected, *, limit=MAX_INPUT):
    source = Path(source).absolute()
    if any(p.is_symlink() or getattr(p, 'is_junction', lambda: False)() for p in (source, *source.parents)):
        raise ValueError('Vendor input paths must not traverse symlinks or junctions')
    info = source.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or not 0 < info.st_size <= limit:
        raise ValueError('Vendor input must be a bounded single-link regular file')
    with source.open('rb') as reader, target.open('xb') as writer:
        opened = os.fstat(reader.fileno())
        if (opened.st_dev, opened.st_ino, opened.st_size) != (info.st_dev, info.st_ino, info.st_size):
            raise ValueError('Vendor input changed during capture')
        remaining = info.st_size
        while remaining:
            block = reader.read(min(1024 * 1024, remaining))
            if not block: raise ValueError('Vendor input was truncated during capture')
            writer.write(block); remaining -= len(block)
        if reader.read(1): raise ValueError('Vendor input grew during capture')
    if target.stat().st_size != info.st_size:
        raise ValueError('Vendor input changed size during capture')
    with target.open('rb') as stream: actual = hashlib.file_digest(stream, 'sha256').hexdigest()
    if actual != expected: raise ValueError('Vendor input SHA256 mismatch')
    return {'file': target.name, 'sha256': actual, 'bytes': info.st_size}


def capture_recipe(path, destination):
    path = Path(path).resolve(strict=True); raw = path.read_bytes()
    recipe = json.loads(raw.decode('utf-8'), object_pairs_hook=unique); validate_recipe(recipe)
    destination = Path(destination); destination.mkdir()
    records = []
    for key in ('inputs', 'licenses'):
        values = []
        for number, item in enumerate(recipe[key]):
            filename = key + '-' + str(number) + ('.deb' if key == 'inputs' else '.txt')
            record = capture_file(path.parent/item['path'], destination/filename, item['sha256'], limit=MAX_INPUT if key == 'inputs' else 8*1024*1024)
            values.append(dict(item, path='/input/'+filename)); records.append(dict(record, role=key, index=number))
        recipe[key] = values
    (destination/'original-recipe.json').write_bytes(raw)
    (destination/'vendor-recipe.json').write_bytes((json.dumps(recipe, indent=2)+'\n').encode())
    return recipe, records, hashlib.sha256(raw).hexdigest()

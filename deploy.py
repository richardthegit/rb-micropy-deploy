#!/usr/bin/env python3
from os import listdir, makedirs
from os.path import abspath, dirname, exists, isdir, join
from shutil import copy, copytree, rmtree

from shared import *


def find_source(root_dir):
    """
    Return a list of directories containing source code. This uses a specific pattern:

        root_dir/*/src
    """
    src_dirs = [join(root_dir, 'src')]
    lib_dir = join(root_dir, 'libs')

    for name in listdir(lib_dir):
        path = join(lib_dir, name, 'src')
        if exists(path):
            src_dirs.append(path)

    return src_dirs


def copy_files(root_dir, dev):
    """
    Copy all files (including any store.json already on the device) into 'build' then 
    rsync that to the device.
    """
    if exists(build_dir):
        err(f'Build directory already exists; delete it manually and retry: {build_dir}')

    info(f'Collecting source to: {build_dir}')
    makedirs(build_dir)

    try:
        src_dirs = find_source(root_dir)
        if len(src_dirs) == 0:
            err('No source directories found')

        info('Source directories found:')
        for d in src_dirs:
            print(f'  {d}')
            copytree(d, build_dir, dirs_exist_ok = True)

        rshell(dev, ['cp', '/pyboard/store.json', build_dir])
        if exists(join(build_dir, 'store.json')):
            info('Existing store file preserved')
        else:
            warn('No store file on device')

        rshell(dev, ['rsync', '-m', build_dir, '/pyboard/'])

    finally:
        info('Deleting build directory')
        rmtree(build_dir)


if __name__ == '__main__':
    parser = std_args()
    parser.add_argument('root_dir', help = 'Root directory')
    args = parser.parse_args()

    copy_files(args.root_dir, args.dev)

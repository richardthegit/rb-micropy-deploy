from os.path import abspath, dirname, exists, join
from subprocess import run
import argparse, sys


repo_dir = dirname(abspath(__file__))
build_dir = join(repo_dir, 'build')
venv_dir = join(repo_dir, 'venv')
python_binary = join(venv_dir, 'bin/python')
rshell_binary = join(venv_dir, 'bin/rshell')
requirements_file = join(repo_dir, 'requirements.txt')

# Text style control codes.
RED = '\033[91m'
GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
END = '\033[0m'

def ok(msg):
    print(f'{GREEN}{msg}{END}')

def info(msg):
    print(f'{CYAN}{msg}{END}')

def warn(msg):
    print(f'{YELLOW}{msg}{END}')

def err(msg, status = 1):
    """
    Print an error - this will also exit with 'status' unless status == None.
    """
    print(f'{RED}{msg}{END}')
    if status != None:
        exit(status)


def ensure_venv():
    if exists(rshell_binary):
        return

    err(f'rshell binary not found at: {rshell_binary}', None)
    ok(f'Creating virtualenv in: {venv_dir}')
    run([sys.executable, '-m', 'venv', venv_dir])
    run([python_binary, '-m', 'pip', 'install', '-r', requirements_file])

    if not exists(rshell_binary):
        err('Failed to create venv')


def rshell(dev, args):
    """
    Call rshell. 'dev' should be just the device name, '/dev/' will be prepended.
    """
    ensure_venv()

    args = [rshell_binary, '-p', f'/dev/{dev}'] + args
    info(f'Running rshell: {" ".join(args)}')
    return run(args)


def std_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dev', default = 'ttyACM0', help = "Connected device name - don't include /dev/")
    return parser

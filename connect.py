#!/usr/bin/env python3
from shared import std_args, rshell

args = std_args().parse_args()

rshell(args.dev, ['--editor', '/usr/bin/nano'])
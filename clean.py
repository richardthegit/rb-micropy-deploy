#!/usr/bin/env python3
from shared import *


args = std_args().parse_args()

# Copy just any existing store to the build dir, then rsync.
prepare_build(args.dev)
try:
    rsync_build(args.dev)
finally:
    purge_build()

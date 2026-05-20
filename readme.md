Micropython Deployment Tools
============================

This repo provides a script which simplifies deployment of source from a linux host to a connected microcontroller. The assumption is that a project repo contains multiple dependent repos in addition
to it's own source, and all use this naming convention:

    <repo name>/src/

When run, files from all *src* directories found using this naming scheme are copied to the device. For example, consider this filesystem, for a typical parent repo:

    src # Project sourcecode
        my_app.py

    libs
        rb-micropy-deploy # This repo - ignored (no 'src' subdirectory)
        rb-micropy-core   # Dependency
            src
                rb
                    core
                        file.py

When you run *libs/rb-micropy-deploy/deploy.py .*, the hierarchy copied to the device looks like this:

    my_app.py
    rb
        core
            file.py

# Setup

To access the device via USB, the user must be given access to the serial port; this is most easily done by adding the user to the `dialout` group:

    sudo usermod -a -G dialout $USER

Reboot for the changes to take effect.

# WARNING - rshell is weird!

rshell is used to copy files to and from the device. It uses a stupid path resolution which looks first on the device, then the host. So if you create a folder */pyboard/home*, a path which starts */home/* will always resolve to the device, meaning any attempt to copy files from the host inside */home/* (ie. your code!) will fail.

# Device Discovery

To see what devices are connected, use:

    sudo lsusb

# Waveshare ESP32-C3 Zero Setup

Download the generic ESP32-C3 firmware (links at the bottom of the page):

    https://micropython.org/download/ESP32_GENERIC_C3/

Boot the device into upgrade mode (hold down the boot button and reset). Install the image using esptool (included in the venv requirements.txt):

    esptool chip-id  # To test connection
    esptool erase-flash
    esptool write-flash 0 <firmware>

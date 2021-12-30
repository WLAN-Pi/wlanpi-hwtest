[![packagecloud-badge](https://img.shields.io/badge/deb-packagecloud.io-844fec.svg)](https://packagecloud.io/)

# wlanpi-hwtest

`hwtest` is a tool for the WLAN Pi Pro used to update VLI USB controller EEPROMs and run pytest to drive pass/fail testing.

## Example CLI usage

Optional arguments may be passed in to override default behaviors set in `/etc/wlanpi-hwtest/config.ini`. 

```bash
usage: hwtest [-h] [--debug] [-e] [--oled] [--firmware] [--verbose] [--version]

hwtest is a VLI USB Controller EEPROM updater and hardware testing tool for the WLAN Pi Pro.

optional arguments:
  -h, --help     show this help message and exit
  --debug        enable debug logging output
  -e, --emulate  enable keyboard emulation
  --oled         enable OLED and interactive (I/A) tests
  --firmware     enable VL805 firmware check
  --verbose      enable verbose printing of results to oled
  --version, -V  show program's version number and exit
```

## Contributors

See [AUTHORS](AUTHORS.md).

## Code of Conduct

See [CoC](CODE_OF_CONDUCT.md).

## OSS

Thank you to all the creators and maintainers of the following open source software used by `hwtest`:

* [dh-virtualenv](https://github.com/spotify/dh-virtualenv)
* [Font Awesome](https://fontawesome.com)
* [GPIO Zero](https://gpiozero.readthedocs.io/en/stable)
* [Luma.OLED](https://luma-oled.readthedocs.io/en/latest)
* [Pillow](https://python-pillow.org)
* [Pytest](https://pytest.org)
* [Python](https://www.python.org)
* [RPi.GPIO](https://pypi.org/project/RPi.GPIO)
* [rpi-eeprom](https://github.com/raspberrypi/rpi-eeprom)

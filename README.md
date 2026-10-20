[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](LICENSE) [![Tests](https://github.com/WLAN-Pi/wlanpi-hwtest/actions/workflows/python-tests.yml/badge.svg)](https://github.com/WLAN-Pi/wlanpi-hwtest/actions/workflows/python-tests.yml) [![packagecloud](https://img.shields.io/badge/deb-packagecloud.io-844fec.svg)](https://packagecloud.io/wlanpi)

# wlanpi-hwtest

`hwtest` is a tool for the WLAN Pi project used to update VLI USB controller EEPROMs and run pytest to drive pass/fail testing.

The tests run on WLAN Pi Pro hardware with Debian Trixie. Installing the package doesn't enable or start `wlanpi-hwtest.service`. To run the suite at boot, enable the service:

```bash
sudo systemctl enable wlanpi-hwtest
```

## Example CLI Usage

Optional arguments may be passed in to override default behaviors set in `/etc/wlanpi-hwtest/config.ini`.

```text
usage: hwtest [-h] [--debug] [-e] [--oled] [--firmware] [--waveshare]
              [--buttonsmash] [--verbose] [--version]

hwtest is a VLI USB Controller EEPROM updater and hardware testing tool for the WLAN Pi Pro.

options:
  -h, --help     show this help message and exit
  --debug        enable debug logging output
  -e, --emulate  enable keyboard emulation
  --oled         enable OLED and interactive (I/A) tests
  --firmware     enable VL805 firmware check
  --waveshare    enable waveshare LCD
  --buttonsmash  enable buttonsmash mode and print button presses to CLI
  --verbose      enable verbose printing of results to oled
  --version, -V  show program's version number and exit
```

`--firmware` checks the VL805 USB controller EEPROM. If the check fails, it writes new firmware and reboots the WLAN Pi.

## Buttonsmash Mode

FPMS and `hwtest` share the display and buttons, so stop FPMS first:

```bash
sudo apt update
sudo apt install wlanpi-hwtest
sudo systemctl stop wlanpi-fpms
sudo hwtest --buttonsmash --oled
```

To return to the FPMS menu, press Ctrl-C and start FPMS again:

```bash
sudo systemctl start wlanpi-fpms
```

Example:

![image](https://user-images.githubusercontent.com/13954434/193359114-7a4f6398-fa78-4a7e-bdda-4fcc3f4222c7.png)

## Logs

Pytest reports for each testing session are saved to `/var/log/wlanpi-hwtest/`:

Example:

```text
$ ls /var/log/wlanpi-hwtest | grep dc
dca632.fea1a2_report_automated_2021-12-30T175453.html
dca632.fea1a2_report_interactive_2021-12-30T175453.html
```

## Development & Contributing

See [WLAN-Pi/developers](https://github.com/WLAN-Pi/developers) for branch strategy, commit conventions, and setup guides. The pytest files under `hwtest/` are the device suite and need WLAN Pi Pro hardware. Repo-specific commands:

```bash
tox                  # install with the pinned deps, byte-compile, lint, check formatting
tox -e lint          # ruff check
tox -e format        # ruff format and safe fixes
```

## Changelog

See [debian/changelog](debian/changelog) for version history.

## Contributors

See [AUTHORS](AUTHORS.md).

## License

BSD-3-Clause. See [LICENSE](LICENSE).

## Open Source Software

Thank you to all the creators and maintainers of the following open source software used by `hwtest`:

* [dh-virtualenv](https://github.com/spotify/dh-virtualenv)
* [FIGlet](http://www.figlet.org/)
* [Font Awesome](https://fontawesome.com)
* [libgpiod](https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git)
* [Luma.OLED](https://luma-oled.readthedocs.io/en/latest)
* [Pillow](https://python-pillow.org)
* [Pytest](https://pytest.org)
* [Python](https://www.python.org)
* [RPi.GPIO](https://pypi.org/project/RPi.GPIO)
* [rpi-eeprom](https://github.com/raspberrypi/rpi-eeprom)

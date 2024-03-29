[![packagecloud-badge](https://img.shields.io/badge/deb-packagecloud.io-844fec.svg)](https://packagecloud.io/)

# wlanpi-hwtest

`hwtest` is a tool for the WLAN Pi project used to update VLI USB controller EEPROMs and run pytest to drive pass/fail testing.

## Example CLI usage

Optional arguments may be passed in to override default behaviors set in `/etc/wlanpi-hwtest/config.ini`. 

```bash
usage: hwtest [-h] [--debug] [-e] [--oled] [--firmware] [--waveshare] [--buttonsmash] [--verbose] [--version]

hwtest is a VLI USB Controller EEPROM updater and hardware testing tool for the WLAN Pi Pro.

optional arguments:
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

## Buttonsmash mode

- Install hwtest and disable the service

```bash
sudo apt update
sudo apt install wlanpi-hwtest
sudo systemctl disable wlanpi-hwtest
```

- Stop FPMS service 

```bash
sudo systemctl stop wlanpi-fpms
```

- Start `hwtest` in buttonsmash mode with OLED from CLI

```bash
sudo hwtest --buttons --oled
```

Example:

![image](https://user-images.githubusercontent.com/13954434/193359114-7a4f6398-fa78-4a7e-bdda-4fcc3f4222c7.png)

## Logs

Pytest reports for each testing session are saved to `/var/log/wlanpi-hwtest/`:

Example:

```bash
$ ls /var/log/wlanpi-hwtest | grep dc
dca632.fea1a2_report_automated_2021-12-30T175453.html
dca632.fea1a2_report_interactive_2021-12-30T175453.html
```

## Contributors

See [AUTHORS](AUTHORS.md).

## Code of Conduct

See [CoC](CODE_OF_CONDUCT.md).

## OSS

Thank you to all the creators and maintainers of the following open source software used by `hwtest`:

* [dh-virtualenv](https://github.com/spotify/dh-virtualenv)
* [FIGlet](http://www.figlet.org/)
* [Font Awesome](https://fontawesome.com)
* [GPIO Zero](https://gpiozero.readthedocs.io/en/stable)
* [Luma.OLED](https://luma-oled.readthedocs.io/en/latest)
* [Pillow](https://python-pillow.org)
* [Pytest](https://pytest.org)
* [Python](https://www.python.org)
* [RPi.GPIO](https://pypi.org/project/RPi.GPIO)
* [rpi-eeprom](https://github.com/raspberrypi/rpi-eeprom)

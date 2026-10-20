# Guidance for coding agents

`hwtest` is the WLAN Pi Pro hardware test suite. The pytest files under `hwtest/automated/` and `hwtest/interactive/` are the product: `hwtest` runs them on the device through `pytest.main()`. They are not unit tests, and they fail on a development host.

## Checks

- `tox` installs the package with the pinned dependencies on Python 3.13, byte-compiles it, runs `ruff check`, and checks formatting. CI runs the same.
- Behavior changes need a run on a WLAN Pi Pro with Debian Trixie. Stop `wlanpi-fpms` first, because both programs drive the same display and buttons. Run `sudo hwtest`, plus `--oled` or `--buttonsmash` when the change touches the display or buttons. Start `wlanpi-fpms` again afterwards.
- The fan tests leave GPIO 26 low. Restore it with `sudo pinctrl set 26 op dh`.

## Hardware and platform

- The target is Debian Trixie on BCM2711 boards. GPIO numbers in sysfs start at 512, so RPi.GPIO edge detection and gpiozero's native backend fail. Read the buttons with `gpiod` on `/dev/gpiochip0`, as wlanpi-fpms does.
- RPi.GPIO stays as a dependency because luma.core drives the display control pins with it.
- Use `pinctrl`, not `raspi-gpio`, and `/boot/firmware/config.txt`, not `/boot/config.txt`.
- Never run with `--firmware` and never set `firmware: True` without the device owner's approval. It writes the VL805 USB controller EEPROM and then reboots the WLAN Pi.

## Packaging

- The package is a dh-virtualenv build pinned to `python3.13`. `requirements.txt` holds every runtime pin, and `pyproject.toml` reads it.
- Installing never enables or starts `wlanpi-hwtest.service` (`dh_installsystemd --no-enable --no-start`). Keep it that way.
- A `debian/changelog` change merged to `main` deploys to Packagecloud. The deploy workflow checks that `hwtest/__version__.py` equals the changelog version without its `-N` revision.

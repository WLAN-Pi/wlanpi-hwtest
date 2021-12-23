import pytest
from hwtest.tests.helpers import run_command


@pytest.fixture
def capture_vcdbg_output(tmp_path):
    _dir = tmp_path / "t"
    _dir.mkdir()
    f = _dir / "dummy.log"
    cmd = ['sudo', 'vcdbg', 'log', 'msg', '>', f, '2>&1']
    run_command(cmd, invoke_shell=True)
    return(f)

    # f.write_text(config_data)
    # return(f)


def test_hi(capture_vcdbg_output):
    f = capture_vcdbg_output
    meh = f.open()
    # data = f.read()
    # print(data)


def test_dtoverlay():
    """
    Test command:
        read /boot/config.txt

    Results:
        True - "gpio-fan" exists in config.txt
        False - "gpio-fan" not found in config.txt
    """

    with open('/boot/config.txt', 'r') as f:
        config_txt = f.read()
        assert 'gpio-fan' in config_txt

from hwtest.helpers import run_command
import subprocess

def i2c_present():
    '''
    Use modinfo to check if i2c module is loaded
    '''
    try:
        cmd = "lsmod | grep i2c"
        subprocess.check_output(cmd, shell=True)
        return True
    except subprocess.CalledProcessError as exc:
        return False

def test_i2c_present():
    """
    Test command:
        lsmod | grep i2c
    
    Results:
        True - i2c module(s) detected in lsmod
        False - not detected
    """

    assert i2c_present() == True

# enable i2c: sudo raspi-config nonint do_i2c 0
# disable i2c: sudo raspi-config nonint do_i2c 1

def test_i2c_enabled():
    """
    Test command:
        sudo raspi-config nonint get_i2c

    Expect:
        0 = i2c is enabled
        1 = i2c is disabled
    """

    resp = run_command(["raspi-config", "nonint", "get_i2c"])

    assert resp == '0'

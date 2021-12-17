import subprocess

def bluetooth_module_present():
    '''
    Use modinfo to check if bluetooth module is loaded
    '''
    try:
        cmd = "lsmod | grep bluetooth"
        subprocess.check_output(cmd, shell=True)
        return True
    except subprocess.CalledProcessError as exc:
        return False


def test_bluetooth_module_present():
    """
    Test command:
        lsmod | grep bluetooth
    
    Results:
        True - bluetooth module detected in lsmod
        False - not detected
    """

    assert bluetooth_module_present() == True

def bluetooth_present():
    '''
    We want to use hciconfig here as it works OK when no devices are present
    '''
    try:
        cmd = "hciconfig | grep hci*"
        subprocess.check_output(cmd, shell=True)
        return True
    except subprocess.CalledProcessError as exc:
        return False


def test_bluetooth_present():
    """
    Test command:
        hciconfig | grep hci*
    
    Results:
        True - Bluetooth adapter(s) detected
        False - no Bluetooth adapter(s) detected
    """

    assert bluetooth_present() == True
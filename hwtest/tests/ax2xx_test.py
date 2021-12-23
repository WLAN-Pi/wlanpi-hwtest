from hwtest.tests.helpers import run_command


def test_2_intel_ax2xx():
    """
    Test command:
        lspci | grep Intel

    Results:
        True - (2) network controllers of "Intel Corporation Wi-Fi 6" exist
        False - <2 or >2 network controllers of "Intel Corporation Wi-Fi 6" exist
    """
    resp = run_command(["lspci", "|", "grep", "Intel"], invoke_shell=True)

    assert resp.count("Intel Corporation Wi-Fi 6") == 2

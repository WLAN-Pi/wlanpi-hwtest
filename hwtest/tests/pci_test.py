from hwtest.helpers import run_command


def test_pci_bridge():
    """
    Test that "PCI Bridge" is in the `lspci` output
    """

    resp = run_command(["lspci"])

    assert "PCI bridge" in resp

import subprocess 

def is_module_present(module: str ) -> bool:
    '''
    Use modinfo to check if module is loaded
    '''
    try:
        cmd = f"lsmod | grep {module}"
        subprocess.check_output(cmd, shell=True)
        return True
    except subprocess.CalledProcessError as exc:
        return False
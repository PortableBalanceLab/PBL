import subprocess

def run_shell_command(cmd, cwd=None):
    print(f"running: {cmd}", flush=True)
    return subprocess.run(cmd, shell=True, check=True, cwd=cwd)
import logging
import subprocess
import sys

from aiconsole.core.code_running.virtual_env.install_and_upgrade_pip import (
    install_and_update_pip,
)
from aiconsole.core.code_running.virtual_env.install_dependencies import (
    install_dependencies,
)
from aiconsole_toolkit.env import get_current_project_venv_path

_log = logging.getLogger(__name__)


def run_subprocess(*args):
    try:
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            _log.error(f"Command {' '.join(args)} failed with error: {stderr.decode().strip()}")
            raise RuntimeError(stderr.decode().strip())

        return stdout.decode().strip()
    except subprocess.CalledProcessError as e:
            _log.error(f"Error getting Python version: {e.stderr}")
            return None


def get_python_version(python_executable):
    """Returns the Python version for the given executable."""
    return run_subprocess(python_executable, "-c", "import sys; print(sys.version)")
    


async def create_dedicated_venv():
    venv_path = get_current_project_venv_path()  # Ensure this function returns a Path object
    system_python_version = get_python_version(sys.executable)

    if not venv_path.exists():
        _log.info(f"Creating venv in {venv_path}")
        run_subprocess(sys.executable, "-m", "venv", venv_path, "--system-site-packages")
    else:
        _log.info(f"Venv already exists in {venv_path}")

        # Check Python version in venv
        venv_python_executable = venv_path / ("Scripts" if sys.platform == "win32" else "bin") / "python"
        venv_python_version = get_python_version(venv_python_executable)

        if venv_python_version != system_python_version:
            _log.info("Upgrading venv due to different Python version.")
            run_subprocess(sys.executable, "-m", "venv", "--upgrade", venv_path)
            _log.info("Venv upgraded for new Python version.")
        else:
            _log.info("Venv upgrade not necessary, Python version matches.")

    install_and_update_pip(venv_path)
    install_dependencies(venv_path)

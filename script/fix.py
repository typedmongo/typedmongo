import subprocess

source_dirs = "typedmongo tests"
subprocess.check_call(f"isort --diff {source_dirs}", shell=True)
subprocess.check_call(f"black --diff {source_dirs}", shell=True)
subprocess.check_call(f"flake8 --ignore W503,E203,E501,E731 {source_dirs}", shell=True)
subprocess.check_call(f"mypy --ignore-missing-imports {source_dirs}", shell=True)

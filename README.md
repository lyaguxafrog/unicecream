# Unicecream

A simple formatter for removing [icecream](https://github.com/gruns/icecream) from your code after debugging.

![Python Version](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
[![PyPI - Version](https://img.shields.io/pypi/v/unicecream)](https://pypi.org/project/unicecream/)
[![GitHub License](https://img.shields.io/github/license/lyaguxafrog/unicecream)](https://github.com/lyaguxafrog/unicecream/blob/master/LICENSE.md)

## Example
```bash
lyaguxa@thinkpad:$ cat somefile.py
from icecream import ic

def return_one() -> int:
    return 1

ic(return_one())

lyaguxa@thinkpad:$ unicecream --check somefile.py
somefile.py:6:1: IC001 remove icecream call
somefile.py:1:1: IC003 remove icecream from-import

lyaguxa@thinkpad:$ unicecream somefile.py
fixed: somefile.py

lyaguxa@thinkpad:$ cat somefile.py
def return_one() -> int:
    return 1

return_one()
```

## Installation
```bash
pip install unicecream # for pyproject in python3.9 install unicecream[toml]
```

## Usage
```plaintext
usage: unicecream [-h] [--check] [--select CODE] [--ignore CODE] [--version] path

Remove icecream debug calls from Python files

positional arguments:
  path

optional arguments:
  -h, --help     show this help message and exit
  --check
  --select CODE  Select rule code
  --ignore CODE  Ignore rule code
  --version      show program's version number and exit
```

## Configuration
In pyproject:
```toml
[tool.unicecream]

# Rules to enable by default
select = ["IC001", "IC002", "IC003"]

# Rules to ignore
ignore = []

# Paths to skip
exclude = [
    ".venv",
    "__pycache__",
    "build",
    "dist"
]
```

## Pre-commit
```yaml
repos:
  - repo: https://github.com/lyaguxafrog/unicecream
    rev: 0.2.1 # 0.2.1 is the minimum version that supports pre-commit.
    hooks:
      - id: unicecream
```

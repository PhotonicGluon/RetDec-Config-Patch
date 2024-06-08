# RetDec-Config-Patch

<!-- TODO: Update base URLs -->

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/retdec-config-patch?pypiBaseUrl=https%3A%2F%2Ftest.pypi.org&logo=python)
![PyPI - Version](https://img.shields.io/pypi/v/retdec-config-patch?pypiBaseUrl=https%3A%2F%2Ftest.pypi.org&logo=pypi)
![PyPI - Downloads](https://img.shields.io/pypi/dm/retdec-config-patch)
![PyPI - License](https://img.shields.io/pypi/l/retdec-config-patch?pypiBaseUrl=https%3A%2F%2Ftest.pypi.org)

Patch for the broken `--config` option in [RetDec](https://github.com/avast/retdec).

## Installation

You can choose to install the patch from package or building from scratch. In either case, you will still need to [activate the patch](#activating-the-patch).

### Installing from Package

The `retdec-config-patch` is available on PyPi. It is important to note that the package is to be installed **system-wide** so that the patch binary can be accessed across the whole system.

```bash
pip install retdec-config-patch
```

Troubleshooting:

- If `pip` does not work, try `pip3`.

### Building the Package

One could also build the package from scratch. This is particularly useful for contributions.

1. Clone the repository.
2. If you are using VSCode, set up the devcontainer.
    - If that doesn't work, follow the next few steps.
    - Otherwise, go to step 6.
3. Create a new virtual environment by running `python3 -m venv venv`.
4. Activate the virtual environment.
5. Install [Poetry](https://python-poetry.org/) in the virtual environment using `pip install poetry`.
    - Check that Poetry was successfully installed by running `poetry --version`.
6. Install the dependencies by running `poetry install`.

## Activating/Deactivating the Patch

Installing the package does not mean that the patch is active; you need to manually activate it.

### Activating the Patch

To activate the patch, run

```bash
retdec-config-patch
```

This will perform the necessary checks before implementing the patch.

Once the patch is activated, you can use `retdec-decompiler` as per normal. The only difference is that the `--config` option works properly now.

### Deactivating the Patch

If you want to deactivate the patch, run

```bash
undo-retdec-config-patch
```

### License

The `retdec-config-patch` is licensed under the MIT license.

```
MIT License

Copyright (c) 2024 Ryan Kan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Appendix: Rationale

TODO: ADD

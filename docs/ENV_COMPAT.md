# Environment Compatibility Check

Generated: 2026-03-22 15:22 UTC
- Python: `3.14.3`
- Platform: `macOS-26.1-arm64-arm-64bit-Mach-O`

## Issues
- Python 3.14 may fail building scipy from source on some macOS setups (Fortran toolchain missing).

## Recommendations
- Use Python 3.11/3.12 for smoother scientific package installation.
- Prefer virtualenv: `python3 -m venv .venv && source .venv/bin/activate`
- Install base test deps for lightweight checks: `pip install numpy joblib`

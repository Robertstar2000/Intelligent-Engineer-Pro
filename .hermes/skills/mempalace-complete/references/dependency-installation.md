# MemPalace Dependency Installation Guide

This guide provides steps to install the required Python dependencies for the MemPalace long-term memory enhancement layer.

## Required Packages

- numpy
- sentence-transformers
- faiss-cpu
- transformers
- torch
- scikit-learn
- scipy

## Installation in Hermes Agent Environment

The Hermes agent uses a virtual environment located at:
  ~/.hermes/hermes-agent/venv

To install packages in this environment, use the venv's pip:

```bash
/home/bob/.hermes/hermes-agent/venv/bin/pip3 install numpy sentence-transformers faiss-cpu transformers torch scikit-learn scipy
```

## Verification

After installation, verify that the packages are installed correctly:

```bash
/home/bob/.hermes/hermes-agent/venv/bin/python3 -c "import numpy, sentence_transformers, faiss, transformers, torch, sklearn, scipy; print('All dependencies installed')"
```

## Troubleshooting

### Missing pip in the virtual environment

If the virtual environment does not have pip installed, you can install it by running:

```bash
/home/bob/.hermes/hermes-agent/venv/bin/python3 -m ensurepip --upgrade
```

### Network Issues

If you encounter network issues during installation, try:

1. Using the `--no-cache-dir` flag to avoid cache-related problems:
   ```bash
   /home/bob/.hermes/hermes-agent/venv/bin/pip3 install --no-cache-dir <package>
   ```

2. Installing packages one at a time to isolate failures.

### Version Conflicts

If you encounter version conflicts, consider installing specific versions that are known to work together. As of the time of writing, the following versions have been tested:

- numpy==2.4.6
- sentence-transformers==5.5.1
- faiss-cpu==1.14.3
- transformers==5.12.0
- torch==2.12.0
- scikit-learn==1.9.0
- scipy==1.17.1

You can install specific versions with:

```bash
/home/bob/.hermes/hermes-agent/venv/bin/pip3 install numpy==2.4.6 sentence-transformers==5.5.1 faiss-cpu==1.14.3 transformers==5.12.0 torch==2.12.0 scikit-learn==1.9.0 scipy==1.17.1
```

## Notes

- The MemPalace system will not function correctly without these dependencies.
- The embedding model (sentence-transformers) requires torch and its dependencies, which can be large and time-consuming to download.
- In cron jobs or isolated environments, ensure that the virtual environment's path is correctly set in the PYTHONPATH or by using the full path to the python interpreter.
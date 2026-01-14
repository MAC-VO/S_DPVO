#!/bin/bash
set -euo pipefail

# Install standalone lietorch (shared between DPVO and DROID-SLAM)
# Using DROID-SLAM's thirdparty lietorch as the canonical source
LIETORCH_PATH="../DROID_SLAM/thirdparty/lietorch"

if ! python -c "import lietorch" 2>/dev/null; then
    if [ -d "$LIETORCH_PATH" ]; then
        echo "Installing lietorch from $LIETORCH_PATH..."
        pip install -v "$LIETORCH_PATH" --no-build-isolation
    else
        echo "Error: lietorch not found at $LIETORCH_PATH"
        echo "Make sure DROID_SLAM submodule is initialized."
        exit 1
    fi
else
    echo "lietorch already installed, skipping..."
fi

# Install DPVO (CUDA extensions: cuda_corr, cuda_ba)
pip install -v -e . --no-build-isolation

#!/bin/bash
set -euo pipefail

# Auto-detect GPU architecture and compile only for current GPU.
CUDA_ARCH=$(python -c "import torch; cc = torch.cuda.get_device_capability(); print(f'{cc[0]}.{cc[1]}')" 2>/dev/null) || {
    echo "Error: Failed to detect GPU architecture. Ensure CUDA is available."
    exit 1
}
export TORCH_CUDA_ARCH_LIST="$CUDA_ARCH"
echo "Compiling for GPU architecture: $CUDA_ARCH"

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

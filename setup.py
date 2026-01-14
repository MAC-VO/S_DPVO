import os.path as osp

from setuptools import setup, find_packages

try:
    from torch.utils.cpp_extension import BuildExtension, CUDAExtension
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError(
        "dpvo requires PyTorch to build its CUDA extensions. "
        "Please install torch in your current environment and reinstall dpvo. "
        "If you are using pip's build isolation, export TORCH_INSTALL_PATH or "
        "DPVO_TORCH_PREFIX to the site-packages containing torch, or rerun with "
        "`pip install -e . --no-build-isolation`."
    ) from exc

ROOT = osp.dirname(osp.abspath(__file__))



setup(
    name='dpvo',
    packages=find_packages(),
    ext_modules=[
        CUDAExtension('cuda_corr',
            sources=['dpvo/altcorr/correlation.cpp', 'dpvo/altcorr/correlation_kernel.cu'],
            extra_compile_args={
                'cxx':  ['-O3'], 
                'nvcc': ['-O3'],
            }),
        CUDAExtension('cuda_ba',
            sources=['dpvo/fastba/ba.cpp', 'dpvo/fastba/ba_cuda.cu'],
            extra_compile_args={
                'cxx':  ['-O3'], 
                'nvcc': ['-O3'],
            }),
        # lietorch_backends is now provided by standalone lietorch package
        # (installed from DROID_SLAM/thirdparty/lietorch)
    ],
    cmdclass={
        'build_ext': BuildExtension
    })

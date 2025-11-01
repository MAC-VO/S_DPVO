import os
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Sequence

from setuptools import build_meta as _orig_backend


def _candidate_site_packages(python_version: str) -> Iterable[Path]:
    """Derive potential site-packages directories with user overrides first."""
    overrides = []
    manual_path = os.environ.get("TORCH_INSTALL_PATH")
    if manual_path:
        overrides.append(Path(manual_path))

    manual_prefix = os.environ.get("DPVO_TORCH_PREFIX")
    if manual_prefix:
        overrides.extend(_prefix_to_candidates(Path(manual_prefix), python_version))

    for env_var in ("CONDA_PREFIX", "VIRTUAL_ENV", "PYENV_VIRTUAL_ENV"):
        prefix = os.environ.get(env_var)
        if prefix:
            overrides.extend(_prefix_to_candidates(Path(prefix), python_version))

    pythonpath = os.environ.get("PYTHONPATH")
    if pythonpath:
        for item in pythonpath.split(os.pathsep):
            if item:
                overrides.append(Path(item))

    base_prefix = getattr(sys, "base_prefix", sys.prefix)
    overrides.extend(_prefix_to_candidates(Path(base_prefix), python_version))

    return overrides


def _prefix_to_candidates(prefix: Path, python_version: str) -> Sequence[Path]:
    """Return common site-packages directories for a prefix."""
    return [
        prefix / "lib" / python_version / "site-packages",
        prefix / "lib" / "site-packages",
        prefix / "Lib" / "site-packages",
        prefix / "site-packages",
    ]


def _ensure_torch_available() -> None:
    """Ensure torch can be imported, attempting to reuse the caller's environment."""
    try:
        import torch  # noqa: F401
        return
    except ModuleNotFoundError:
        pass

    python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"
    inserted: list[str] = []

    for candidate in _candidate_site_packages(python_version):
        if not candidate.exists():
            continue
        path = str(candidate.resolve())
        if path not in sys.path:
            sys.path.insert(0, path)
            inserted.append(path)
            try:
                import torch  # noqa: F401
                return
            except ModuleNotFoundError:
                continue

    error_hint = (
        "Could not import torch while building dpvo. "
        "Install torch in your environment before installing dpvo, "
        "or set TORCH_INSTALL_PATH/DPVO_TORCH_PREFIX to the site-packages "
        "containing your torch installation. Alternatively run "
        "`pip install -e . --no-build-isolation`."
    )
    if inserted:
        error_hint += f" Searched paths: {', '.join(inserted)}."
    raise ModuleNotFoundError(error_hint)


def _prepare(kwargs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Normalize kwargs before delegating to setuptools' backend."""
    _ensure_torch_available()
    return kwargs or {}


def build_wheel(wheel_directory: str, config_settings: Optional[Dict[str, Any]] = None, metadata_directory: Optional[str] = None) -> str:
    _prepare(config_settings)
    return _orig_backend.build_wheel(wheel_directory, config_settings, metadata_directory)


def build_editable(wheel_directory: str, config_settings: Optional[Dict[str, Any]] = None, metadata_directory: Optional[str] = None) -> str:
    _prepare(config_settings)
    return _orig_backend.build_editable(wheel_directory, config_settings, metadata_directory)


def build_sdist(sdist_directory: str, config_settings: Optional[Dict[str, Any]] = None) -> str:
    _prepare(config_settings)
    return _orig_backend.build_sdist(sdist_directory, config_settings)


def prepare_metadata_for_build_wheel(metadata_directory: str, config_settings: Optional[Dict[str, Any]] = None) -> str:
    _prepare(config_settings)
    return _orig_backend.prepare_metadata_for_build_wheel(metadata_directory, config_settings)


def prepare_metadata_for_build_editable(metadata_directory: str, config_settings: Optional[Dict[str, Any]] = None) -> str:
    _prepare(config_settings)
    return _orig_backend.prepare_metadata_for_build_editable(metadata_directory, config_settings)


def get_requires_for_build_wheel(config_settings: Optional[Dict[str, Any]] = None) -> Sequence[str]:
    _prepare(config_settings)
    return _orig_backend.get_requires_for_build_wheel(config_settings)


def get_requires_for_build_editable(config_settings: Optional[Dict[str, Any]] = None) -> Sequence[str]:
    _prepare(config_settings)
    return _orig_backend.get_requires_for_build_editable(config_settings)


def get_requires_for_build_sdist(config_settings: Optional[Dict[str, Any]] = None) -> Sequence[str]:
    _prepare(config_settings)
    return _orig_backend.get_requires_for_build_sdist(config_settings)

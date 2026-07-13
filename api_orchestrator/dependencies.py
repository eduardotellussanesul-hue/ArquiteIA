import importlib
import sys
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
_backend = None


def _find_extension_artifact(name_prefix='arquiteia'):
    """Search common build directories for the compiled extension (.pyd/.so).

    Returns the parent directory to add to sys.path or None.
    """
    repo_root = Path(__file__).resolve().parents[1]
    candidates = []
    # common locations
    search_dirs = [
        repo_root / 'backend_simulator' / 'build' / 'Release',
        repo_root / 'backend_simulator' / 'build',
        repo_root / 'backend_simulator',
    ]
    for d in search_dirs:
        if not d.exists():
            continue
        for ext in ('*.pyd', '*.so', '*.dll'):
            for p in d.rglob(ext):
                if p.stem.startswith(name_prefix):
                    candidates.append(p)
    if candidates:
        # prefer first match
        return candidates[0].parent
    return None


def get_backend():
    """Attempt to import the compiled `arquiteia` module.

    On failure, try to find the built extension artifact and add its
    directory to `sys.path`, then retry the import.
    Returns the imported module or None.
    """
    global _backend
    if _backend is not None:
        return _backend

    try:
        _backend = importlib.import_module('arquiteia')
        return _backend
    except Exception as e:
        logger.warning('Initial import of arquiteia failed: %s', e)

    # Try to locate built extension and add to path
    artifact_dir = _find_extension_artifact('arquiteia')
    if artifact_dir:
        artifact_dir_str = str(artifact_dir)
        if artifact_dir_str not in sys.path:
            sys.path.insert(0, artifact_dir_str)
            logger.info('Added %s to sys.path to load arquiteia', artifact_dir_str)
        try:
            _backend = importlib.import_module('arquiteia')
            return _backend
        except Exception as e:
            logger.error('Import after adding artifact dir failed: %s', e)

    logger.error('Could not import arquiteia. Make sure the C++ extension is built.')
    return None


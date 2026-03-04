"""File I/O operations for MTG to D&D conversion."""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def load_json(filepath: str) -> Dict[str, Any] | List[Any]:
    """
    Load JSON data from file with error handling.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Parsed JSON data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If JSON is invalid
    """
    try:
        with open(filepath, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {filepath}: {e}")
        raise


def save_json(data: Any, filepath: str, pretty: bool = False) -> None:
    """
    Save data to JSON file.
    
    Args:
        data: Data to serialize
        filepath: Output file path
        pretty: Whether to format with indentation
    """
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2 if pretty else None)
        logger.info(f"Saved data to {filepath}")
    except IOError as e:
        logger.error(f"Failed to save {filepath}: {e}")
        raise


def append_to_file(filepath: str, content: str) -> None:
    """
    Append text to file.
    
    Args:
        filepath: File path
        content: Content to append
    """
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(content + "\n")
    except IOError as e:
        logger.error(f"Failed to append to {filepath}: {e}")
        raise


# Data caching for performance
_json_cache: Dict[str, Any] = {}


def load_json_cached(filepath: str) -> Dict[str, Any] | List[Any]:
    """Load JSON with caching to avoid repeated file I/O."""
    if filepath not in _json_cache:
        _json_cache[filepath] = load_json(filepath)
    return _json_cache[filepath]


def clear_cache() -> None:
    """Clear the JSON cache."""
    _json_cache.clear()

"""
Configuration management for FlowFacilitator
"""

import json
import os
from pathlib import Path
from typing import Dict, Any


def get_config_path(custom_path: str = None, dev_mode: bool = False) -> Path:
    """Get the configuration file path"""
    if custom_path:
        return Path(custom_path)
    
    if dev_mode:
        # Use local config for development
        return Path(__file__).parent.parent / 'config.example.json'
    
    # Production path
    config_dir = Path.home() / 'Library' / 'Application Support' / 'FlowFacilitator'
    return config_dir / 'config.json'


def load_config(custom_path: str = None, dev_mode: bool = False) -> Dict[str, Any]:
    """Load configuration from file"""
    config_path = get_config_path(custom_path, dev_mode)
    
    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found at {config_path}. "
            f"Please copy config.example.json to the appropriate location."
        )
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Expand paths
    if 'native_messaging' in config:
        manifest_path = config['native_messaging']['manifest_path']
        config['native_messaging']['manifest_path'] = os.path.expanduser(manifest_path)
    
    return config


def save_config(config: Dict[str, Any], custom_path: str = None, dev_mode: bool = False):
    """Save configuration to file"""
    config_path = get_config_path(custom_path, dev_mode)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

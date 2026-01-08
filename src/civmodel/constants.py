"""
Global constants and preset configurations for the civilization meta-model.
"""

from typing import Dict, Any
import numpy as np

# =============================================================================
# 全局默认参数配置
# =============================================================================
PARAMS = {
    # 二维扫描设置 / 2D Scan Settings
    "male_space_range": (0.2, 1.0),
    "male_space_points": 12,
    "female_activation_range": (0.0, 1.0),
    "female_activation_points": 15,
    
    # 模型基础参数 / Base Model Parameters
    "N": 100,
    "d": 2,
    "simulation_steps": 300,
    "random_seeds": [42, 43, 44, 45, 46],  # 5 seeds for better statistics
    
    # 探索与制度参数 / Exploration & Institution Parameters
    "exploration_prob": 0.5,
    "exploration_strength": 0.52,
    "institution_learning_rate": 0.04,
    "institution_pull_strength": 0.05,
    "state_bounds": (-1, 1),
    
    # 创新检测参数 / Innovation Detection Parameters
    "innovation_base_threshold": 0.04,
    "female_threshold_modulation": 0.4,
    "history_buffer_size": 3,
    
    # 协同效应参数 / Synergy Parameters
    "synergy_female_threshold": 0.4,
    "synergy_diversity_weight": 2.0,
    "synergy_upper_bound": 3.0,
    
    # 性能与日志参数 / Performance & Logging
    "verbose": False,
    "save_trajectory": True,
}

# =============================================================================
# 历史时期预设参数
# =============================================================================
HISTORICAL_PRESETS = {
    "stagnation_typical": {
        "male_explore_space": 0.3,
        "female_activation": 0.05,
        "N": 80,
        "d": 2,
        "innovation_base_threshold": 0.05,
        "description": "Typical agrarian society with limited exploration"
    },
    "tang_song_window": {
        "male_explore_space": 0.75,
        "female_activation": 0.25,
        "N": 150,
        "d": 4,
        "innovation_base_threshold": 0.035,
        "institution_learning_rate": 0.03,
        "description": "Tang-Song transition period: commercial and cultural flourishing"
    },
    "renaissance_window": {
        "male_explore_space": 0.78,
        "female_activation": 0.3,
        "N": 120,
        "d": 4,
        "exploration_strength": 0.6,
        "description": "European Renaissance: revival of arts and sciences"
    },
    "industrial_transition": {
        "male_explore_space": 0.85,
        "female_activation": 0.65,
        "N": 200,
        "d": 6,
        "innovation_base_threshold": 0.025,
        "synergy_female_threshold": 0.35,
        "description": "Industrial revolution: technological acceleration"
    },
    "modern_creative": {
        "male_explore_space": 0.9,
        "female_activation": 0.85,
        "N": 300,
        "d": 8,
        "exploration_prob": 0.6,
        "synergy_female_threshold": 0.3,
        "description": "Modern creative society: high diversity and exploration"
    }
}

# =============================================================================
# 工具函数
# =============================================================================
def merge_params(custom_params: Dict[str, Any], base_params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    安全合并参数字典，自定义参数优先。
    
    Parameters
    ----------
    custom_params : dict
        自定义参数
    base_params : dict, optional
        基础参数，默认为全局 PARAMS
        
    Returns
    -------
    dict
        合并后的参数字典
    """
    if base_params is None:
        base_params = PARAMS.copy()
    
    result = base_params.copy()
    result.update(custom_params)
    return result


def load_preset(preset_name: str) -> Dict[str, Any]:
    """
    加载历史时期预设配置。
    
    Parameters
    ----------
    preset_name : str
        预设名称，如 "tang_song_window"
        
    Returns
    -------
    dict
        预设参数字典
        
    Raises
    ------
    KeyError
        当预设名称不存在时
    """
    if preset_name not in HISTORICAL_PRESETS:
        available = list(HISTORICAL_PRESETS.keys())
        raise KeyError(f"Preset '{preset_name}' not found. Available: {available}")
    
    return merge_params(HISTORICAL_PRESETS[preset_name])


def validate_params(params: Dict[str, Any]) -> None:
    """
    验证参数有效性。
    
    Parameters
    ----------
    params : dict
        待验证的参数
        
    Raises
    ------
    ValueError
        当参数无效时
    """
    # 检查必要参数
    required = ["N", "d", "male_explore_space", "female_activation"]
    for key in required:
        if key not in params:
            raise ValueError(f"Missing required parameter: {key}")
    
    # 检查数值范围
    if params["male_explore_space"] < 0 or params["male_explore_space"] > 1:
        raise ValueError(f"male_explore_space must be between 0 and 1, got {params['male_explore_space']}")
    
    if params["female_activation"] < 0 or params["female_activation"] > 1:
        raise ValueError(f"female_activation must be between 0 and 1, got {params['female_activation']}")
    
    if params["N"] <= 0:
        raise ValueError(f"N must be positive, got {params['N']}")
    
    if params["d"] <= 0:
        raise ValueError(f"d must be positive, got {params['d']}")


def get_param_ranges() -> Dict[str, tuple]:
    """
    获取关键参数的合理范围，用于参数扫描。
    
    Returns
    -------
    dict
        参数范围字典
    """
    return {
        "male_explore_space": (0.1, 1.0),
        "female_activation": (0.0, 1.0),
        "exploration_strength": (0.1, 1.0),
        "innovation_base_threshold": (0.01, 0.2),
        "institution_pull_strength": (0.01, 0.2),
    }
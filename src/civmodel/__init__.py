"""
Civilization Meta-Model (CMM)
A computational framework for simulating civilizational phase transitions.
"""

from .core import CivilizationModel
from .scanner import ParameterScanner
from .constants import PARAMS, HISTORICAL_PRESETS, load_preset, merge_params
from .utils.visualize import plot_phase_diagram, plot_innovation_timeseries
EnhancedGenderModel = CivilizationModel  # 如果希望保持方案中的名称
__version__ = "0.1.0"
__author__ = "Civilization Meta-Model Contributors"
__all__ = [
    "CivilizationModel",
    "EnhancedGenderModel", 
    "ParameterScanner",
    "PARAMS",
    "HISTORICAL_PRESETS",
    "load_preset",
    "merge_params",
    "np.random.RandomState",
    "plot_phase_diagram",
    "plot_innovation_timeseries",
]
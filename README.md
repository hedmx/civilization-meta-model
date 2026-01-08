
# Civilization Meta-Model (CMM)

A computational meta-framework for simulating structural phase transitions in civilizational evolution.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](docs/CONTRIBUTING.md)

## 🧠 Core Idea

Civilizational leaps are not merely accumulations of innovation, but **structural phase transitions** triggered when the system's "effective choice space" expands nonlinearly. This model formalizes a two-layer mechanism:

1.  **Window Period (Necessary Condition)**: Expansion of the `male_explore_space` parameter (representing the exploration freedom of dominant social groups).
2.  **Transition Period (Sufficient Condition)**: Activation of the `female_activation` parameter beyond a critical threshold, unlocking suppressed cognitive diversity and generating synergistic effects.

## 🚀 Quick Start

```bash
# Install from PyPI (recommended)
pip install civilization-metamodel

# OR install from source
git clone https://github.com/hedmx/Civilization-Meta-Model.git
cd Civilization-Meta-Model
pip install -e .
Run your first simulation in 3 lines:

python
from civmodel import CivilizationModel
import matplotlib.pyplot as plt

# 1. Create a civilization
model = CivilizationModel(male_explore_space=0.8, female_activation=0.3)
# 2. Run simulation
innovations, synergies, metadata = model.run(steps=300)
# 3. Analyze
print(f"Innovation Rate: {metadata['innovation_rate']*100:.2f}%")
print(f"Average Synergy: {metadata['avg_synergy']:.2f}")
📈 Explore Key Findings
The model robustly reproduces three distinct civilizational phases:

Phase	Parameters	Expected Innovation	Historical Analogy
Stagnation	male_explore_space=0.3, female_activation=0.0	< 5%	Traditional agrarian societies
Window Period	male_explore_space=0.75, female_activation=0.3	10-30%	Tang-Song China, Renaissance
Transition	male_explore_space=0.85, female_activation=0.8	> 50%	Industrial Revolution
Run the phase diagram scan:

bash
python examples/01_basic_usage.py
🗺️ Phase Diagram & Synergy Effects
The model reveals a non-linear synergy effect: when female activation exceeds ~0.4, the system benefits from cognitive diversity, dramatically boosting innovation efficiency.

https://docs/images/phase_diagram.png

🧩 Project Structure
src/civmodel/core.py - Core simulation engine (CivilizationModel)

src/civmodel/scanner.py - Parameter space scanning utilities (ParameterScanner)

src/civmodel/constants.py - Default parameters & configuration (PARAMS, HISTORICAL_PRESETS)

src/civmodel/utils/visualize.py - Visualization utilities

examples/ - Tutorial notebooks and scripts

docs/ - Documentation and theory

🔬 Advanced Usage
Historical Case Study
python
from civmodel.constants import HISTORICAL_PRESETS

# Load Tang-Song transition parameters
tang_song_params = HISTORICAL_PRESETS['tang_song_window']
model = CivilizationModel(**tang_song_params)
innovations, synergies, metadata = model.run(steps=500)
Parameter Space Analysis
python
from civmodel import ParameterScanner

scanner = ParameterScanner()
results = scanner.scan_2d(
    male_space_range=(0.2, 1.0),
    female_activation_range=(0.0, 1.0),
    seeds=[42, 43, 44]
)
Custom Model Extensions
python
from civmodel import CivilizationModel
import numpy as np

class NetworkCivilizationModel(CivilizationModel):
    """Add network effects between agents"""
    
    def __init__(self, network_density=0.1, **kwargs):
        super().__init__(**kwargs)
        self.network_density = network_density
        self._initialize_network()
    
    def _initialize_network(self):
        """Create random interaction network"""
        self.adjacency = np.random.rand(self.N, self.N) < self.network_density
        np.fill_diagonal(self.adjacency, 0)
    
    def _agent_exploration(self, agent_idx: int) -> np.ndarray:
        """Override with network-aware exploration"""
        base_exploration = super()._agent_exploration(agent_idx)
        
        # Add social influence from neighbors
        neighbors = np.where(self.adjacency[agent_idx])[0]
        if len(neighbors) > 0:
            neighbor_states = self.states[neighbors]
            social_influence = neighbor_states.mean(axis=0) - self.states[agent_idx]
            social_influence = social_influence * 0.1  # Small influence weight
            return base_exploration + social_influence
        
        return base_exploration
📚 Learn the Theory
For a deep dive into the theoretical foundations:

The Meta-Model Theory - Philosophical and mathematical basis

Computational Historical Dynamics - Methodology

From Gender to General Diversity - Model extensions

🧪 Testing
Run the test suite:

bash
pytest tests/ -v
🤝 Contributing
We welcome contributions! Whether you're a historian, computational social scientist, or developer, there are many ways to help:

Test historical scenarios - Apply the model to different civilizations

Improve visualization - Create better explanatory graphics

Extend the model - Add economic, ecological, or network layers

Translate documentation - Make the framework accessible globally

See our Contributing Guidelines for details.

📄 Citation
If you use CMM in your research, please cite:

bibtex
@software{civilization_meta_model,
  title = {Civilization Meta-Model: A Computational Framework for Civilizational Phase Transitions},
  author = {Civilization Meta-Model Contributors},
  year = {2024},
  url = {https://github.com/hedmx/Civilization-Meta-Model},
  version = {0.1.0}
}
🔗 Related Work
Seshat Global History Databank - Historical data for validation

Cultural Evolution - Theoretical foundations

Complexity Explorer - Educational resources

📊 Data Availability
The model generates all data internally. Historical parameter presets are based on literature estimates.

🐛 Bug Reports and Feature Requests
Please use the GitHub Issues page.

License
MIT License. See LICENSE for details.



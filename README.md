# Civilization Meta-Model (CMM) 文明元模型
用于模拟文明演化中结构性相变的计算元框架。

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](docs/CONTRIBUTING.md)
[![Documentation](https://img.shields.io/badge/docs-latest-blue)](https://hedmx.github.io/Civilization-Meta-Model/)
[![Examples](https://img.shields.io/badge/examples-4-orange)](examples/)

## 🧠 核心理念 | Core Idea

文明的跃迁不仅仅是创新的积累，而是系统"有效选择空间"非线性扩展所触发的**结构性相变**。本模型形式化了一个双层机制：

Civilizational leaps are not merely accumulations of innovation, but **structural phase transitions** triggered when the system's "effective choice space" expands nonlinearly. This model formalizes a two-layer mechanism:

1.  **窗口期（必要条件）**：`male_explore_space` 参数的扩展（代表主导社会群体的探索自由度）。  
    **Window Period (Necessary Condition)**: Expansion of the `male_explore_space` parameter (representing the exploration freedom of dominant social groups).

2.  **转型期（充分条件）**：`female_activation` 参数超过临界阈值，释放被抑制的认知多样性并产生协同效应。  
    **Transition Period (Sufficient Condition)**: Activation of the `female_activation` parameter beyond a critical threshold, unlocking suppressed cognitive diversity and generating synergistic effects.

## 🚀 快速开始 | Quick Start

```bash
# 从PyPI安装（推荐）| Install from PyPI (recommended)
pip install civilization-metamodel

# 或从源码安装 | OR install from source
git clone https://github.com/hedmx/Civilization-Meta-Model.git
cd Civilization-Meta-Model
pip install -e .
```

用3行代码运行你的第一个模拟 | Run your first simulation in 3 lines:

```python
from civmodel import CivilizationModel

# 1. 创建一个文明 | Create a civilization
model = CivilizationModel(male_explore_space=0.8, female_activation=0.3)
# 2. 运行模拟 | Run simulation
innovations, synergies, metadata = model.run(steps=300)
# 3. 分析结果 | Analyze results
print(f"创新率: {metadata['innovation_rate']*100:.2f}%")
print(f"平均协同效应: {metadata['avg_synergy']:.2f}")
```

## 📈 关键发现 | Key Findings

该模型稳健地复现了三种不同的文明阶段，与历史观察一致：

The model robustly reproduces three distinct civilizational phases, consistent with historical observations:

| 阶段 Phase | 参数 Parameters | 预期创新率 Expected Innovation | 历史类比 Historical Analogy |
|------------|-----------------|-------------------------------|----------------------------|
| **停滞期 Stagnation** | male=0.3, female=0.0 | < 5% | 传统农业社会 Traditional agrarian societies |
| **窗口期 Window Period** | male=0.75, female=0.3 | 10-30% | 唐宋转型、文艺复兴 Tang-Song China, Renaissance |
| **转型期 Transition** | male=0.85, female=0.8 | > 50% | 工业革命 Industrial Revolution |

运行相图扫描 | Run the phase diagram scan:
```bash
python examples/01_basic_usage.py
```

## 🗺️ 相图与协同效应 | Phase Diagram & Synergy Effects

该模型揭示了一个非线性协同效应：当女性激活度超过约0.4时，系统受益于认知多样性，显著提升创新效率。

The model reveals a non-linear synergy effect: when female activation exceeds ~0.4, the system benefits from cognitive diversity, dramatically boosting innovation efficiency.

**关键阈值发现** | **Key Threshold Findings**:
- **临界点**：female_activation ≈ 0.4-0.5 | **Critical point**: female_activation ≈ 0.4-0.5
- **窗口期条件**：male_explore_space > 0.6 | **Window period condition**: male_explore_space > 0.6
- **协同效应爆发**：激活度>0.4时创新率非线性增长 | **Synergy explosion**: Non-linear innovation growth when activation > 0.4

## 📊 案例研究结果 | Case Study Results

### 唐宋转型期分析 | Tang-Song Transition Analysis
通过参数化历史分析，模型成功再现了唐宋时期的创新加速现象：

Through parameterized historical analysis, the model successfully reproduces the innovation acceleration phenomenon of the Tang-Song period:

| 时期 Period | 模型参数 Model Parameters | 创新率 Innovation Rate | 历史解释 Historical Interpretation |
|-------------|--------------------------|------------------------|-----------------------------------|
| **唐代早期 Early Tang** | male=0.65, female=0.35 | 15-20% | 科举制度确立，文化开放 Imperial examination established, cultural openness |
| **宋代高峰 Song Peak** | male=0.82, female=0.48 | 25-30% | 商业革命，科技创新繁荣 Commercial revolution, technological innovation boom |
| **绩效提升 Performance Gain** | +0.17探索空间, +0.13激活度<br>+0.17 exploration, +0.13 activation | **+67%** | 制度完善与社会结构优化 Institutional refinement and social structure optimization |

### 模型扩展验证 | Model Extension Validation
- **网络增强**：社会网络连接显著提升信息扩散效率，**创新率+10%** | **Network enhancement**: Social network connections significantly improve information diffusion efficiency, **+10% innovation rate**
- **记忆增强**：经验学习机制减少重复探索，提升创新效率，**创新率+10%** | **Memory enhancement**: Experiential learning reduces redundant exploration, improves innovation efficiency, **+10% innovation rate**
- **简化设计**：验证核心机制，避免过度复杂化 | **Simplified design**: Validates core mechanisms, avoids over-complexity

## 🧩 项目结构 | Project Structure

```
src/civmodel/
├── core.py              # 核心模拟引擎 | Core simulation engine (CivilizationModel)
├── scanner.py           # 参数空间扫描工具 | Parameter space scanning utilities (ParameterScanner)
├── constants.py         # 默认参数与配置 | Default parameters & configuration (PARAMS, HISTORICAL_PRESETS)
└── utils/visualize.py  # 可视化工具 | Visualization utilities

examples/               # 示例代码 | Example code
├── 01_basic_usage.py           # 基础使用方法 | Basic usage
├── 02_tang_song_case_study.py  # 唐宋案例研究 | Tang-Song case study
├── 03_parameter_analysis.py    # 参数空间分析 | Parameter space analysis
└── 04_custom_model.py         # 自定义模型扩展 | Custom model extensions

docs/                   # 文档和理论 | Documentation and theory
tests/                  # 测试套件 | Test suite
```

## 🔬 高级用法 | Advanced Usage

### 历史案例研究 | Historical Case Study
```python
from civmodel.constants import HISTORICAL_PRESETS

# 加载唐宋转型参数 | Load Tang-Song transition parameters
tang_song_params = HISTORICAL_PRESETS['tang_song_window']
model = CivilizationModel(**tang_song_params)
innovations, synergies, metadata = model.run(steps=500)
```

### 参数空间分析 | Parameter Space Analysis
```python
from civmodel import ParameterScanner

scanner = ParameterScanner()
results = scanner.scan_2d(
    male_space_range=(0.2, 1.0),
    female_activation_range=(0.0, 1.0),
    seeds=[42, 43, 44]
)
```

### 自定义模型扩展 | Custom Model Extensions
基于 `examples/04_custom_model.py` 模板创建新功能：

Based on `examples/04_custom_model.py` template to create new features:

```python
from civmodel import CivilizationModel

class SimplifiedNetworkModel(CivilizationModel):
    """简化的网络增强模型 | Simplified network-enhanced model"""
    
    def __init__(self, network_density=0.15, influence_strength=0.2, **kwargs):
        super().__init__(**kwargs)
        self.network_density = network_density
        self.influence_strength = influence_strength
        self._initialize_network()
```

**扩展验证结果** | **Extension Validation Results**:
- ✅ **网络增强**：平均提升10%创新率 | **Network enhancement**: Average 10% innovation rate improvement
- ✅ **记忆增强**：平均提升10%创新率 | **Memory enhancement**: Average 10% innovation rate improvement  
- 🎯 **简化有效**：核心机制验证比复杂指标更重要 | **Simplified effectiveness**: Core mechanism validation is more important than complex metrics

## 📚 学习理论 | Learn the Theory

深入了解理论基础 | For a deep dive into the theoretical foundations:

- **元模型理论** - 哲学和数学基础 | **The Meta-Model Theory** - Philosophical and mathematical basis
- **计算历史动力学** - 方法论 | **Computational Historical Dynamics** - Methodology
- **从性别到一般多样性** - 模型扩展 | **From Gender to General Diversity** - Model extensions
- **结构性相变理论** - 物理启发的方法 | **Structural Phase Transition Theory** - Physics-inspired approach

## 🧪 测试 | Testing

运行测试套件 | Run the test suite:

```bash
pytest tests/ -v
```

## 🤝 贡献 | Contributing

我们欢迎贡献！无论您是历史学家、计算社会科学家还是开发者，都有许多方式可以帮助：

We welcome contributions! Whether you're a historian, computational social scientist, or developer, there are many ways to help:

- **测试历史场景** - 将模型应用于不同的文明 | **Test historical scenarios** - Apply the model to different civilizations
- **改进可视化** - 创建更好的解释性图表 | **Improve visualization** - Create better explanatory graphics
- **扩展模型** - 基于`04_custom_model.py`创建新功能 | **Extend the model** - Create new features based on `04_custom_model.py`
- **参数验证** - 完善历史参数预设 | **Parameter validation** - Refine historical parameter presets
- **翻译文档** - 使框架在全球范围内更易访问 | **Translate documentation** - Make the framework accessible globally

详见贡献指南 | See our [Contributing Guidelines](docs/CONTRIBUTING.md) for details.

## 📄 引用 | Citation

如果您在研究中使用CMM，请引用 | If you use CMM in your research, please cite:

```bibtex
@software{civilization_meta_model,
  title = {Civilization Meta-Model: A Computational Framework for Civilizational Phase Transitions},
  author = {Civilization Meta-Model Contributors},
  year = {2024},
  url = {https://github.com/hedmx/Civilization-Meta-Model},
  version = {0.1.0}
}

@software{civilization_meta_model_examples,
  title = {Civilization Meta-Model Examples: Computational Historical Analysis},
  author = {Civilization Meta-Model Contributors},
  year = {2024},
  url = {https://github.com/hedmx/Civilization-Meta-Model/tree/main/examples},
  note = {Example implementations including Tang-Song case study, parameter analysis, and model extensions}
}
```

## 🔗 相关工作 | Related Work

- **Seshat全球历史数据库** - 验证用的历史数据 | **Seshat Global History Databank** - Historical data for validation
- **文化演化** - 理论基础 | **Cultural Evolution** - Theoretical foundations
- **复杂性探索者** - 教育资源 | **Complexity Explorer** - Educational resources
- **计算社会科学** - 方法论框架 | **Computational Social Science** - Methodological framework

## 📊 数据可用性 | Data Availability

模型内部生成所有数据。历史参数预设基于文献估计。

The model generates all data internally. Historical parameter presets are based on literature estimates.

**示例输出文件** | **Example Output Files**:
- `examples/tang_song_case_study.png` - 唐宋时期对比图表 | Tang-Song period comparison charts
- `examples/parameter_analysis_results.png` - 参数空间相图 | Parameter space phase diagrams
- `examples/simple_model_comparison.png` - 自定义模型性能对比 | Custom model performance comparison

## 🐛 错误报告和功能请求 | Bug Reports and Feature Requests

请使用 [GitHub Issues](https://github.com/hedmx/Civilization-Meta-Model/issues) 页面。

Please use the [GitHub Issues](https://github.com/hedmx/Civilization-Meta-Model/issues) page.

## 📞 联系方式 | Contact

- **项目主页** | **Project Homepage**: [https://github.com/hedmx/Civilization-Meta-Model](https://github.com/hedmx/Civilization-Meta-Model)
- **文档网站** | **Documentation**: [https://hedmx.github.io/Civilization-Meta-Model/](https://hedmx.github.io/Civilization-Meta-Model/)
- **讨论区** | **Discussions**: [GitHub Discussions](https://github.com/hedmx/Civilization-Meta-Model/discussions)

## 许可证 | License

MIT许可证。详见 [LICENSE](LICENSE) 文件。

MIT License. See [LICENSE](LICENSE) for details.
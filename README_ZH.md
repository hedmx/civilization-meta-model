Civilization Meta-Model (CMM) 文明元模型
用于模拟文明演化中结构性相变的计算元框架。

https://img.shields.io/badge/License-MIT-green.svg
https://img.shields.io/badge/python-3.8+-blue.svg
https://img.shields.io/badge/PRs-welcome-brightgreen.svg

🧠 核心理念
文明的跃迁不仅仅是创新的积累，而是系统"有效选择空间"非线性扩展所触发的结构性相变。本模型形式化了一个双层机制：

窗口期（必要条件）：male_explore_space 参数的扩展（代表主导社会群体的探索自由度）。

转型期（充分条件）：female_activation 参数超过临界阈值，释放被抑制的认知多样性并产生协同效应。

🚀 快速开始
bash
# 从PyPI安装（推荐）
pip install civilization-metamodel

# 或从源码安装
git clone https://github.com/YOUR_USERNAME/civilization-meta-model.git
cd civilization-meta-model
pip install -e .
用3行代码运行你的第一个模拟：

python
from civmodel import CivilizationModel

# 1. 创建一个文明
model = CivilizationModel(male_explore_space=0.8, female_activation=0.3)
# 2. 运行模拟
innovations, synergies, metadata = model.run(steps=300)
# 3. 分析结果
print(f"创新率: {metadata['innovation_rate']*100:.2f}%")
print(f"平均协同效应: {metadata['avg_synergy']:.2f}")
📈 关键发现
该模型稳健地复现了三种不同的文明阶段：

阶段	参数	预期创新率	历史类比
停滞期	male_explore_space=0.3, female_activation=0.0	< 5%	传统农业社会
窗口期	male_explore_space=0.75, female_activation=0.3	10-30%	唐宋转型、文艺复兴
转型期	male_explore_space=0.85, female_activation=0.8	> 50%	工业革命
运行相图扫描：

bash
python examples/01_basic_usage.py
🗺️ 相图与协同效应
该模型揭示了一个非线性协同效应：当女性激活度超过约0.4时，系统受益于认知多样性，显著提升创新效率。

https://docs/images/phase_diagram.png

🧩 项目结构
src/civmodel/core.py - 核心模拟引擎 (CivilizationModel)

src/civmodel/scanner.py - 参数空间扫描工具 (ParameterScanner)

src/civmodel/constants.py - 默认参数与配置 (PARAMS, HISTORICAL_PRESETS)

src/civmodel/utils/visualize.py - 可视化工具

examples/ - 教程笔记本和脚本

docs/ - 文档和理论

🔬 高级用法
历史案例研究
python
from civmodel.constants import HISTORICAL_PRESETS

# 加载唐宋转型参数
tang_song_params = HISTORICAL_PRESETS['tang_song_window']
model = CivilizationModel(**tang_song_params)
innovations, synergies, metadata = model.run(steps=500)
参数空间分析
python
from civmodel import ParameterScanner

scanner = ParameterScanner()
results = scanner.scan_2d(
    male_space_range=(0.2, 1.0),
    female_activation_range=(0.0, 1.0),
    seeds=[42, 43, 44]
)
自定义模型扩展
python
from civmodel import CivilizationModel
import numpy as np

class NetworkCivilizationModel(CivilizationModel):
    """添加智能体间的网络效应"""
    
    def __init__(self, network_density=0.1, **kwargs):
        super().__init__(**kwargs)
        self.network_density = network_density
        self._initialize_network()
    
    def _initialize_network(self):
        """创建随机交互网络"""
        self.adjacency = np.random.rand(self.N, self.N) < self.network_density
        np.fill_diagonal(self.adjacency, 0)
    
    def _agent_exploration(self, agent_idx: int) -> np.ndarray:
        """重写为具有网络意识的探索"""
        base_exploration = super()._agent_exploration(agent_idx)
        
        # 添加邻居的社会影响
        neighbors = np.where(self.adjacency[agent_idx])[0]
        if len(neighbors) > 0:
            neighbor_states = self.states[neighbors]
            social_influence = neighbor_states.mean(axis=0) - self.states[agent_idx]
            social_influence = social_influence * 0.1  # 小的影响权重
            return base_exploration + social_influence
        
        return base_exploration
📚 学习理论
深入了解理论基础：

元模型理论 - 哲学和数学基础

计算历史动力学 - 方法论

从性别到一般多样性 - 模型扩展

🧪 测试
运行测试套件：

bash
pytest tests/ -v
🤝 贡献
我们欢迎贡献！无论您是历史学家、计算社会科学家还是开发者，都有许多方式可以帮助：

测试历史场景 - 将模型应用于不同的文明

改进可视化 - 创建更好的解释性图表

扩展模型 - 添加经济、生态或网络层

翻译文档 - 使框架在全球范围内更易访问

详见贡献指南。

📄 引用
如果您在研究中使用CMM，请引用：

bibtex
@software{civilization_meta_model,
  title = {Civilization Meta-Model: A Computational Framework for Civilizational Phase Transitions},
  author = {Civilization Meta-Model Contributors},
  year = {2024},
  url = {https://github.com/YOUR_USERNAME/civilization-meta-model},
  version = {0.1.0}
}
🔗 相关工作
Seshat全球历史数据库 - 验证用的历史数据

文化演化 - 理论基础

复杂性探索者 - 教育资源

📊 数据可用性
模型内部生成所有数据。历史参数预设基于文献估计。

🐛 错误报告和功能请求
请使用GitHub Issues页面。

许可证
MIT许可证。详见LICENSE文件。
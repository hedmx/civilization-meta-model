# Civilization Meta-Model 示例目录 | Examples Directory

本目录包含使用文明元模型的各种示例。这些示例展示了如何将理论模型应用于实际历史场景和参数分析。

This directory contains various examples using the Civilization Meta-Model. These examples demonstrate how to apply the theoretical model to actual historical scenarios and parameter analysis.

## 示例列表 | Examples List

### 1. 基础示例 | Basic Examples
- **`01_basic_usage.py`** - 基础使用方法，展示三种文明阶段 | Basic usage demonstrating three civilizational phases

### 2. 历史案例研究 | Historical Case Studies
- **`02_tang_song_case_study.py`** - 唐宋转型期案例研究 | Tang-Song Transition Case Study
  - 模拟中国唐宋时期(618-1127 CE)的文明跃迁 | Simulates the civilizational leap during China's Tang-Song period (618-1127 CE)
  - 展示如何将模型参数与历史条件对应 | Shows how to map model parameters to historical conditions
  - 生成可视化图表和分析报告 | Generates visualizations and analytical reports

### 3. 参数空间分析 | Parameter Space Analysis
- **`03_parameter_analysis.py`** - 参数空间扫描与分析 | Parameter space scanning and analysis
  - 系统扫描 male_explore_space 和 female_activation 参数空间 | Systematic scanning of male_explore_space and female_activation parameter space
  - 检测相变临界点和相边界 | Detects phase transition critical points and boundaries
  - 提供敏感性分析和参数重要性评估 | Provides sensitivity analysis and parameter importance assessment
  - 生成综合性相图和统计报告 | Generates comprehensive phase diagrams and statistical reports

### 4. 模型扩展与自定义 | Model Extensions and Customization
- **`04_custom_model.py`** - 自定义模型扩展示例 | Custom model extension examples
  - **网络增强模型**：添加社会网络影响，模拟知识传播 | **Network-enhanced model**: Adds social network influence, simulates knowledge diffusion
  - **记忆增强模型**：添加经验学习机制，实现历史记忆积累 | **Memory-enhanced model**: Adds experiential learning mechanism, achieves historical memory accumulation
  - **简化设计**：验证核心机制，避免过度复杂化 | **Simplified design**: Validates core mechanisms, avoids over-complexity
  - **性能对比**：网络提升+10%，记忆提升+10%创新率 | **Performance comparison**: Network +10%, Memory +10% innovation rate improvement

## 案例研究成果 | Case Study Results

### 唐宋转型期分析 | Tang-Song Transition Analysis
通过参数化历史分析，模型成功再现了唐宋时期的创新加速现象：

Through parameterized historical analysis, the model successfully reproduces the innovation acceleration phenomenon of the Tang-Song period:

| 时期 | 模型参数 | 创新率 | 历史解释 |
|------|----------|--------|----------|
| **唐代早期** | male=0.65, female=0.35 | 15-20% | 科举制度确立，文化开放 |
| **宋代高峰** | male=0.82, female=0.48 | 25-30% | 商业革命，科技创新繁荣 |
| **绩效提升** | +0.17探索空间, +0.13激活度 | **+67%** | 制度完善与社会结构优化 |

| Period | Model Parameters | Innovation Rate | Historical Interpretation |
|--------|------------------|-----------------|---------------------------|
| **Early Tang** | male=0.65, female=0.35 | 15-20% | Imperial examination established, cultural openness |
| **Song Peak** | male=0.82, female=0.48 | 25-30% | Commercial revolution, technological innovation boom |
| **Performance Gain** | +0.17 exploration, +0.13 activation | **+67%** | Institutional refinement and social structure optimization |

### 参数空间关键发现 | Key Parameter Space Findings
1. **相变临界点**：female_activation ≈ 0.4-0.5 | **Phase transition critical point**: female_activation ≈ 0.4-0.5
2. **窗口期条件**：male_explore_space > 0.6 | **Window period condition**: male_explore_space > 0.6
3. **协同效应阈值**：女性激活度超过0.4时产生非线性提升 | **Synergy threshold**: Nonlinear boost when female_activation > 0.4

### 模型扩展验证 | Model Extension Validation
- **网络增强**：社会网络连接显著提升信息扩散效率 | **Network enhancement**: Social network connections significantly improve information diffusion efficiency
- **记忆增强**：经验学习机制减少重复探索，提升创新效率 | **Memory enhancement**: Experiential learning reduces redundant exploration, improves innovation efficiency
- **混合潜力**：网络+记忆的组合可能产生协同效应 | **Hybrid potential**: Network+Memory combination may produce synergistic effects

## 运行示例 | Running Examples

```bash
# 确保在项目根目录 | Make sure you're in the project root directory
cd /path/to/civilization_metamodel

# 运行基础示例 | Run basic example
python examples/01_basic_usage.py

# 运行唐宋案例研究 | Run Tang-Song case study
python examples/02_tang_song_case_study.py

# 运行参数空间分析 | Run parameter space analysis
python examples/03_parameter_analysis.py

# 运行自定义模型示例 | Run custom model example
python examples/04_custom_model.py
```

## 输出文件 | Output Files

运行示例将生成以下可视化文件：

Running the examples will generate the following visualization files:

| 示例 | 生成文件 | 说明 |
|------|----------|------|
| `02_tang_song_case_study.py` | `tang_song_case_study.png` | 唐宋各时期对比图表 |
| `03_parameter_analysis.py` | `parameter_analysis_results.png` | 参数空间相图与分析图表 |
| `04_custom_model.py` | `simple_model_comparison.png` | 自定义模型性能对比 |

| Example | Generated File | Description |
|---------|----------------|-------------|
| `02_tang_song_case_study.py` | `tang_song_case_study.png` | Tang-Song period comparison charts |
| `03_parameter_analysis.py` | `parameter_analysis_results.png` | Parameter space phase diagrams and analysis charts |
| `04_custom_model.py` | `simple_model_comparison.png` | Custom model performance comparison |

## 理论启示 | Theoretical Insights

1. **结构性相变**：文明跃迁是系统参数达到临界阈值的结果 | **Structural phase transitions**: Civilizational leaps result from system parameters reaching critical thresholds
2. **双重机制**：窗口期（制度开放）与转型期（群体激活）的协同作用 | **Dual mechanism**: Synergy between window period (institutional openness) and transition period (group activation)
3. **认知多样性**：被抑制社会群体的激活释放系统创新潜力 | **Cognitive diversity**: Activation of suppressed social groups releases systemic innovation potential
4. **历史动力学**：参数化建模为历史分析提供计算框架 | **Historical dynamics**: Parametric modeling provides computational framework for historical analysis

## 扩展应用 | Extended Applications

基于现有示例，您可以：

Based on the existing examples, you can:

1. **创建新的历史案例**：调整参数模拟其他文明转型期 | **Create new historical cases**: Adjust parameters to simulate other civilizational transitions
2. **探索参数敏感性**：修改扫描范围和精度获得更详细分析 | **Explore parameter sensitivity**: Modify scanning range and precision for more detailed analysis
3. **设计自定义扩展**：基于`04_custom_model.py`模板创建新功能 | **Design custom extensions**: Create new features based on `04_custom_model.py` template
4. **结合历史数据**：将实际历史数据与模型输出对比验证 | **Integrate historical data**: Compare actual historical data with model outputs for validation

## 依赖要求 | Dependencies

运行所有示例需要以下Python包：

Running all examples requires the following Python packages:

```bash
pip install numpy matplotlib scipy tqdm
```

## 引用参考 | Citation Reference

如果您在研究中使用这些示例，请引用：

If you use these examples in research, please cite:

```bibtex
@software{civilization_meta_model_examples,
  title = {Civilization Meta-Model Examples: Computational Historical Analysis},
  author = {Civilization Meta-Model Contributors},
  year = {2024},
  url = {https://github.com/hedmx/Civilization-Meta-Model/tree/main/examples},
  note = {Example implementations for civilizational phase transition modeling}
}
```
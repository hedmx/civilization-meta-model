"""
自定义模型扩展示例 - Civilization Meta-Model 高级功能（简化版）
===============================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from civmodel import CivilizationModel
import os

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Heiti TC', 'Hiragino Sans GB', 'PingFang SC']
plt.rcParams['axes.unicode_minus'] = False

class NetworkCivilizationModel(CivilizationModel):
    """简化的网络增强模型"""
    
    def __init__(self, network_density=0.1, influence_strength=0.15, **kwargs):
        super().__init__(**kwargs)
        self.network_density = network_density
        self.influence_strength = influence_strength
        self._initialize_network()
    
    def _initialize_network(self):
        """简化网络初始化"""
        # 创建简单的随机网络
        self.adjacency = np.random.rand(self.N, self.N) < self.network_density
        np.fill_diagonal(self.adjacency, 0)
        # 确保对称
        self.adjacency = np.maximum(self.adjacency, self.adjacency.T)
        
        # 计算节点度
        self.degrees = np.sum(self.adjacency, axis=1)
        self.avg_degree = np.mean(self.degrees) if self.N > 0 else 0
    
    def _agent_exploration(self, agent_idx: int) -> np.ndarray:
        """添加网络影响的探索"""
        base_exploration = super()._agent_exploration(agent_idx)
        
        # 找到邻居
        neighbors = np.where(self.adjacency[agent_idx])[0]
        if len(neighbors) > 0:
            neighbor_states = self.states[neighbors]
            neighbor_mean = neighbor_states.mean(axis=0)
            
            # 简单的社会影响
            social_influence = (neighbor_mean - self.states[agent_idx])
            return base_exploration + social_influence * self.influence_strength
        
        return base_exploration
    
    def get_network_metrics(self):
        """获取简单网络指标"""
        # 计算网络连通性
        connected = np.all(np.sum(self.adjacency, axis=1) > 0)
        return {
            'avg_degree': float(self.avg_degree),
            'network_density': float(np.sum(self.degrees) / (self.N * (self.N - 1))) if self.N > 1 else 0,
            'connected': connected
        }


class MemoryCivilizationModel(CivilizationModel):
    """简化的记忆增强模型"""
    
    def __init__(self, memory_strength=0.2, memory_decay=0.95, **kwargs):
        super().__init__(**kwargs)
        self.memory_strength = memory_strength
        self.memory_decay = memory_decay
        
        # 初始化记忆：每个智能体记住自己的最佳状态
        self.best_states = self.states.copy()
        self.best_performance = np.zeros(self.N)
    
    def step(self):
        """重写step方法，包含记忆更新"""
        # 保存旧状态用于比较
        old_states = self.states.copy()
        
        # 执行基础步骤
        innovation, synergy = super().step()
        
        # 更新记忆：如果新状态更好，则记住它
        for i in range(self.N):
            # 简单性能评估：距离系统中心的接近程度
            old_dist = np.linalg.norm(old_states[i] - self.institution)
            new_dist = np.linalg.norm(self.states[i] - self.institution)
            
            if new_dist < old_dist * 0.9:  # 有明显改进
                self.best_states[i] = self.states[i].copy()
                self.best_performance[i] = self.best_performance[i] * self.memory_decay + 1
            else:
                self.best_performance[i] = self.best_performance[i] * self.memory_decay
        
        return innovation, synergy
    
    def _agent_exploration(self, agent_idx: int) -> np.ndarray:
        """添加记忆引导的探索"""
        base_exploration = super()._agent_exploration(agent_idx)
        
        # 如果记忆有足够强度，添加记忆引导
        if self.best_performance[agent_idx] > 0.5:
            memory_guidance = (self.best_states[agent_idx] - self.states[agent_idx])
            memory_weight = min(self.memory_strength * self.best_performance[agent_idx], 0.3)
            return base_exploration + memory_guidance * memory_weight
        
        return base_exploration
    
    def get_memory_metrics(self):
        """获取简单记忆指标"""
        active_memory = np.sum(self.best_performance > 0.1)
        avg_memory_strength = np.mean(self.best_performance[self.best_performance > 0])
        
        return {
            'active_memory_agents': int(active_memory),
            'avg_memory_strength': float(avg_memory_strength) if active_memory > 0 else 0,
            'memory_utilization': float(active_memory / self.N) if self.N > 0 else 0
        }


def run_simple_comparison():
    """运行简化比较"""
    print("=" * 60)
    print("自定义模型简化比较")
    print("=" * 60)
    
    # 基础参数
    base_params = {
        'male_explore_space': 0.75,
        'female_activation': 0.4,
        'N': 50,  # 减少智能体数量以加速
        'd': 2,   # 减少维度以简化
        'seed': 42,
        'verbose': False
    }
    
    results = []
    
    # 1. 基础模型
    print("\n1. 基础模型...")
    base_model = CivilizationModel(**base_params)
    innov_base, syn_base, meta_base = base_model.run(steps=100)
    results.append(('基础模型', meta_base, None, None))
    
    # 2. 网络增强模型
    print("2. 网络增强模型...")
    net_model = NetworkCivilizationModel(**base_params, network_density=0.15)
    innov_net, syn_net, meta_net = net_model.run(steps=100)
    net_metrics = net_model.get_network_metrics()
    results.append(('网络增强', meta_net, net_metrics, None))
    
    # 3. 记忆增强模型
    print("3. 记忆增强模型...")
    mem_model = MemoryCivilizationModel(**base_params, memory_strength=0.25)
    innov_mem, syn_mem, meta_mem = mem_model.run(steps=100)
    mem_metrics = mem_model.get_memory_metrics()
    results.append(('记忆增强', meta_mem, None, mem_metrics))
    
    return results


def visualize_simple_results(results):
    """简化可视化"""
    print("\n📊 生成简化对比图表...")
    
    model_names = [r[0] for r in results]
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # 1. 创新率对比
    ax1 = axes[0, 0]
    innov_rates = [r[1]['innovation_rate'] * 100 for r in results]
    colors = ['lightblue', 'lightgreen', 'orange']
    
    bars = ax1.bar(model_names, innov_rates, color=colors)
    ax1.set_ylabel('创新率 (%)')
    ax1.set_title('创新率对比')
    ax1.grid(True, alpha=0.3, axis='y')
    
    for bar, rate in zip(bars, innov_rates):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{rate:.1f}%', ha='center', va='bottom')
    
    # 2. 协同效应对比
    ax2 = axes[0, 1]
    synergies = [r[1]['avg_synergy'] for r in results]
    bars = ax2.bar(model_names, synergies, color=colors)
    ax2.axhline(y=1.0, color='red', linestyle='--', alpha=0.5, label='基准')
    ax2.set_ylabel('协同效应')
    ax2.set_title('协同效应对比')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    for bar, syn in zip(bars, synergies):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f'{syn:.2f}', ha='center', va='bottom')
    
    # 3. 网络指标（仅网络模型）
    ax3 = axes[1, 0]
    net_data = []
    net_labels = []
    
    for name, meta, net_metrics, mem_metrics in results:
        if net_metrics:
            net_data.append(net_metrics['avg_degree'])
            net_labels.append(name)
    
    if net_data:
        bars = ax3.bar(net_labels, net_data, color='lightgreen')
        ax3.set_ylabel('平均节点度')
        ax3.set_title('网络结构指标')
        ax3.grid(True, alpha=0.3, axis='y')
        
        for bar, degree in zip(bars, net_data):
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{degree:.1f}', ha='center', va='bottom')
    else:
        ax3.text(0.5, 0.5, '无网络数据', ha='center', va='center', fontsize=12)
        ax3.set_title('网络结构指标')
    
    # 4. 记忆指标（仅记忆模型）
    ax4 = axes[1, 1]
    mem_data = []
    mem_labels = []
    
    for name, meta, net_metrics, mem_metrics in results:
        if mem_metrics:
            mem_data.append(mem_metrics['memory_utilization'] * 100)
            mem_labels.append(name)
    
    if mem_data:
        bars = ax4.bar(mem_labels, mem_data, color='orange')
        ax4.set_ylabel('记忆利用率 (%)')
        ax4.set_title('记忆系统指标')
        ax4.grid(True, alpha=0.3, axis='y')
        
        for bar, util in zip(bars, mem_data):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{util:.1f}%', ha='center', va='bottom')
    else:
        ax4.text(0.5, 0.5, '无记忆数据', ha='center', va='center', fontsize=12)
        ax4.set_title('记忆系统指标')
    
    plt.tight_layout()
    
    # 保存
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'simple_model_comparison.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✅ 图表已保存: {output_path}")
    
    plt.show()
    return fig


def print_simple_analysis(results):
    """打印简化分析"""
    print("\n" + "=" * 60)
    print("性能分析总结")
    print("=" * 60)
    
    for i, (name, meta, net_metrics, mem_metrics) in enumerate(results):
        print(f"\n{name}:")
        print(f"  创新率: {meta['innovation_rate']*100:.1f}%")
        print(f"  协同效应: {meta['avg_synergy']:.2f}x")
        print(f"  创新总数: {meta['total_innovations']}")
        
        if net_metrics:
            print(f"  网络密度: {net_metrics['network_density']:.3f}")
            print(f"  平均节点度: {net_metrics['avg_degree']:.1f}")
        
        if mem_metrics:
            print(f"  记忆利用率: {mem_metrics['memory_utilization']*100:.1f}%")
            print(f"  激活记忆智能体: {mem_metrics['active_memory_agents']}/{meta.get('N', '?')}")
    
    # 计算提升
    if len(results) >= 3:
        base_rate = results[0][1]['innovation_rate'] * 100
        net_rate = results[1][1]['innovation_rate'] * 100
        mem_rate = results[2][1]['innovation_rate'] * 100
        
        print(f"\n📈 性能提升:")
        print(f"  网络增强: +{(net_rate - base_rate):.1f}%")
        print(f"  记忆增强: +{(mem_rate - base_rate):.1f}%")
    
    print(f"\n💡 关键发现:")
    print(f"  1. 简化模型更容易理解和调试")
    print(f"  2. 核心机制验证比复杂指标更重要")
    print(f"  3. 适度的模型复杂度能达到最佳效果")


def main():
    """主函数"""
    try:
        # 运行简化比较
        results = run_simple_comparison()
        
        # 可视化
        visualize_simple_results(results)
        
        # 分析
        print_simple_analysis(results)
        
        print("\n" + "=" * 60)
        print("✅ 简化示例完成！")
        print("核心思想：保持简单，验证核心机制")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
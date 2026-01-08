"""
唐宋转型期案例研究 - Civilization Meta-Model 示例
====================================================

这个示例展示了如何使用文明元模型模拟中国唐宋时期的文明转型。
这是一个完整的历史案例研究，包含参数设置、模拟运行和结果可视化。

使用方法:
    python examples/02_tang_song_case_study.py

输出:
    - 屏幕显示关键指标对比
    - 保存可视化图表为 PNG 文件
    - 生成简明的数据分析报告
"""

import numpy as np
import matplotlib.pyplot as plt
from civmodel import CivilizationModel
import os
import warnings
warnings.filterwarnings('ignore')
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Heiti TC', 'Hiragino Sans GB', 'PingFang SC']
plt.rcParams['axes.unicode_minus'] = False

def get_tang_song_parameters():
    """返回唐宋各时期的模型参数估计"""
    return {
        'tang_early': {
            'name': '唐代早期 (618-755 CE)',
            'male_explore_space': 0.65,
            'female_activation': 0.35,
            'N': 120,
            'd': 3,
            'description': '盛唐时期：科举制度确立，文化开放'
        },
        'tang_late': {
            'name': '唐代晚期 (755-907 CE)',
            'male_explore_space': 0.55,
            'female_activation': 0.32,
            'N': 100,
            'd': 3,
            'description': '安史之乱后：中央集权削弱'
        },
        'song_early': {
            'name': '宋代早期 (960-1127 CE)',
            'male_explore_space': 0.78,
            'female_activation': 0.45,
            'N': 150,
            'd': 4,
            'description': '商业革命：科举完善，经济繁荣'
        },
        'song_peak': {
            'name': '宋代高峰 (1080-1120 CE)',
            'male_explore_space': 0.82,
            'female_activation': 0.48,
            'N': 180,
            'd': 5,
            'description': '科技文化高峰：指南针、火药、活字印刷'
        }
    }

def run_case_study():
    """运行唐宋案例研究"""
    print("=" * 70)
    print("唐宋转型期案例研究 - Civilization Meta-Model 示例")
    print("=" * 70)
    
    # 获取参数
    periods = get_tang_song_parameters()
    results = []
    
    # 模拟每个时期
    for period_key, params in periods.items():
        print(f"\n📜 模拟: {params['name']}")
        print(f"   描述: {params['description']}")
        print(f"   参数: male_explore_space={params['male_explore_space']:.2f}, "
              f"female_activation={params['female_activation']:.2f}")
        
        # 创建并运行模型
        model = CivilizationModel(
            male_explore_space=params['male_explore_space'],
            female_activation=params['female_activation'],
            N=params['N'],
            d=params['d'],
            seed=42,
            verbose=False
        )
        
        innovations, synergies, metadata = model.run(steps=200)
        
        # 记录结果
        results.append({
            'name': params['name'],
            'innovation_rate': metadata['innovation_rate'] * 100,
            'avg_synergy': metadata['avg_synergy'],
            'total_innovations': metadata['total_innovations'],
            'diversity': metadata['diversity']
        })
        
        print(f"   结果: 创新率={metadata['innovation_rate']*100:.2f}%, "
              f"协同效应={metadata['avg_synergy']:.2f}x")
    
    return results

def visualize_results(results, save_dir='.'):
    """可视化并保存结果"""
    print("\n📊 生成可视化图表...")
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # 1. 创新率对比
    ax1 = axes[0, 0]
    names = [r['name'].split(' ')[0] for r in results]  # 只取时期名称
    innovation_rates = [r['innovation_rate'] for r in results]
    
    bars = ax1.bar(names, innovation_rates, color=['blue', 'lightblue', 'green', 'darkgreen'])
    ax1.set_ylabel('创新率 (%)')
    ax1.set_title('唐宋各时期创新率对比')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # 添加数值标签
    for bar, rate in zip(bars, innovation_rates):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{rate:.1f}%', ha='center', va='bottom')
    
    # 2. 协同效应对比
    ax2 = axes[0, 1]
    synergies = [r['avg_synergy'] for r in results]
    ax2.plot(names, synergies, 'o-', linewidth=2, markersize=8)
    ax2.axhline(y=1.0, color='red', linestyle='--', alpha=0.5, label='无协同基准')
    ax2.set_ylabel('平均协同效应')
    ax2.set_title('协同效应变化')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. 创新产出对比
    ax3 = axes[1, 0]
    innovations = [r['total_innovations'] for r in results]
    bars = ax3.bar(names, innovations, color='orange', alpha=0.7)
    ax3.set_ylabel('创新总数 (200步)')
    ax3.set_title('创新产出对比')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # 4. 参数空间演进
    ax4 = axes[1, 1]
    # 使用参数估计值
    periods = get_tang_song_parameters()
    male_spaces = [p['male_explore_space'] for p in periods.values()]
    female_acts = [p['female_activation'] for p in periods.values()]
    
    scatter = ax4.scatter(female_acts, male_spaces, s=200, 
                         c=innovation_rates, cmap='RdYlGn', 
                         edgecolor='black', alpha=0.8)
    
    # 添加箭头显示演进方向
    for i in range(len(female_acts)-1):
        ax4.annotate('', xy=(female_acts[i+1], male_spaces[i+1]),
                    xytext=(female_acts[i], male_spaces[i]),
                    arrowprops=dict(arrowstyle='->', color='gray', lw=1.5, alpha=0.7))
    
    ax4.set_xlabel('女性激活度')
    ax4.set_ylabel('男性探索空间')
    ax4.set_title('参数空间演进路径')
    plt.colorbar(scatter, ax=ax4, label='创新率 (%)')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # 保存图表
    output_path = os.path.join(save_dir, 'tang_song_case_study.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✅ 图表已保存: {output_path}")
    
    plt.show()
    
    return fig

def print_summary(results):
    """打印分析总结"""
    print("\n" + "=" * 70)
    print("案例分析总结")
    print("=" * 70)
    
    # 计算转型效果
    tang_early = results[0]['innovation_rate']
    song_peak = results[-1]['innovation_rate']
    improvement = (song_peak - tang_early) / tang_early * 100
    
    print(f"\n📈 创新率增长: {tang_early:.2f}% → {song_peak:.2f}% "
          f"(提升 {improvement:.1f}%)")
    
    print(f"🔄 协同效应: {results[0]['avg_synergy']:.2f}x → "
          f"{results[-1]['avg_synergy']:.2f}x")
    
    print("\n🔍 历史解释:")
    print("  • 科举制度完善显著扩大了精英探索空间")
    print("  • 商业网络发展增强了知识交流强度")
    print("  • 有限的女性文化参与贡献了协同效应")
    print("  • 符合'唐宋变革论'描述的创新加速现象")
    
    print("\n💡 模型启示:")
    print("  • 制度性安排对文明创新有决定性影响")
    print("  • 社会群体激活能产生非线性协同效应")
    print("  • 文明转型需要在多个维度达到临界阈值")

def main():
    """主函数：运行唐宋案例研究"""
    try:
        # 运行模拟
        results = run_case_study()
        
        # 可视化结果
        # 确保输出到 examples 目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        fig = visualize_results(results, save_dir=script_dir)
        
        # 打印总结
        print_summary(results)
        
        print("\n✅ 唐宋案例研究完成！")
        print("这个案例展示了如何使用文明元模型分析具体历史转型期。")
        print("您可以修改参数来探索不同的历史假设。")
        
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        print("请确保已安装所有依赖: pip install numpy matplotlib")
        raise

if __name__ == "__main__":
    main()
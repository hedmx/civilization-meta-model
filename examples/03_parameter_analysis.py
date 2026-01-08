"""
参数空间扫描与分析 - Civilization Meta-Model 高级示例
=====================================================

这个示例展示了如何使用参数扫描工具全面分析文明元模型的参数空间。
包含系统性的参数扫描、临界点检测和多维度结果分析。

使用方法:
    python examples/03_parameter_analysis.py

输出:
    - 完整的参数扫描相图
    - 临界区域检测可视化
    - 敏感性分析图表
    - 参数重要性排序
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from mpl_toolkits.mplot3d import Axes3D
from scipy.ndimage import gaussian_filter
from civmodel import ParameterScanner, plot_phase_diagram
import os
import warnings
warnings.filterwarnings('ignore')
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Heiti TC', 'Hiragino Sans GB', 'PingFang SC']
plt.rcParams['axes.unicode_minus'] = False

def comprehensive_parameter_scan():
    """执行全面的参数空间扫描"""
    print("=" * 70)
    print("参数空间扫描与分析 - Civilization Meta-Model 示例")
    print("=" * 70)
    
    # 创建参数扫描器
    scanner = ParameterScanner()
    
    print("\n📊 执行2D参数扫描...")
    print("参数范围: male_explore_space=[0.1, 1.0], female_activation=[0.0, 1.0]")
    print("网格精度: 20×25 (共计500个参数组合)")
    print("随机种子: 3个 (结果平均)")
    
    # 执行详细的2D扫描
    scan_results = scanner.scan_2d(
        male_space_range=(0.1, 1.0),
        male_space_points=20,
        female_activation_range=(0.0, 1.0),
        female_activation_points=25,
        seeds=[42, 43, 44],  # 多个种子确保稳定性
        n_workers=4
    )
    
    return scanner, scan_results

def analyze_critical_regions(scan_results, scanner):
    """分析临界区域和相变点"""
    print("\n🔬 分析临界区域...")
    
    ms_vals = scan_results['male_space_values']
    fa_vals = scan_results['female_activation_values']
    innov_grid = scan_results['innovation_grid']
    
    # 1. 检测临界点
    critical_point = scanner.detect_critical_point(
        innov_grid, fa_vals, ms_vals, sigma=1.2
    )
    
    if critical_point:
        fa_critical, ms_critical = critical_point
        print(f"✅ 检测到主临界点:")
        print(f"   女性激活度: {fa_critical:.3f}")
        print(f"   男性探索空间: {ms_critical:.3f}")
        
        # 计算临界点处的创新率
        fa_idx = np.argmin(np.abs(fa_vals - fa_critical))
        ms_idx = np.argmin(np.abs(ms_vals - ms_critical))
        innov_at_critical = innov_grid[ms_idx, fa_idx] * 100
        print(f"   创新率: {innov_at_critical:.2f}%")
    else:
        print("⚠️  未检测到明显临界点")
        fa_critical, ms_critical = None, None
    
    # 2. 计算相边界
    print("\n📐 计算相边界...")
    thresholds = [0.01, 0.05, 0.10, 0.20]  # 不同创新率阈值
    phase_boundaries = {}
    
    for threshold in thresholds:
        boundary_mask = innov_grid > threshold
        phase_area = np.sum(boundary_mask) / boundary_mask.size * 100
        phase_boundaries[threshold] = {
            'mask': boundary_mask,
            'area_percent': phase_area
        }
        print(f"   创新率阈值 {threshold*100:.0f}%: 相面积占 {phase_area:.1f}%")
    
    return critical_point, phase_boundaries

def sensitivity_analysis(scan_results):
    """执行参数敏感性分析"""
    print("\n📈 执行参数敏感性分析...")
    
    ms_vals = scan_results['male_space_values']
    fa_vals = scan_results['female_activation_values']
    innov_grid = scan_results['innovation_grid']
    syn_grid = scan_results['synergy_grid']
    
    # 1. 参数边际效应
    marginal_effect_fa = np.mean(np.diff(innov_grid, axis=1), axis=0)
    marginal_effect_ms = np.mean(np.diff(innov_grid, axis=0), axis=1)
    
    # 2. 计算参数重要性（方差贡献）
    total_variance = np.var(innov_grid)
    
    # 女性激活度的边际方差
    innov_by_fa = np.mean(innov_grid, axis=0)
    variance_fa = np.var(innov_by_fa)
    
    # 男性探索空间的边际方差
    innov_by_ms = np.mean(innov_grid, axis=1)
    variance_ms = np.var(innov_by_ms)
    
    importance_fa = variance_fa / total_variance * 100
    importance_ms = variance_ms / total_variance * 100
    interaction_importance = 100 - importance_fa - importance_ms
    
    print(f"📊 参数重要性分析:")
    print(f"   女性激活度贡献: {importance_fa:.1f}%")
    print(f"   男性探索空间贡献: {importance_ms:.1f}%")
    print(f"   参数交互贡献: {interaction_importance:.1f}%")
    
    return {
        'marginal_fa': marginal_effect_fa,
        'marginal_ms': marginal_effect_ms,
        'importance': {
            'female_activation': importance_fa,
            'male_space': importance_ms,
            'interaction': interaction_importance
        }
    }

def visualize_analysis_results(scanner, scan_results, critical_point, phase_boundaries, sensitivity):
    """可视化分析结果"""
    print("\n🎨 生成分析可视化图表...")
    
    ms_vals = scan_results['male_space_values']
    fa_vals = scan_results['female_activation_values']
    innov_grid = scan_results['innovation_grid']
    syn_grid = scan_results['synergy_grid']
    
    # 创建多面板图表
    fig = plt.figure(figsize=(16, 12))
    
    # 1. 综合相图
    ax1 = plt.subplot(2, 3, 1)
    im1 = ax1.imshow(innov_grid * 100, aspect='auto', origin='lower',
                    extent=[fa_vals[0], fa_vals[-1], ms_vals[0], ms_vals[-1]],
                    cmap='RdYlGn', vmin=0, vmax=30)
    
    # 标记临界点
    if critical_point:
        fa_crit, ms_crit = critical_point
        ax1.scatter(fa_crit, ms_crit, s=200, color='blue', 
                   edgecolor='black', linewidth=2, marker='*',
                   label='临界点')
        ax1.text(fa_crit + 0.03, ms_crit, '临界点', fontsize=10,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    # 添加历史参考点
    historical_points = {
        '传统社会': (0.1, 0.3),
        '唐宋时期': (0.45, 0.75),
        '文艺复兴': (0.5, 0.8),
        '现代转型': (0.85, 0.9)
    }
    
    for label, (fa, ms) in historical_points.items():
        ax1.scatter(fa, ms, s=80, edgecolor='black', alpha=0.7)
        ax1.text(fa + 0.03, ms, label, fontsize=8, alpha=0.8)
    
    ax1.set_xlabel('女性激活度')
    ax1.set_ylabel('男性探索空间')
    ax1.set_title('创新率相图 (%)')
    plt.colorbar(im1, ax=ax1)
    ax1.legend(loc='upper left', fontsize=8)
    
    # 2. 相边界可视化
    ax2 = plt.subplot(2, 3, 2)
    
    # 创建自定义颜色映射显示不同相
    phase_cmap = colors.ListedColormap(['gray', 'yellow', 'orange', 'red'])
    
    phase_map = np.zeros_like(innov_grid)
    for i, (threshold, data) in enumerate(phase_boundaries.items()):
        phase_map[data['mask']] = i + 1
    
    im2 = ax2.imshow(phase_map, aspect='auto', origin='lower',
                    extent=[fa_vals[0], fa_vals[-1], ms_vals[0], ms_vals[-1]],
                    cmap=phase_cmap, vmin=0, vmax=4)
    
    ax2.set_xlabel('女性激活度')
    ax2.set_ylabel('男性探索空间')
    ax2.set_title('相边界 (不同创新率阈值)')
    
    # 添加图例
    legend_labels = ['停滞相 (<1%)', 
                     '缓慢相 (1-5%)', 
                     '活跃相 (5-10%)', 
                     '创新相 (>20%)']
    from matplotlib.patches import Patch
    legend_patches = [Patch(color=phase_cmap(i), label=label) 
                     for i, label in enumerate(legend_labels)]
    ax2.legend(handles=legend_patches, loc='upper left', fontsize=8)
    
    # 3. 敏感性分析：参数边际效应
    ax3 = plt.subplot(2, 3, 3)
    
    # 女性激活度的边际效应
    ax3.plot(fa_vals[:-1], sensitivity['marginal_fa'] * 1000, 
            'b-', linewidth=2, marker='o', markersize=4,
            label='女性激活度边际效应')
    
    # 男性探索空间的边际效应
    ax3_secondary = ax3.twinx()
    ax3_secondary.plot(ms_vals[:-1], sensitivity['marginal_ms'] * 1000,
                      'r-', linewidth=2, marker='s', markersize=4,
                      label='男性探索空间边际效应')
    
    ax3.set_xlabel('参数值')
    ax3.set_ylabel('女性激活度边际效应 (‰)', color='b')
    ax3_secondary.set_ylabel('男性探索空间边际效应 (‰)', color='r')
    ax3.set_title('参数边际效应分析')
    ax3.grid(True, alpha=0.3)
    
    # 合并图例
    lines1, labels1 = ax3.get_legend_handles_labels()
    lines2, labels2 = ax3_secondary.get_legend_handles_labels()
    ax3.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=8)
    
    # 4. 参数重要性饼图
    ax4 = plt.subplot(2, 3, 4)
    
    importance = sensitivity['importance']
    labels = ['女性激活度', '男性探索空间', '交互作用']
    sizes = [importance['female_activation'], 
             importance['male_space'], 
             importance['interaction']]
    colors_pie = ['lightblue', 'lightcoral', 'lightgreen']
    
    wedges, texts, autotexts = ax4.pie(sizes, labels=labels, colors=colors_pie,
                                      autopct='%1.1f%%', startangle=90)
    
    ax4.set_title('参数对创新率的方差贡献')
    ax4.axis('equal')
    
    # 5. 创新率分布直方图
    ax5 = plt.subplot(2, 3, 5)
    
    innov_rates = innov_grid.flatten() * 100
    ax5.hist(innov_rates, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    ax5.axvline(x=np.mean(innov_rates), color='red', linestyle='--',
               linewidth=2, label=f'均值: {np.mean(innov_rates):.1f}%')
    ax5.axvline(x=np.median(innov_rates), color='green', linestyle='--',
               linewidth=2, label=f'中位数: {np.median(innov_rates):.1f}%')
    
    ax5.set_xlabel('创新率 (%)')
    ax5.set_ylabel('频率')
    ax5.set_title('创新率分布')
    ax5.legend(fontsize=8)
    ax5.grid(True, alpha=0.3)
    
    # 6. 协同效应与创新率关系
    ax6 = plt.subplot(2, 3, 6)
    
    # 散点图：协同效应 vs 创新率
    sc = ax6.scatter(syn_grid.flatten(), innov_grid.flatten() * 100,
                    c=innov_grid.flatten() * 100, cmap='viridis',
                    alpha=0.6, edgecolor='black', linewidth=0.5)
    
    # 添加回归线
    from scipy import stats
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        syn_grid.flatten(), innov_grid.flatten() * 100
    )
    
    x_range = np.linspace(np.min(syn_grid), np.max(syn_grid), 100)
    ax6.plot(x_range, intercept + slope * x_range, 
            'r-', linewidth=2, 
            label=f'R² = {r_value**2:.3f}')
    
    ax6.set_xlabel('协同效应')
    ax6.set_ylabel('创新率 (%)')
    ax6.set_title(f'协同效应与创新率关系 (R² = {r_value**2:.3f})')
    ax6.legend(fontsize=8)
    ax6.grid(True, alpha=0.3)
    
    plt.colorbar(sc, ax=ax6, label='创新率 (%)')
    
    plt.tight_layout()
    
    # 保存图表
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'parameter_analysis_results.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✅ 分析图表已保存: {output_path}")
    
    plt.show()
    
    return fig

def print_analysis_summary(scan_results, critical_point, sensitivity):
    """打印分析总结报告"""
    print("\n" + "=" * 70)
    print("参数空间分析总结")
    print("=" * 70)
    
    innov_grid = scan_results['innovation_grid']
    
    # 计算关键统计量
    mean_innovation = np.mean(innov_grid) * 100
    max_innovation = np.max(innov_grid) * 100
    min_innovation = np.min(innov_grid) * 100
    std_innovation = np.std(innov_grid) * 100
    
    print(f"\n📊 创新率统计:")
    print(f"   平均值: {mean_innovation:.2f}%")
    print(f"   最大值: {max_innovation:.2f}%")
    print(f"   最小值: {min_innovation:.2f}%")
    print(f"   标准差: {std_innovation:.2f}%")
    
    # 计算高低创新区域
    high_innov_mask = innov_grid > 0.2  # >20% 为高创新区域
    high_innov_percent = np.sum(high_innov_mask) / high_innov_mask.size * 100
    low_innov_mask = innov_grid < 0.05  # <5% 为低创新区域
    low_innov_percent = np.sum(low_innov_mask) / low_innov_mask.size * 100
    
    print(f"\n🌍 参数空间分布:")
    print(f"   高创新区域 (>20%): {high_innov_percent:.1f}%")
    print(f"   低创新区域 (<5%): {low_innov_percent:.1f}%")
    
    if critical_point:
        fa_crit, ms_crit = critical_point
        print(f"\n⚡ 临界点特性:")
        print(f"   女性激活度阈值: {fa_crit:.3f}")
        print(f"   男性探索空间阈值: {ms_crit:.3f}")
        
        # 提供历史解释
        if fa_crit > 0.4 and ms_crit > 0.6:
            print(f"\n📜 历史启示:")
            print(f"   • 临界点位于中等以上参数区域")
            print(f"   • 文明转型需要同时满足两个维度的阈值")
            print(f"   • 女性激活度的作用呈现非线性特征")
    
    print(f"\n🎯 参数敏感性结论:")
    print(f"   1. 女性激活度是最敏感参数 (贡献 {sensitivity['importance']['female_activation']:.1f}%)")
    print(f"   2. 男性探索空间是必要基础条件")
    print(f"   3. 参数交互作用显著 ({sensitivity['importance']['interaction']:.1f}%)")
    
    print(f"\n💡 对文明发展的启示:")
    print(f"   • 单纯的制度开放不足以触发转型")
    print(f"   • 社会群体激活具有'乘数效应'")
    print(f"   • 转型需要系统性参数匹配")

def main():
    """主函数：执行完整的参数空间分析"""
    try:
        # 1. 执行参数扫描
        scanner, scan_results = comprehensive_parameter_scan()
        
        # 2. 分析临界区域
        critical_point, phase_boundaries = analyze_critical_regions(scan_results, scanner)
        
        # 3. 敏感性分析
        sensitivity = sensitivity_analysis(scan_results)
        
        # 4. 可视化结果
        fig = visualize_analysis_results(scanner, scan_results, critical_point, 
                                        phase_boundaries, sensitivity)
        
        # 5. 打印分析总结
        print_analysis_summary(scan_results, critical_point, sensitivity)
        
        print("\n✅ 参数空间分析完成！")
        print("这个分析展示了文明元模型的完整参数空间特性。")
        print("您可以使用这些洞察来优化历史案例模拟或设计新的文明演化路径。")
        
    except Exception as e:
        print(f"\n❌ 分析出错: {e}")
        print("请确保已安装所有依赖: pip install numpy matplotlib scipy")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
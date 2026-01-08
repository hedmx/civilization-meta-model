"""
Basic usage example for the Civilization Meta-Model.
"""

import numpy as np
import matplotlib.pyplot as plt
from civmodel import CivilizationModel, ParameterScanner, plot_phase_diagram

def demonstrate_basic_simulation():
    """Demonstrate basic model functionality."""
    print("=== Civilization Meta-Model - Basic Demo ===\n")
    
    # 1. Create a civilization with specific parameters
    print("1. Creating a 'Window Period' civilization...")
    window_model = CivilizationModel(
        male_explore_space=0.75,
        female_activation=0.3,
        N=100,
        d=3,
        seed=42,
        verbose=True
    )
    
    # 2. Run simulation
    print("\n2. Running simulation...")
    innovations, synergies, metadata = window_model.run(steps=300)
    
    print(f"   Innovation rate: {metadata['innovation_rate']*100:.2f}%")
    print(f"   Total innovations: {metadata['total_innovations']}")
    print(f"   Average synergy: {metadata['avg_synergy']:.3f}")
    print(f"   Cognitive diversity: {metadata['diversity']:.3f}")
    
    # 3. Create a 'Transition Period' civilization for comparison
    print("\n3. Creating a 'Transition Period' civilization...")
    transition_model = CivilizationModel(
        male_explore_space=0.85,
        female_activation=0.8,
        N=100,
        d=3,
        seed=42  # Same seed for fair comparison
    )
    
    innovations2, synergies2, metadata2 = transition_model.run(steps=300)
    
    print(f"   Innovation rate: {metadata2['innovation_rate']*100:.2f}%")
    print(f"   Total innovations: {metadata2['total_innovations']}")
    print(f"   Average synergy: {metadata2['avg_synergy']:.3f}")
    
    # 4. Compare results
    print("\n4. Comparison:")
    print(f"   Innovation rate increase: "
          f"{metadata2['innovation_rate']/metadata['innovation_rate']:.1f}x")
    print(f"   Synergy increase: "
          f"{metadata2['avg_synergy']/metadata['avg_synergy']:.1f}x")
    
    # 5. Visualize results
    print("\n5. Creating visualizations...")
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    # Innovation time series
    window = 30
    if len(innovations) >= window:
        ma1 = np.convolve(innovations.astype(float), 
                         np.ones(window)/window, mode='valid')
        ma2 = np.convolve(innovations2.astype(float), 
                         np.ones(window)/window, mode='valid')
        
        ax1 = axes[0, 0]
        ax1.plot(ma1 * 100, 'b-', label='Window Period', linewidth=2)
        ax1.plot(ma2 * 100, 'r-', label='Transition Period', linewidth=2)
        ax1.set_xlabel('Time Step')
        ax1.set_ylabel('Innovation Rate (%)')
        ax1.set_title('Innovation Dynamics Comparison')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
    
    # Synergy comparison
    ax2 = axes[0, 1]
    if len(synergies) >= window:
        syn_ma1 = np.convolve(synergies, np.ones(window)/window, mode='valid')
        syn_ma2 = np.convolve(synergies2, np.ones(window)/window, mode='valid')
        
        ax2.plot(syn_ma1, 'b-', label='Window Period', linewidth=2)
        ax2.plot(syn_ma2, 'r-', label='Transition Period', linewidth=2)
        ax2.set_xlabel('Time Step')
        ax2.set_ylabel('Synergy Multiplier')
        ax2.set_title('Synergy Dynamics Comparison')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
    
    # Innovation event distribution
    ax3 = axes[1, 0]
    innov_counts = [metadata['total_innovations'], metadata2['total_innovations']]
    labels = ['Window Period', 'Transition Period']
    colors = ['blue', 'red']
    
    bars = ax3.bar(labels, innov_counts, color=colors, alpha=0.7)
    ax3.set_ylabel('Total Innovations (300 steps)')
    ax3.set_title('Innovation Output Comparison')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar, count in zip(bars, innov_counts):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2, height + 0.5,
                f'{count}', ha='center', va='bottom')
    
    # Parameter space visualization
    ax4 = axes[1, 1]
    param_points = [(0.75, 0.3, 'Window'), (0.85, 0.8, 'Transition')]
    
    for ms, fa, label in param_points:
        ax4.scatter(fa, ms, s=200, label=label, alpha=0.7)
        ax4.text(fa + 0.02, ms, label, fontsize=10, va='center')
    
    ax4.set_xlabel('Female Activation')
    ax4.set_ylabel('Male Exploration Space')
    ax4.set_title('Parameter Space Location')
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0.2, 1.0)
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('basic_demo_results.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    print("\nVisualization saved as 'basic_demo_results.png'")
    
    return window_model, transition_model


def demonstrate_phase_diagram():
    """Demonstrate phase diagram scanning."""
    print("\n=== Phase Diagram Scanning ===")
    
    # Create scanner
    scanner = ParameterScanner()
    
    # Perform 2D scan (smaller grid for demo)
    print("Performing 2D parameter scan...")
    results = scanner.scan_2d(
        male_space_range=(0.3, 1.0),
        male_space_points=8,
        female_activation_range=(0.0, 1.0),
        female_activation_points=10,
        seeds=[42, 43],  # Fewer seeds for speed
        n_workers=2
    )
    
    # Visualize results
    print("Creating phase diagram...")
    fig = plot_phase_diagram(results)
    plt.savefig('phase_diagram.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    print("Phase diagram saved as 'phase_diagram.png'")
    
    # Analyze critical region
    critical_point = scanner.detect_critical_point(
        results['innovation_grid'],
        results['female_activation_values'],
        results['male_space_values']
    )
    
    if critical_point:
        fa_critical, ms_critical = critical_point
        print(f"\nDetected critical point:")
        print(f"  Female activation: {fa_critical:.3f}")
        print(f"  Male exploration space: {ms_critical:.3f}")
        
        # Find innovation rate at critical point
        fa_idx = np.argmin(np.abs(results['female_activation_values'] - fa_critical))
        ms_idx = np.argmin(np.abs(results['male_space_values'] - ms_critical))
        innov_at_critical = results['innovation_grid'][ms_idx, fa_idx] * 100
        
        print(f"  Innovation rate at critical point: {innov_at_critical:.2f}%")
    
    return results


if __name__ == "__main__":
    # Run basic simulation demo
    model1, model2 = demonstrate_basic_simulation()
    
    # Run phase diagram demo (comment out if takes too long)
    # scan_results = demonstrate_phase_diagram()
    
    print("\n=== Demo Complete ===")
    print("The civilization meta-model demonstrates:")
    print("1. Clear phase transitions based on parameter values")
    print("2. Synergy effects from cognitive diversity")
    print("3. Reproducible 'window period' and 'transition period' behaviors")
    print("\nExplore further by modifying parameters in the examples!")
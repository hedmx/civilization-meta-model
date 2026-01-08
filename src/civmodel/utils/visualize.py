"""
Visualization utilities for the civilization meta-model.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from mpl_toolkits.mplot3d import Axes3D
from typing import Optional, Dict, Any


def plot_phase_diagram(scan_results: Dict[str, np.ndarray],
                      figsize: tuple = (12, 10),
                      cmap_innovation: str = 'RdYlGn',
                      cmap_synergy: str = 'YlOrBr',
                      save_path: Optional[str] = None) -> plt.Figure:
    """
    Create comprehensive phase diagram visualization.
    
    Parameters
    ----------
    scan_results : dict
        Results from ParameterScanner.scan_2d()
    figsize : tuple, default=(12, 10)
        Figure size
    cmap_innovation : str, default='RdYlGn'
        Colormap for innovation rate
    cmap_synergy : str, default='YlOrBr'
        Colormap for synergy
    save_path : str, optional
        Path to save the figure
    
    Returns
    -------
    matplotlib.figure.Figure
    """
    ms_vals = scan_results['male_space_values']
    fa_vals = scan_results['female_activation_values']
    innov_grid = scan_results['innovation_grid']
    syn_grid = scan_results['synergy_grid']
    
    fig, axes = plt.subplots(2, 3, figsize=figsize)
    
    # 1. Innovation rate heatmap
    ax1 = axes[0, 0]
    im1 = ax1.imshow(innov_grid * 100, aspect='auto', origin='lower',
                    extent=[fa_vals[0], fa_vals[-1], ms_vals[0], ms_vals[-1]],
                    cmap=cmap_innovation)
    ax1.set_xlabel('Female Activation')
    ax1.set_ylabel('Male Exploration Space')
    ax1.set_title('Innovation Rate (%)')
    plt.colorbar(im1, ax=ax1)
    
    # 2. Synergy heatmap
    ax2 = axes[0, 1]
    im2 = ax2.imshow(syn_grid, aspect='auto', origin='lower',
                    extent=[fa_vals[0], fa_vals[-1], ms_vals[0], ms_vals[-1]],
                    cmap=cmap_synergy)
    ax2.set_xlabel('Female Activation')
    ax2.set_ylabel('Male Exploration Space')
    ax2.set_title('Synergy Multiplier')
    plt.colorbar(im2, ax=ax2)
    
    # 3. 3D surface plot
    ax3 = axes[0, 2]
    FA, MS = np.meshgrid(fa_vals, ms_vals)
    
    try:
        ax3.remove()
        ax3 = fig.add_subplot(2, 3, 3, projection='3d')
        surf = ax3.plot_surface(FA, MS, innov_grid * 100, cmap=cmap_innovation,
                               alpha=0.8, linewidth=0.1, antialiased=True)
        ax3.set_xlabel('Female Activation')
        ax3.set_ylabel('Male Exploration Space')
        ax3.set_zlabel('Innovation Rate (%)')
        ax3.set_title('Innovation Surface')
    except:
        ax3.axis('off')
        ax3.text(0.5, 0.5, '3D plot unavailable', ha='center', va='center')
    
    # 4. Phase transition curves
    ax4 = axes[1, 0]
    selected_indices = [0, len(ms_vals)//2, -1]
    colors_ = ['blue', 'green', 'red']
    
    for idx, ms_idx in enumerate(selected_indices):
        ms = ms_vals[ms_idx]
        innov_curve = innov_grid[ms_idx, :] * 100
        ax4.plot(fa_vals, innov_curve, color=colors_[idx],
                linewidth=2, marker='o', markersize=4,
                label=f'MS={ms:.2f}')
    
    ax4.set_xlabel('Female Activation')
    ax4.set_ylabel('Innovation Rate (%)')
    ax4.set_title('Phase Transition Curves')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    # 5. Synergy threshold effect
    ax5 = axes[1, 1]
    threshold = 0.4  # Typical synergy threshold
    synergy_active = syn_grid > 1.0
    
    # Create custom colormap for synergy activation
    cmap_syn = colors.ListedColormap(['lightgray', 'orange'])
    
    im5 = ax5.imshow(synergy_active.astype(float), aspect='auto', origin='lower',
                    extent=[fa_vals[0], fa_vals[-1], ms_vals[0], ms_vals[-1]],
                    cmap=cmap_syn, alpha=0.6)
    ax5.contour(fa_vals, ms_vals, innov_grid * 100, 
               levels=[5, 15, 25], colors=['blue', 'green', 'red'],
               linewidths=[1, 2, 3])
    ax5.set_xlabel('Female Activation')
    ax5.set_ylabel('Male Exploration Space')
    ax5.set_title('Synergy Activation & Innovation Contours')
    
    # 6. Critical region detection
    ax6 = axes[1, 2]
    
    # Detect high gradient region (approximate critical line)
    from scipy.ndimage import gaussian_gradient_magnitude
    gradient = gaussian_gradient_magnitude(innov_grid, sigma=1.0)
    
    # Normalize and threshold gradient
    gradient_norm = gradient / np.max(gradient)
    critical_region = gradient_norm > 0.5
    
    im6 = ax6.imshow(critical_region, aspect='auto', origin='lower',
                    extent=[fa_vals[0], fa_vals[-1], ms_vals[0], ms_vals[-1]],
                    cmap='Reds', alpha=0.7)
    
    # Add historical reference points
    historical_points = {
        'Stagnation': (0.1, 0.3),
        'Window Period': (0.3, 0.75),
        'Transition': (0.7, 0.85)
    }
    
    for label, (fa, ms) in historical_points.items():
        ax6.scatter(fa, ms, s=100, edgecolor='black', 
                   label=label, alpha=0.8)
    
    ax6.set_xlabel('Female Activation')
    ax6.set_ylabel('Male Exploration Space')
    ax6.set_title('Critical Region & Historical Reference')
    ax6.legend(loc='upper left', fontsize=9)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    return fig


def plot_innovation_timeseries(innovations: np.ndarray,
                              synergies: Optional[np.ndarray] = None,
                              window: int = 30,
                              figsize: tuple = (10, 6),
                              title: Optional[str] = None,
                              save_path: Optional[str] = None) -> plt.Figure:
    """
    Plot innovation time series with optional synergy overlay.
    
    Parameters
    ----------
    innovations : np.ndarray
        Boolean array of innovation events
    synergies : np.ndarray, optional
        Array of synergy values
    window : int, default=30
        Moving average window
    figsize : tuple, default=(10, 6)
        Figure size
    title : str, optional
        Plot title
    save_path : str, optional
        Path to save the figure
    
    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, ax1 = plt.subplots(figsize=figsize)
    
    # Convert boolean innovations to rate
    innovations_float = innovations.astype(float)
    
    # Calculate moving average
    if len(innovations) >= window:
        weights = np.ones(window) / window
        innovation_ma = np.convolve(innovations_float, weights, mode='valid')
        time_axis = np.arange(len(innovation_ma))
        
        ax1.plot(time_axis, innovation_ma * 100, 'b-', 
                linewidth=2, label='Innovation Rate (MA)')
        
        # Mark innovation events
        innov_indices = np.where(innovations[:len(innovation_ma)])[0]
        ax1.scatter(innov_indices, innovation_ma[innov_indices] * 100,
                   color='red', s=20, alpha=0.5, label='Innovation Events')
    else:
        ax1.plot(innovations_float * 100, 'b-', linewidth=2, 
                label='Innovation Rate')
    
    ax1.set_xlabel('Time Step')
    ax1.set_ylabel('Innovation Rate (%)', color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(bottom=0)
    
    # Plot synergy on second axis if provided
    if synergies is not None:
        ax2 = ax1.twinx()
        
        if len(synergies) >= window:
            synergy_ma = np.convolve(synergies, weights, mode='valid')
            ax2.plot(time_axis, synergy_ma, 'g--', 
                    linewidth=1.5, alpha=0.7, label='Synergy (MA)')
        else:
            ax2.plot(synergies, 'g--', linewidth=1.5, 
                    alpha=0.7, label='Synergy')
        
        ax2.set_ylabel('Synergy Multiplier', color='g')
        ax2.tick_params(axis='y', labelcolor='g')
        
        # Combine legends
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    else:
        ax1.legend(loc='upper left')
    
    if title:
        plt.title(title)
    else:
        plt.title('Innovation Dynamics Time Series')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    return fig
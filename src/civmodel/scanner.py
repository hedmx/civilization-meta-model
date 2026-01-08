"""
Parameter space scanning utilities for the civilization meta-model.
"""

import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from tqdm import tqdm
import multiprocessing as mp
from functools import partial

from .core import CivilizationModel
from .constants import PARAMS, merge_params


class ParameterScanner:
    """
    Systematic scanner of the civilization model parameter space.
    """
    
    def __init__(self, base_params: Optional[Dict[str, Any]] = None):
        """
        Initialize the parameter scanner.
        
        Parameters
        ----------
        base_params : dict, optional
            Base parameters for all simulations
        """
        self.base_params = merge_params(base_params or {})
    
    def scan_2d(self,
                male_space_range: Tuple[float, float] = (0.2, 1.0),
                male_space_points: int = 12,
                female_activation_range: Tuple[float, float] = (0.0, 1.0),
                female_activation_points: int = 15,
                seeds: Optional[List[int]] = None,
                n_workers: int = 4) -> Dict[str, np.ndarray]:
        """
        Perform 2D parameter scan over male space and female activation.
        
        Parameters
        ----------
        male_space_range : tuple, default=(0.2, 1.0)
            Range of male exploration space values
        male_space_points : int, default=12
            Number of points in male space dimension
        female_activation_range : tuple, default=(0.0, 1.0)
            Range of female activation values
        female_activation_points : int, default=15
            Number of points in female activation dimension
        seeds : list, optional
            Random seeds for averaging (uses base_params if None)
        n_workers : int, default=4
            Number of parallel workers
        
        Returns
        -------
        dict
            Dictionary containing:
            - male_space_values: 1D array of male space values
            - female_activation_values: 1D array of female activation values
            - innovation_grid: 2D array of innovation rates
            - synergy_grid: 2D array of average synergies
            - diversity_grid: 2D array of average diversities
        """
        # Generate parameter grids
        male_space_values = np.linspace(*male_space_range, male_space_points)
        female_activation_values = np.linspace(*female_activation_range, female_activation_points)
        
        if seeds is None:
            seeds = self.base_params.get("random_seeds", [42, 43, 44])
        
        # Prepare all parameter combinations
        param_combinations = []
        for i, ms in enumerate(male_space_values):
            for j, fa in enumerate(female_activation_values):
                for seed in seeds:
                    param_combinations.append({
                        'male_explore_space': ms,
                        'female_activation': fa,
                        'seed': seed,
                        'grid_position': (i, j)
                    })
        
        # Run simulations in parallel
        print(f"Scanning {len(param_combinations)} parameter combinations "
              f"with {n_workers} workers...")
        
        with mp.Pool(n_workers) as pool:
            results = list(tqdm(
                pool.imap(partial(self._run_single_simulation, base_params=self.base_params), 
                         param_combinations),
                total=len(param_combinations)
            ))
        
        # Aggregate results
        innovation_grid = np.zeros((male_space_points, female_activation_points))
        synergy_grid = np.zeros((male_space_points, female_activation_points))
        diversity_grid = np.zeros((male_space_points, female_activation_points))
        count_grid = np.zeros((male_space_points, female_activation_points))
        
        for (i, j), innovation_rate, avg_synergy, avg_diversity in results:
            innovation_grid[i, j] += innovation_rate
            synergy_grid[i, j] += avg_synergy
            diversity_grid[i, j] += avg_diversity
            count_grid[i, j] += 1
        
        # Average over seeds
        mask = count_grid > 0
        innovation_grid[mask] /= count_grid[mask]
        synergy_grid[mask] /= count_grid[mask]
        diversity_grid[mask] /= count_grid[mask]
        
        return {
            'male_space_values': male_space_values,
            'female_activation_values': female_activation_values,
            'innovation_grid': innovation_grid,
            'synergy_grid': synergy_grid,
            'diversity_grid': diversity_grid
        }
    
    def _run_single_simulation(self, params: Dict[str, Any], 
                               base_params: Dict[str, Any]) -> Tuple[Tuple[int, int], float, float, float]:
        """
        Run a single simulation for parameter scanning.
        
        Parameters
        ----------
        params : dict
            Simulation parameters
        base_params : dict
            Base parameters
        
        Returns
        -------
        tuple
            ((i, j), innovation_rate, avg_synergy, avg_diversity)
        """
        # Merge parameters
        sim_params = base_params.copy()
        sim_params.update({
            'male_explore_space': params['male_explore_space'],
            'female_activation': params['female_activation']
        })
        
        # Create and run model
        model = CivilizationModel(
            male_explore_space=params['male_explore_space'],
            female_activation=params['female_activation'],
            seed=params['seed'],
            params=sim_params
        )
        
        innovations, synergies, metadata = model.run()
        
        return (
            params['grid_position'],
            metadata['innovation_rate'],
            metadata['avg_synergy'],
            metadata['diversity']
        )
    
    def detect_critical_point(self, innovation_grid: np.ndarray, 
                              x_values: np.ndarray, 
                              y_values: np.ndarray,
                              sigma: float = 1.5) -> Optional[Tuple[float, float]]:
        """
        Detect critical point in innovation rate surface.
        
        Parameters
        ----------
        innovation_grid : np.ndarray
            2D grid of innovation rates
        x_values : np.ndarray
            X-axis values (e.g., female activation)
        y_values : np.ndarray
            Y-axis values (e.g., male space)
        sigma : float, default=1.5
            Gaussian smoothing sigma
        
        Returns
        -------
        tuple or None
            (critical_x, critical_y) if detected, None otherwise
        """
        from scipy.ndimage import gaussian_filter
        
        # Smooth the innovation surface
        smoothed = gaussian_filter(innovation_grid, sigma=sigma)
        
        # Calculate gradients
        grad_y, grad_x = np.gradient(smoothed)
        
        # Find point of maximum gradient magnitude
        grad_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        max_idx = np.unravel_index(np.argmax(grad_magnitude), grad_magnitude.shape)
        
        # Check if gradient is sufficiently large
        if grad_magnitude[max_idx] < 0.1:  # Threshold
            return None
        
        critical_x = x_values[max_idx[1]]
        critical_y = y_values[max_idx[0]]
        
        return critical_x, critical_y
    
    def calculate_phase_boundary(self, 
                                 innovation_grid: np.ndarray,
                                 threshold: float = 0.05) -> np.ndarray:
        """
        Calculate phase boundary based on innovation threshold.
        
        Parameters
        ----------
        innovation_grid : np.ndarray
            2D grid of innovation rates
        threshold : float, default=0.05
            Innovation rate threshold for phase boundary
        
        Returns
        -------
        np.ndarray
            Binary mask indicating transition region
        """
        return innovation_grid > threshold
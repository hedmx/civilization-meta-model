"""
Core simulation engine for the civilization meta-model.
"""

import numpy as np
from typing import Tuple, List, Optional, Dict, Any
from .constants import PARAMS, merge_params, validate_params


class CivilizationModel:
    """
    A computational model for simulating civilizational phase transitions.
    
    The model captures the dynamics of innovation through the interaction of
    two gender groups with differentiated exploration capabilities and 
    institutional constraints.
    """
    
    def __init__(self, 
                 male_explore_space: float = 0.5,
                 female_activation: float = 0.0,
                 N: Optional[int] = None,
                 d: Optional[int] = None,
                 seed: int = 42,
                 params: Optional[Dict[str, Any]] = None,
                 verbose: bool = False):
        """
        Initialize the civilization model.
        
        Parameters
        ----------
        male_explore_space : float, default=0.5
            Exploration space for male agents (0-1)
        female_activation : float, default=0.0
            Activation level for female agents (0-1)
        N : int, optional
            Total number of agents (half male, half female)
        d : int, optional
            Dimensionality of state space
        seed : int, default=42
            Random seed for reproducibility
        params : dict, optional
            Additional model parameters overriding defaults
        verbose : bool, default=False
            Whether to print progress information
        """
        # Merge and validate parameters
        self.base_params = merge_params(params or {})
        
        # Override with explicit parameters if provided
        if N is not None:
            self.base_params["N"] = N
        if d is not None:
            self.base_params["d"] = d
            
        self.params = self.base_params.copy()
        self.params.update({
            "male_explore_space": male_explore_space,
            "female_activation": female_activation
        })
        
        validate_params(self.params)
        
        # Set random seed
        self.seed = seed
        #np.random.seed(seed)
        self.rng = np.random.RandomState(seed)
        # Initialize model state
        self._initialize_agents()
        self._initialize_institution()
        self._initialize_history()
        
        self.verbose = verbose
        self.innovation_count = 0
        self.step_count = 0
        
        if verbose:
            print(f"Initialized CivilizationModel with N={self.N}, d={self.d}")
            print(f"  male_explore_space={male_explore_space:.2f}, "
                  f"female_activation={female_activation:.2f}")
    
    def _initialize_agents(self) -> None:
        """Initialize agent states based on gender."""
        self.N = self.params["N"]
        self.d = self.params["d"]
        
        # Gender assignment
        n_male = self.N // 2
        n_female = self.N - n_male
        self.genders = np.array(['male'] * n_male + ['female'] * n_female)
        
        # Shuffle genders for random distribution
        #np.random.shuffle(self.genders)
        
        # Initialize states with gender-based positioning
        self.states = np.zeros((self.N, self.d))
        
        male_mask = self.genders == 'male'
        female_mask = self.genders == 'female'
        
        # Male agents: centered around (-0.25, 0) with some variance
        if np.any(male_mask):
            self.states[male_mask] = self.rng.uniform(
                low=-0.5, high=0.0, 
                size=(np.sum(male_mask), self.d)
            )
        
        # Female agents: centered around (-0.6, 0) with more constraint
        if np.any(female_mask):
            self.states[female_mask] = self.rng.uniform(
                low=-0.8, high=-0.3,
                size=(np.sum(female_mask), self.d)
            )
    
    def _initialize_institution(self) -> None:
        """Initialize the institutional center."""
        # Start with weighted average (males have more influence initially)
        male_mask = self.genders == 'male'
        female_mask = self.genders == 'female'
        
        if np.any(male_mask):
            male_mean = self.states[male_mask].mean(axis=0)
        else:
            male_mean = np.zeros(self.d)
            
        if np.any(female_mask):
            female_mean = self.states[female_mask].mean(axis=0)
        else:
            female_mean = np.zeros(self.d)
        
        # Initial institution biased toward male positions
        bias = 0.7  # 70% toward male mean
        self.institution = bias * male_mean + (1 - bias) * female_mean
    
    def _initialize_history(self) -> None:
        """Initialize the history buffer for innovation detection."""
        self.history_buffer = [self.states.mean(axis=0).copy()]
        self.max_history_size = self.params.get("history_buffer_size", 5)
    
    @property
    def male_explore_space(self) -> float:
        """Get the male exploration space parameter."""
        return self.params["male_explore_space"]
    
    @property
    def female_activation(self) -> float:
        """Get the female activation parameter."""
        return self.params["female_activation"]
    
    def _agent_exploration(self, agent_idx: int) -> np.ndarray:
        """
        Compute exploration vector for a single agent.
        
        Parameters
        ----------
        agent_idx : int
            Index of the agent
            
        Returns
        -------
        np.ndarray
            Exploration vector
        """
        gender = self.genders[agent_idx]
        current_state = self.states[agent_idx]
        
        # Base random exploration
        noise_scale = self.params["exploration_strength"]
        base_noise = self.rng.randn(self.d) * noise_scale
        
        # Gender-specific modulation
        if gender == 'male':
            exploration = base_noise * self.male_explore_space
        else:  # female
            exploration = base_noise * self.female_activation
        
        # Institutional pull (toward current institution)
        pull_strength = self.params["institution_pull_strength"]
        institution_pull = (self.institution - current_state) * pull_strength
        
        # Gender-specific response to institution
        if gender == 'female':
            # Females are less responsive to institution when activated
            institution_pull = institution_pull * (1 - self.female_activation * 0.8)
        
        return exploration + institution_pull
    
    def _detect_innovation(self, new_mean_state: np.ndarray) -> bool:
        """
        Detect if the system has reached a novel state.
        
        Parameters
        ----------
        new_mean_state : np.ndarray
            New mean state of the system
            
        Returns
        -------
        bool
            True if innovation detected
        """
        if len(self.history_buffer) < 2:
            return False
        
        # Calculate distances to historical states
        distances = []
        for hist_state in self.history_buffer:
            dist = np.linalg.norm(new_mean_state - hist_state)
            distances.append(dist)
        
        min_distance = np.min(distances)
        
        # Dynamic threshold based on female activation
        base_threshold = self.params["innovation_base_threshold"]
        female_effect = 1 - self.female_activation * self.params["female_threshold_modulation"]
        threshold = base_threshold * female_effect
        
        # Ensure threshold doesn't go too low
        threshold = max(threshold, 0.01)
        
        return min_distance > threshold
    
    def _update_institution(self, new_mean_state: np.ndarray) -> None:
        """
        Update the institutional center based on system state.
        
        Parameters
        ----------
        new_mean_state : np.ndarray
            Current mean state of the system
        """
        learning_rate = self.params["institution_learning_rate"]
        self.institution = (1 - learning_rate) * self.institution + learning_rate * new_mean_state
    
    def _update_history(self, new_mean_state: np.ndarray) -> None:
        """
        Update the history buffer.
        
        Parameters
        ----------
        new_mean_state : np.ndarray
            New mean state to add to history
        """
        self.history_buffer.append(new_mean_state.copy())
        
        # Maintain buffer size
        if len(self.history_buffer) > self.max_history_size:
            self.history_buffer.pop(0)
    
    def calculate_diversity(self) -> float:
        """
        Calculate cognitive diversity between gender groups.
        
        Returns
        -------
        float
            Diversity measure (norm of difference between group means)
        """
        male_mask = self.genders == 'male'
        female_mask = self.genders == 'female'
        
        if np.sum(male_mask) == 0 or np.sum(female_mask) == 0:
            return 0.0
        
        male_mean = self.states[male_mask].mean(axis=0)
        female_mean = self.states[female_mask].mean(axis=0)
        
        return np.linalg.norm(male_mean - female_mean)
    
    def calculate_synergy(self) -> float:
        """
        Calculate synergy effect from gender diversity.
        
        Returns
        -------
        float
            Synergy multiplier (1.0 = no synergy)
        """
        if self.female_activation < self.params["synergy_female_threshold"]:
            return 1.0
        
        diversity = self.calculate_diversity()
        synergy_base = 1.0 + self.female_activation * 0.5
        diversity_effect = diversity * self.params["synergy_diversity_weight"]
        
        synergy = synergy_base + diversity_effect
        return min(synergy, self.params["synergy_upper_bound"])
    
    def step(self) -> Tuple[bool, float]:
        """
        Execute one simulation step.
        
        Returns
        -------
        tuple
            (innovation_occurred, synergy_value)
        """
        new_states = self.states.copy()
        
        # Agent exploration phase
        exploration_prob = self.params["exploration_prob"]
        for i in range(self.N):
            if self.rng.rand() < exploration_prob:
                explore_vector = self._agent_exploration(i)
                new_states[i] += explore_vector
        
        # Apply state bounds
        bounds = self.params["state_bounds"]
        new_states = np.clip(new_states, bounds[0], bounds[1])
        
        # Calculate new system state
        new_mean_state = new_states.mean(axis=0)
        
        # Innovation detection
        innovation = self._detect_innovation(new_mean_state)
        if innovation:
            self.innovation_count += 1
        
        # Update system state
        self.states = new_states
        self._update_history(new_mean_state)
        self._update_institution(new_mean_state)
        
        # Calculate synergy
        synergy = self.calculate_synergy()
        
        self.step_count += 1
        return innovation, synergy
    
    def run(self, steps: Optional[int] = None, 
            warmup: int = 50) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any]]:
        """
        Run the simulation for multiple steps.
        
        Parameters
        ----------
        steps : int, optional
            Number of steps to run (uses params["simulation_steps"] if None)
        warmup : int, default=50
            Number of initial steps to exclude from innovation rate calculation
        
        Returns
        -------
        tuple
            (innovations_array, synergy_array, metadata_dict)
        """
        if steps is None:
            steps = self.params["simulation_steps"]
        
        innovations = np.zeros(steps, dtype=bool)
        synergies = np.zeros(steps)
        
        if self.verbose:
            print(f"Running {steps} steps...")
        
        for t in range(steps):
            innov, synergy = self.step()
            innovations[t] = innov
            synergies[t] = synergy
            
            if self.verbose and (t + 1) % 100 == 0:
                print(f"  Step {t + 1}/{steps}")
        
        # Calculate statistics
        if steps > warmup:
            effective_innovations = innovations[warmup:]
            innovation_rate = np.mean(effective_innovations)
        else:
            innovation_rate = np.mean(innovations)
        
        avg_synergy = np.mean(synergies)
        
        metadata = {
            "innovation_rate": innovation_rate,
            "total_innovations": self.innovation_count,
            "avg_synergy": avg_synergy,
            "diversity": self.calculate_diversity(),
            "steps": steps,
            "warmup": warmup,
            "params": self.params.copy()
        }
        
        return innovations, synergies, metadata
    
    def get_system_state(self) -> Dict[str, Any]:
        """
        Get current system state for analysis.
        
        Returns
        -------
        dict
            System state information
        """
        male_mask = self.genders == 'male'
        female_mask = self.genders == 'female'
        
        male_states = self.states[male_mask] if np.any(male_mask) else None
        female_states = self.states[female_mask] if np.any(female_mask) else None
        
        return {
            "male_mean": male_states.mean(axis=0) if male_states is not None else None,
            "female_mean": female_states.mean(axis=0) if female_states is not None else None,
            "system_mean": self.states.mean(axis=0),
            "institution": self.institution,
            "diversity": self.calculate_diversity(),
            "synergy": self.calculate_synergy(),
            "innovation_count": self.innovation_count,
            "step_count": self.step_count
        }
"""
Unit tests for the core civilization model.
"""

import numpy as np
import pytest
from civmodel import CivilizationModel, PARAMS


class TestCivilizationModel:
    """Test cases for CivilizationModel."""
    
    def test_initialization_default(self):
        """Test model initialization with default parameters."""
        model = CivilizationModel()
        
        assert model.N == PARAMS["N"]
        assert model.d == PARAMS["d"]
        assert model.male_explore_space == 0.5
        assert model.female_activation == 0.0
        assert model.states.shape == (model.N, model.d)
        assert len(model.genders) == model.N
        
        # Check gender distribution
        n_male = np.sum(model.genders == 'male')
        n_female = np.sum(model.genders == 'female')
        assert abs(n_male - n_female) <= 1  # Allow for odd N
    
    def test_initialization_custom(self):
        """Test model initialization with custom parameters."""
        model = CivilizationModel(
            male_explore_space=0.8,
            female_activation=0.3,
            N=50,
            d=3,
            seed=123
        )
        
        assert model.male_explore_space == 0.8
        assert model.female_activation == 0.3
        assert model.N == 50
        assert model.d == 3
    
    def test_parameter_validation(self):
        """Test parameter validation."""
        # Test invalid male_explore_space
        with pytest.raises(ValueError, match="male_explore_space must be between"):
            CivilizationModel(male_explore_space=1.5)
        
        # Test invalid female_activation
        with pytest.raises(ValueError, match="female_activation must be between"):
            CivilizationModel(female_activation=-0.1)
        
        # Test invalid N
        with pytest.raises(ValueError, match="N must be positive"):
            CivilizationModel(params={"N": 0})
    
    def test_step_method(self):
        """Test that step method updates model state."""
        model = CivilizationModel(seed=42)
        initial_states = model.states.copy()
        initial_institution = model.institution.copy()
        
        innovation, synergy = model.step()
        
        # Check that state changed
        assert not np.array_equal(model.states, initial_states)
        
        # Check that institution changed
        assert not np.array_equal(model.institution, initial_institution)
        
        # Check return types
        assert isinstance(innovation, bool)
        assert isinstance(synergy, float)
        assert synergy >= 1.0  # Synergy should be at least 1.0
    
    def test_run_method(self):
        """Test that run method produces correct outputs."""
        model = CivilizationModel(seed=42)
        steps = 100
        
        innovations, synergies, metadata = model.run(steps=steps)
        
        # Check output shapes
        assert len(innovations) == steps
        assert len(synergies) == steps
        assert innovations.dtype == bool
        
        # Check metadata
        assert "innovation_rate" in metadata
        assert "total_innovations" in metadata
        assert "avg_synergy" in metadata
        assert metadata["steps"] == steps
        
        # Innovation rate should be between 0 and 1
        assert 0 <= metadata["innovation_rate"] <= 1
    
    def test_diversity_calculation(self):
        """Test cognitive diversity calculation."""
        model = CivilizationModel(seed=42)
        
        diversity = model.calculate_diversity()
        
        assert isinstance(diversity, float)
        assert diversity >= 0
        
        # With default parameters, diversity should be positive
        assert diversity > 0
    
    def test_synergy_calculation(self):
        """Test synergy calculation."""
        # Test with low female activation (no synergy)
        model_low = CivilizationModel(female_activation=0.1, seed=42)
        synergy_low = model_low.calculate_synergy()
        assert synergy_low == 1.0
        
        # Test with high female activation (should have synergy)
        model_high = CivilizationModel(female_activation=0.8, seed=42)
        synergy_high = model_high.calculate_synergy()
        assert synergy_high > 1.0
        assert synergy_high <= PARAMS["synergy_upper_bound"]
    
    def test_system_state(self):
        """Test system state retrieval."""
        model = CivilizationModel(seed=42)
        
        state = model.get_system_state()
        
        # Check required keys
        required_keys = ["male_mean", "female_mean", "system_mean", 
                        "institution", "diversity", "synergy",
                        "innovation_count", "step_count"]
        
        for key in required_keys:
            assert key in state
        
        # Check data types
        assert isinstance(state["diversity"], float)
        assert isinstance(state["synergy"], float)
        assert isinstance(state["innovation_count"], int)
        assert isinstance(state["step_count"], int)
    
    def test_reproducibility(self):
        """Test that models with same seed produce identical results."""
        model1 = CivilizationModel(seed=42)
        model2 = CivilizationModel(seed=42)
        
        # Run same number of steps
        for _ in range(10):
            model1.step()
            model2.step()
        
        # Check that states are identical
        assert np.array_equal(model1.states, model2.states)
        assert np.array_equal(model1.institution, model2.institution)
        assert model1.innovation_count == model2.innovation_count
    
    def test_innovation_detection_sensitivity(self):
        """Test that innovation detection responds to parameters."""
        # Low exploration should produce few innovations
        model_low = CivilizationModel(
            male_explore_space=0.1,
            female_activation=0.1,
            seed=42
        )
        innovations_low, _, metadata_low = model_low.run(steps=200)
        
        # High exploration should produce more innovations
        model_high = CivilizationModel(
            male_explore_space=0.9,
            female_activation=0.9,
            seed=42
        )
        innovations_high, _, metadata_high = model_high.run(steps=200)
        
        # High exploration should have higher innovation rate
        # (not guaranteed but very likely with our parameters)
        assert metadata_high["innovation_rate"] > metadata_low["innovation_rate"]
    
    def test_state_bounds(self):
        """Test that states stay within bounds."""
        model = CivilizationModel(
            params={"state_bounds": (-0.5, 0.5)},
            seed=42
        )
        
        # Run for many steps
        model.run(steps=500)
        
        # Check bounds
        assert np.all(model.states >= -0.5)
        assert np.all(model.states <= 0.5)
        
        # Institution should also be within reasonable bounds
        assert np.all(np.abs(model.institution) <= 1.0)
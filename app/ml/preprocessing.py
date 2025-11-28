"""
Data preprocessing utilities for menstrual cycle prediction.
"""

import numpy as np


def preprocess_data(cycles, seq_length):
    """
    Prepare time-series data for LSTM/GRU training.
    Creates sequences of past cycles to predict the next cycle.
    
    Args:
        cycles: List of cycle lengths
        seq_length: Desired sequence length
        
    Returns:
        Tuple of (X, y, min_val, max_val, actual_seq_length)
    """
    if len(cycles) < seq_length + 1:
        seq_length = max(3, len(cycles) - 1)
    
    # Normalize data to [0, 1] range for better training
    cycles_array = np.array(cycles, dtype=np.float32)
    min_val = cycles_array.min()
    max_val = cycles_array.max()
    
    # Avoid division by zero
    if max_val == min_val:
        normalized = np.ones_like(cycles_array) * 0.5
    else:
        normalized = (cycles_array - min_val) / (max_val - min_val)
    
    # Create sequences: [seq1, seq2, ..., seqN] -> next_value
    X, y = [], []
    for i in range(len(normalized) - seq_length):
        X.append(normalized[i:i + seq_length])
        y.append(normalized[i + seq_length])
    
    return np.array(X), np.array(y), min_val, max_val, seq_length


def denormalize(value, min_val, max_val):
    """
    Convert normalized value back to original scale.
    
    Args:
        value: Normalized value
        min_val: Minimum value from original data
        max_val: Maximum value from original data
        
    Returns:
        Denormalized value
    """
    if max_val == min_val:
        return min_val
    return value * (max_val - min_val) + min_val


def calculate_uncertainty(cycles):
    """
    Calculate prediction uncertainty based on historical variance.
    
    Args:
        cycles: List of cycle lengths
        
    Returns:
        Standard deviation as uncertainty measure
    """
    return np.std(cycles)


# ============================================================================
# Enhanced Multi-Feature Preprocessing
# ============================================================================

def preprocess_multi_feature_data(feature_matrix, seq_length):
    """
    Prepare multi-feature time-series data for LSTM training.
    
    Args:
        feature_matrix: Array of shape (n_cycles, n_features)
        seq_length: Desired sequence length
        
    Returns:
        Tuple of (X, y, min_vals, max_vals, actual_seq_length)
        - X: (n_samples, seq_length, n_features)
        - y: (n_samples,) - normalized cycle lengths
        - min_vals: Min values for each feature
        - max_vals: Max values for each feature
    """
    if len(feature_matrix) < seq_length + 1:
        seq_length = max(3, len(feature_matrix) - 1)
    
    feature_matrix = np.array(feature_matrix, dtype=np.float32)
    n_features = feature_matrix.shape[1]
    
    # Normalize each feature independently
    min_vals = feature_matrix.min(axis=0)
    max_vals = feature_matrix.max(axis=0)
    
    normalized = np.zeros_like(feature_matrix)
    for i in range(n_features):
        if max_vals[i] == min_vals[i]:
            normalized[:, i] = 0.5
        else:
            normalized[:, i] = (feature_matrix[:, i] - min_vals[i]) / (max_vals[i] - min_vals[i])
    
    # Create sequences
    X, y = [], []
    for i in range(len(normalized) - seq_length):
        X.append(normalized[i:i + seq_length])
        # Target is the cycle length (first feature) of next cycle
        y.append(normalized[i + seq_length, 0])
    
    return np.array(X), np.array(y), min_vals, max_vals, seq_length


def denormalize_multi_feature(value, min_val, max_val):
    """
    Denormalize a single feature value.
    
    Args:
        value: Normalized value
        min_val: Minimum value from original data
        max_val: Maximum value from original data
        
    Returns:
        Denormalized value
    """
    if max_val == min_val:
        return min_val
    return value * (max_val - min_val) + min_val


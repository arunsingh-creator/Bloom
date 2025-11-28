"""
Model factory for PyTorch LSTM models.
"""

from app.ml.pytorch_model import (
    PYTORCH_AVAILABLE,
    train_pytorch_model,
    predict_pytorch,
)

# Update config with framework availability
import app.config as config
config.PYTORCH_AVAILABLE = PYTORCH_AVAILABLE
config.TENSORFLOW_AVAILABLE = False


def get_framework_availability():
    """
    Get availability status of ML frameworks.
    
    Returns:
        Dictionary with framework availability
    """
    return {
        "pytorch": PYTORCH_AVAILABLE,
    }


def get_default_framework():
    """
    Get the default framework to use.
    
    Returns:
        Name of default framework
    """
    return "pytorch"


def train_model(framework, X, y):
    """
    Train a PyTorch LSTM model.
    
    Args:
        framework: Must be 'pytorch'
        X: Training sequences
        y: Target values
        
    Returns:
        Trained model
        
    Raises:
        ValueError: If framework is not 'pytorch' or PyTorch is not available
    """
    if framework != 'pytorch':
        raise ValueError(f"Only PyTorch is supported. Requested: {framework}")
    
    if not PYTORCH_AVAILABLE:
        raise ValueError("PyTorch is not available. Please install: pip install torch")
    
    return train_pytorch_model(X, y)


def predict(framework, model, last_sequence):
    """
    Make a prediction using PyTorch model.
    
    Args:
        framework: Must be 'pytorch'
        model: Trained PyTorch model
        last_sequence: Last sequence of normalized values
        
    Returns:
        Predicted normalized value
        
    Raises:
        ValueError: If framework is not 'pytorch' or PyTorch is not available
    """
    if framework != 'pytorch':
        raise ValueError(f"Only PyTorch is supported. Requested: {framework}")
    
    if not PYTORCH_AVAILABLE:
        raise ValueError("PyTorch is not available. Please install: pip install torch")
    
    return predict_pytorch(model, last_sequence)

"""
Enhanced PyTorch LSTM implementation for multi-feature menstrual cycle prediction.
"""

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    import numpy as np
    
    class EnhancedCycleLSTM(nn.Module):
        """Enhanced LSTM model for multi-feature cycle prediction."""
        
        def __init__(self, input_size=11, hidden_size=64, num_layers=2, dropout=0.2):
            super(EnhancedCycleLSTM, self).__init__()
            self.hidden_size = hidden_size
            self.num_layers = num_layers
            
            # LSTM layers with dropout
            self.lstm = nn.LSTM(
                input_size, 
                hidden_size, 
                num_layers, 
                batch_first=True,
                dropout=dropout if num_layers > 1 else 0
            )
            
            # Fully connected layers
            self.fc1 = nn.Linear(hidden_size, 32)
            self.relu = nn.ReLU()
            self.dropout = nn.Dropout(dropout)
            self.fc2 = nn.Linear(32, 1)
        
        def forward(self, x):
            # Initialize hidden states
            h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
            c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
            
            # LSTM forward pass
            out, _ = self.lstm(x, (h0, c0))
            
            # Take the last output
            out = out[:, -1, :]
            
            # Fully connected layers
            out = self.fc1(out)
            out = self.relu(out)
            out = self.dropout(out)
            out = self.fc2(out)
            
            return out
    
    
    def train_enhanced_pytorch_model(X, y, epochs=100):
        """
        Train enhanced PyTorch LSTM model with multi-feature input.
        
        Args:
            X: Training sequences (n_samples, sequence_length, n_features)
            y: Target values (n_samples,)
            epochs: Number of training epochs
            
        Returns:
            Trained model
        """
        # Convert to tensors
        X_tensor = torch.FloatTensor(X)
        y_tensor = torch.FloatTensor(y).unsqueeze(-1)
        
        # Initialize model
        input_size = X.shape[2] if len(X.shape) > 2 else 1
        model = EnhancedCycleLSTM(input_size=input_size, hidden_size=64, num_layers=2, dropout=0.2)
        
        # Loss and optimizer
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        
        # Training loop
        model.train()
        for epoch in range(epochs):
            optimizer.zero_grad()
            outputs = model(X_tensor)
            loss = criterion(outputs, y_tensor)
            loss.backward()
            optimizer.step()
            
            # Optional: Print progress every 20 epochs
            if (epoch + 1) % 20 == 0:
                print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')
        
        return model
    
    
    def predict_enhanced_pytorch(model, last_sequence):
        """
        Make prediction using trained enhanced PyTorch model.
        
        Args:
            model: Trained PyTorch model
            last_sequence: Last sequence of normalized features (sequence_length, n_features)
            
        Returns:
            Predicted normalized value
        """
        model.eval()
        with torch.no_grad():
            # Ensure correct shape: (1, sequence_length, n_features)
            if len(last_sequence.shape) == 2:
                last_seq_tensor = torch.FloatTensor(last_sequence).unsqueeze(0)
            else:
                last_seq_tensor = torch.FloatTensor(last_sequence).unsqueeze(0).unsqueeze(-1)
            
            prediction = model(last_seq_tensor)
            return prediction.item()
    
    ENHANCED_PYTORCH_AVAILABLE = True
    
except ImportError:
    ENHANCED_PYTORCH_AVAILABLE = False
    EnhancedCycleLSTM = None
    train_enhanced_pytorch_model = None
    predict_enhanced_pytorch = None


# Keep original simple model for backward compatibility
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    
    class CycleLSTM(nn.Module):
        """LSTM model for cycle length prediction."""
        
        def __init__(self, input_size=1, hidden_size=64, num_layers=2):
            super(CycleLSTM, self).__init__()
            self.hidden_size = hidden_size
            self.num_layers = num_layers
            self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
            self.fc = nn.Linear(hidden_size, 1)
        
        def forward(self, x):
            h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
            c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
            out, _ = self.lstm(x, (h0, c0))
            out = self.fc(out[:, -1, :])
            return out
    
    
    def train_pytorch_model(X, y):
        """
        Train PyTorch LSTM model.
        
        Args:
            X: Training sequences
            y: Target values
            
        Returns:
            Trained model
        """
        X_tensor = torch.FloatTensor(X).unsqueeze(-1)
        y_tensor = torch.FloatTensor(y).unsqueeze(-1)
        
        model = CycleLSTM(input_size=1, hidden_size=32, num_layers=1)
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=0.01)
        
        model.train()
        for epoch in range(50):
            optimizer.zero_grad()
            outputs = model(X_tensor)
            loss = criterion(outputs, y_tensor)
            loss.backward()
            optimizer.step()
        
        return model
    
    
    def predict_pytorch(model, last_sequence):
        """
        Make prediction using trained PyTorch model.
        
        Args:
            model: Trained PyTorch model
            last_sequence: Last sequence of normalized cycle lengths
            
        Returns:
            Predicted normalized value
        """
        model.eval()
        with torch.no_grad():
            last_seq_tensor = torch.FloatTensor(last_sequence).unsqueeze(0).unsqueeze(-1)
            prediction = model(last_seq_tensor)
            return prediction.item()
    
    PYTORCH_AVAILABLE = True
    
except ImportError:
    PYTORCH_AVAILABLE = False
    CycleLSTM = None
    train_pytorch_model = None
    predict_pytorch = None

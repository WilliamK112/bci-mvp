import numpy as np
from scipy.linalg import fractional_matrix_power

class CORAL:
    """
    Correlation Alignment (CORAL) for Domain Adaptation.
    Aligns the second-order statistics (covariance) of source and target domains.
    """
    def __init__(self):
        self.cov_source_inv_half = None
        self.cov_target_half = None

    def fit(self, X_source, X_target):
        # Add small regularization to avoid singular matrices
        epsilon = 1e-5
        d = X_source.shape[1]
        
        Cs = np.cov(X_source, rowvar=False) + np.eye(d) * epsilon
        Ct = np.cov(X_target, rowvar=False) + np.eye(d) * epsilon
        
        self.cov_source_inv_half = fractional_matrix_power(Cs, -0.5)
        self.cov_target_half = fractional_matrix_power(Ct, 0.5)
        
        # Ensure matrices are real
        self.cov_source_inv_half = np.real(self.cov_source_inv_half)
        self.cov_target_half = np.real(self.cov_target_half)
        return self

    def transform(self, X):
        """Transforms source features to target domain."""
        if self.cov_source_inv_half is None:
            raise ValueError("CORAL not fitted.")
        return np.dot(np.dot(X, self.cov_source_inv_half), self.cov_target_half)

    def fit_transform(self, X_source, X_target):
        self.fit(X_source, X_target)
        return self.transform(X_source)

import unittest
import numpy as np
from src.domain_adaptation import CORAL

class TestDomainAdaptation(unittest.TestCase):
    def test_coral_alignment(self):
        # Generate dummy source and target data with different covariances
        np.random.seed(42)
        X_source = np.random.randn(100, 5) * 1.5 + 2.0
        
        # Apply a linear transformation to create domain shift
        A = np.random.randn(5, 5)
        X_target = np.dot(X_source, A) + 5.0
        
        # Compute covariances before alignment
        Cs_before = np.cov(X_source, rowvar=False)
        Ct_before = np.cov(X_target, rowvar=False)
        
        # They should be substantially different
        diff_before = np.linalg.norm(Cs_before - Ct_before)
        self.assertGreater(diff_before, 5.0, "Source and Target should start with different covariances")
        
        # Apply CORAL
        coral = CORAL()
        X_source_aligned = coral.fit_transform(X_source, X_target)
        
        # Compute covariance after alignment
        Cs_after = np.cov(X_source_aligned, rowvar=False)
        
        # The new covariance of the aligned source should match the target covariance
        diff_after = np.linalg.norm(Cs_after - Ct_before)
        
        self.assertLess(diff_after, 0.1, "Aligned source covariance should closely match target covariance")

if __name__ == "__main__":
    unittest.main()

import math

class TwoPoisson:
    def __init__(self, k=1.2):
        
        self.k = k

    def calculate_score(self, tf, N, Nt):
        
        if tf == 0 or Nt == 0:
            return 0.0
            
    
        wt = math.log10((0.5 * N) / Nt)
        
        
        tf_factor = (tf * (self.k + 1.0)) / (tf + self.k)
        
        
        return tf_factor * wt

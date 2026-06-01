import math

class TwoPoisson:
    def __init__(self, max_iter=10):
        self.max_iter = max_iter

    def estimate_parameters(self, tf_list):
        # Estimasi parameter lambda_1 (elite), lambda_2 (non-elite), dan pi (peluang elite)
        N = len(tf_list)
        if N == 0: return 1.5, 0.1, 0.5
        
        total_tf = sum(tf_list)
        if total_tf == 0: return 0.1, 0.01, 0.1
            
        # Inisialisasi 
        mean_tf = total_tf / N
        lambda_1 = mean_tf + 1.0            
        lambda_2 = max(0.01, mean_tf * 0.2) 
        pi = 0.2                            
        
        def poisson_pmf(x, lam):
            if lam <= 0: return 1.0 if x == 0 else 0.0
            try:
                log_factorial = sum(math.log(i) for i in range(1, x + 1))
                return math.exp(-lam + x * math.log(lam) - log_factorial)
            except (ValueError, OverflowError):
                return 0.0

        # Algoritma Expectation-Maximization 
        for _ in range(self.max_iter):
            gamma = []
            
            # E-Step
            for x in tf_list:
                p_elite = pi * poisson_pmf(x, lambda_1)
                p_non_elite = (1 - pi) * poisson_pmf(x, lambda_2)
                denom = p_elite + p_non_elite
                gamma.append(pi if denom == 0 else p_elite / denom)
            
            # M-Step
            sum_gamma = sum(gamma)
            if sum_gamma == 0 or sum_gamma == N: break
                
            pi = sum_gamma / N
            lambda_1 = sum(g * x for g, x in zip(gamma, tf_list)) / sum_gamma
            lambda_2 = sum((1 - g) * x for g, x in zip(gamma, tf_list)) / (N - sum_gamma)
            
            # lambda_1 frekuensi lebih tinggi
            if lambda_1 < lambda_2:
                lambda_1, lambda_2 = lambda_2, lambda_1
                pi = 1 - pi

        return lambda_1, lambda_2, pi

    def calculate_score(self, tf, lambda_1, N, Nt):
        if tf == 0 or Nt == 0: return 0.0
            
        # Bobot wt (Tanpa Relevance Judgement)
        wt = math.log10((0.5 * N) / Nt)
        
        # Mencari k lambda_1, ( dibatasi 1 <= k < 2 )
        k = max(1.0, min(1.99, lambda_1))
        
        # Rumus skor utama Two Poisson (Sesuai Slide 46 & 58)
        tf_factor = (tf * (k + 1.0)) / (tf + k)
        
        return tf_factor * wt
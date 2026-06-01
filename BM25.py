import math

class BM25:
    def __init__(self, k1=1.5, b=0.75):# Parameter 
        self.k1 = k1
        self.b = b

    def calculate_score(self, tf, N, Nt, dl, avgdl):
        if tf == 0:
            return 0.0
            
        # IDF standar Okapi BM25 (log10)
        idf = math.log10((N - Nt + 0.5) / (Nt + 0.5))
        if idf < 0: 
            idf = 0.0001 #  agar peringkat tidak rusak
            
        # Normalisasi panjang dokumen 
        denom = tf + self.k1 * (1.0 - self.b + self.b * (dl / avgdl))
        num = tf * (self.k1 + 1.0)
        
        return idf * (num / denom)
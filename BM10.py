import math

class BM10:
    def __init__(self, k1=1.5):
        # Parameter BM10 hanya k1 untuk mengontrol saturasi TF.
        # Tidak menggunakan b karena tidak ada normalisasi panjang dokumen.
        self.k1 = k1

    def calculate_score(self, tf, N, Nt):
        if tf == 0 or Nt == 0:
            return 0.0
            
        # Perhitungan IDF yang konsisten dengan BM25 agar perbandingan adil
        idf = math.log10((N - Nt + 0.5) / (Nt + 0.5))
        if idf < 0: 
            idf = 0.0001 # Penyesuaian penanganan nilai negatif
            
        # Formula BM10: saturasi TF murni tanpa pengaruh panjang dokumen (b=0)
        num = tf * (self.k1 + 1.0)
        denom = tf + self.k1
        
        return idf * (num / denom)
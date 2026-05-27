import math

class BIM:
    def __init__(self):
        pass

    def calculate_ut(self):
        return 0.5
    
    def calculate_pt(self, N, Nt):
        return N / Nt
    
    def calculate_RSVt(self, ut, pt):
        return math.log(ut * pt, 10)
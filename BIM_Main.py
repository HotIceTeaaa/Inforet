from Utils import Utils
from BIM import BIM
from porterStemmer import PorterStemmer
from collections import defaultdict
from BM25 import BM25
from TwoPoisson import TwoPoisson
from BM10 import BM10  


class IREvaluator:
    @staticmethod
    def calculate_metrics(ranked_docs, ground_truth, k_values=[3, 5, 10]):
        if not ground_truth:
            return {
                "precision": 0.0, "recall": 0.0,
                "p_at_k": {k: 0.0 for k in k_values},
                "eleven_point": [0.0] * 11
            }
        
        retrieved_set = ranked_docs
        relevant_set = set(ground_truth)
        
        # 1. Hitung Precision & Recall Total
        intersection = [doc for doc in retrieved_set if doc in relevant_set]
        precision = len(intersection) / len(retrieved_set) if retrieved_set else 0.0
        recall = len(intersection) / len(relevant_set) if relevant_set else 0.0
        
        # 2. Hitung Precision @ K
        p_at_k = {}
        for k in k_values:
            top_k = ranked_docs[:k]
            intersection_k = [doc for doc in top_k if doc in relevant_set]
            p_at_k[k] = len(intersection_k) / k if k > 0 else 0.0
            
        # 3. Hitung 11-Point Interpolated Average Precision
        precisions = []
        recalls = []
        hits = 0
        for i, doc in enumerate(ranked_docs):
            if doc in relevant_set:
                hits += 1
                precisions.append(hits / (i + 1))
                recalls.append(hits / len(relevant_set))
        
        eleven_points = []
        standard_recalls = [x / 10.0 for x in range(11)]
        
        for r in standard_recalls:
            suffix_precisions = [p for p, rec in zip(precisions, recalls) if rec >= r]
            if suffix_precisions:
                eleven_points.append(max(suffix_precisions))
            else:
                eleven_points.append(0.0)
                
        return {
            "precision": precision,
            "recall": recall,
            "p_at_k": p_at_k,
            "eleven_point": eleven_points
        }

class BIM_Main:
    def __init__(self):
        self.BIM = BIM()
        self.ps = PorterStemmer()
        self.utils = Utils()
        self.invertedIndex = self.utils.makeInvertedIndex()
        self.bm25 = BM25(k1=1.5, b=0.75)
        self.two_poisson = TwoPoisson(k=1.2)
        self.bm10 = BM10(k1=1.5)  

    def get_relevance_judgment(self, query):
        matrix = {
            "box": [12, 46],
            "computer": [13, 15, 23, 31, 47, 48, 58, 63, 84, 85, 91, 92],
            "compute": [13, 15, 23, 31, 47, 48, 58, 63, 84, 85, 91, 92],
            "boundary": [15, 23, 48, 58, 72]
        }
        return matrix.get(query.lower().strip(), [])

    def main(self):
        while(True):
            query = self.getQuery()
            if not query:
                continue
                
            query_tokens = self.utils.tokenize(query)
            query_stems = self.ps.stem(query_tokens)
            query_posting_lists = self.get_query_posting_lists(query_stems)
            
            # Hitung skor untuk semua model
            rel_bim = self.build_relDQ(query_posting_lists)
            rel_bm25 = self.build_relDQ_BM25(query_posting_lists, query_stems)
            rel_tp = self.build_relDQ_TwoPoisson(query_posting_lists, query_stems)
            rel_bm10 = self.build_relDQ_BM10(query_posting_lists, query_stems)  
    
            # Ranking dokumen
            ranked_bim = self.rank_rel(rel_bim)
            ranked_bm25 = self.rank_rel(rel_bm25)
            ranked_tp = self.rank_rel(rel_tp)
            ranked_bm10 = self.rank_rel(rel_bm10)  
            
            # Tampilkan perbandingan ranking dan evaluasi metrik Tugas 3
            self.print_comparison_output(query, ranked_bim, ranked_tp, ranked_bm25, ranked_bm10)
        
    def getQuery(self):
        str_input = input("Enter Query: ")
        str_input = str_input.strip()
        return str_input

    def get_query_posting_lists(self, query_stems):
        res = []
        for query_stem in query_stems:
            posting = self.invertedIndex.get(query_stem)
            if posting is None:
                res.append([]) 
            else:
                res.append(list(posting))
        return res
    
    def build_relDQ(self, query_posting_lists):
        rel = defaultdict(float)
        N = self.utils.get_N()
        for query_posting_list in query_posting_lists:
            if not query_posting_list: continue
            Nt = self.utils.get_Nt(query_posting_list)
            for d in query_posting_list:
                ut = self.BIM.calculate_ut()
                pt = self.BIM.calculate_pt(N, Nt)
                RSVt = self.BIM.calculate_RSVt(ut, pt)
                rel[d] += RSVt
        return rel
    
    def build_relDQ_BM25(self, query_posting_lists, query_stems):
        rel = defaultdict(float)
        N = self.utils.get_N()
        avgdl = self.utils.get_avg_document_length()

        for stem, posting_list in zip(query_stems, query_posting_lists):
            if not posting_list: 
                continue
            Nt = self.utils.get_Nt(posting_list)
            for d in posting_list:
                tf = self.utils.get_tf(stem, d)
                dl = self.utils.get_document_length(d)
                score = self.bm25.calculate_score(tf, N, Nt, dl, avgdl)
                rel[d] += score
        return rel

    def build_relDQ_TwoPoisson(self, query_posting_lists, query_stems):
        rel = defaultdict(float)
        N = self.utils.get_N()

        for stem, posting_list in zip(query_stems, query_posting_lists):
            if not posting_list: 
                continue
            Nt = self.utils.get_Nt(posting_list)
            for d in posting_list:
                tf = self.utils.get_tf(stem, d)
                score = self.two_poisson.calculate_score(tf, N, Nt)
                rel[d] += score
        return rel

    def build_relDQ_BM10(self, query_posting_lists, query_stems):
        rel = defaultdict(float)
        N = self.utils.get_N()

        for stem, posting_list in zip(query_stems, query_posting_lists):
            if not posting_list: continue
            Nt = self.utils.get_Nt(posting_list)
            for d in posting_list:
                tf = self.utils.get_tf(stem, d)
                score = self.bm10.calculate_score(tf, N, Nt)
                rel[d] += score
        return rel
    
    def rank_rel(self, rel):
        return sorted(rel, key=rel.get, reverse=True)
    
    def print_comparison_output(self, query, ranked_bim, ranked_tp, ranked_bm25, ranked_bm10):
        ground_truth = self.get_ground_truth_for_query = self.get_relevance_judgment(query)
        
        print("\n" + "="*100)
        print(f"HASIL EVALUASI PERBANDINGAN MODEL UNTUK QUERY: '{query}'")
        print("="*100)
        print(f"Ground Truth (Dokumen Sebenarnya Relevan): {ground_truth}")
        print("-"*100)
        
        # Cetak Ranking Top 10
        print(f"1. BIM Peringkat Dokumen          : {ranked_bim[:10]}")
        print(f"2. Two-Poisson Peringkat Dokumen  : {ranked_tp[:10]}")
        print(f"3. BM25 Peringkat Dokumen         : {ranked_bm25[:10]}")
        print(f"4. BM10 Peringkat Dokumen         : {ranked_bm10[:10]}")
        print("-"*100)
        
        # Hitung Metrik Menggunakan IREvaluator
        metrics_bim = IREvaluator.calculate_metrics(ranked_bim, ground_truth)
        metrics_tp = IREvaluator.calculate_metrics(ranked_tp, ground_truth)
        metrics_bm25 = IREvaluator.calculate_metrics(ranked_bm25, ground_truth)
        metrics_bm10 = IREvaluator.calculate_metrics(ranked_bm10, ground_truth)
        
        # Tampilkan Tabel Evaluasi
        print(f"{'METRIK EVALUASI':<25} | {'BIM':<12} | {'Two-Poisson':<12} | {'BM25':<12} | {'BM10':<12}")
        print("-"*100)
        print(f"{'Precision (Total)':<25} | {metrics_bim['precision']:<12.4f} | {metrics_tp['precision']:<12.4f} | {metrics_bm25['precision']:<12.4f} | {metrics_bm10['precision']:<12.4f}")
        print(f"{'Recall (Total)':<25} | {metrics_bim['recall']:<12.4f} | {metrics_tp['recall']:<12.4f} | {metrics_bm25['recall']:<12.4f} | {metrics_bm10['recall']:<12.4f}")
        print(f"{'Precision @3':<25} | {metrics_bim['p_at_k'][3]:<12.4f} | {metrics_tp['p_at_k'][3]:<12.4f} | {metrics_bm25['p_at_k'][3]:<12.4f} | {metrics_bm10['p_at_k'][3]:<12.4f}")
        print(f"{'Precision @5':<25} | {metrics_bim['p_at_k'][5]:<12.4f} | {metrics_tp['p_at_k'][5]:<12.4f} | {metrics_bm25['p_at_k'][5]:<12.4f} | {metrics_bm10['p_at_k'][5]:<12.4f}")
        print(f"{'Precision @10':<25} | {metrics_bim['p_at_k'][10]:<12.4f} | {metrics_tp['p_at_k'][10]:<12.4f} | {metrics_bm25['p_at_k'][10]:<12.4f} | {metrics_bm10['p_at_k'][10]:<12.4f}")
        print("-"*100)
        
        print("\n11-POINT INTERPOLATED AVERAGE PRECISION:")
        print(f"Recall Levels : [0.0,    0.1,    0.2,    0.3,    0.4,    0.5,    0.6,    0.7,    0.8,    0.9,    1.0]")
        print(f"BIM           : {[round(x,3) for x in metrics_bim['eleven_point']]}")
        print(f"Two-Poisson   : {[round(x,3) for x in metrics_tp['eleven_point']]}")
        print(f"BM25          : {[round(x,3) for x in metrics_bm25['eleven_point']]}")
        print(f"BM10          : {[round(x,3) for x in metrics_bm10['eleven_point']]}")
        print("="*100 + "\n")

if __name__ == "__main__":
    mainClass = BIM_Main()
    mainClass.main()
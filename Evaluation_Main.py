from Utils import Utils
from BIM import BIM
from porterStemmer import PorterStemmer
from collections import defaultdict
from BM25 import BM25
from TwoPoisson import TwoPoisson
from BM10 import BM10  

class IREvaluator:
    def __init__(self):
        self.qrels = self.load_qrels()

    def load_qrels(self):
        relevance_data = {}

        with open("cleanedQrel.txt", 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]

            for i in range(0, len(lines), 2):
                title = lines[i]
                vals_str = lines[i+1]

                vals = [int(v) for v in vals_str.split()] if vals_str else []
                relevance_data[title] = vals

        return relevance_data

    def calculate_metrics(self, retrieved_docs, query, top_k=10):
        query = str(query)
        relevant_docs = self.qrels.get(query, [])
        
        # Jika query tidak ada di qrels, kembalikan nilai 0
        if not relevant_docs:
            return {
                'precision': 0.0, 'recall': 0.0, 
                'p_at_k': {3: 0.0, 5: 0.0, 10: 0.0}, 
                'eleven_point': [0.0] * 11
            }

        retrieved_k = retrieved_docs[:top_k] 
        relevant_set = set(relevant_docs)

        # 1. Hitung Precision & Recall Total (di Top K)
        true_positives = [doc for doc in retrieved_k if doc in relevant_set]
        tp_count = len(true_positives)

        precision = tp_count / len(retrieved_k) if retrieved_k else 0.0
        recall = tp_count / len(relevant_set) if relevant_set else 0.0

        # 2. Hitung Precision at K (P@3, P@5, P@10)
        p_at_k = {}
        for k in [3, 5, 10]:
            ret_k = retrieved_docs[:k]
            tp_k = len([d for d in ret_k if d in relevant_set])
            p_at_k[k] = tp_k / k if k > 0 else 0.0

        # 3. Hitung 11-Point Interpolated Average Precision
        precisions_at_recall = []
        tp_so_far = 0
        
        for i, doc in enumerate(retrieved_docs):
            if doc in relevant_set:
                tp_so_far += 1
                current_precision = tp_so_far / (i + 1)
                current_recall = tp_so_far / len(relevant_set)
                precisions_at_recall.append((current_recall, current_precision))

        eleven_points = []
        for r_target in [x / 10.0 for x in range(11)]:
            max_p = 0.0
            for r, p in precisions_at_recall:
                if r >= r_target and p > max_p:
                    max_p = p
            eleven_points.append(round(max_p, 4))

        return {
            'precision': round(precision, 4),
            'recall': round(recall, 4),
            'p_at_k': p_at_k,
            'eleven_point': eleven_points
        }

class Main:
    def __init__(self):
        self.ps = PorterStemmer()
        self.utils = Utils()
        self.invertedIndex = self.utils.makeInvertedIndex()

        self.BIM = BIM()
        self.bm25 = BM25(k1=1.5, b=0.75)
        self.two_poisson = TwoPoisson(k=1.2)
        self.bm10 = BM10(k1=1.5)  

        self.evaluator = IREvaluator()

    def main(self):
        while True:
            query = self.getQuery()
            if not query:
                continue
            if query.lower() == 'exit':
                print("Exiting program...")
                break
                
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
            
            # Tampilkan perbandingan ranking dan evaluasi metrik
            self.print_comparison_output(query, ranked_bim, ranked_tp, ranked_bm25, ranked_bm10)
        
    def getQuery(self):
        return input("Enter Query (ketik 'exit' untuk keluar): ").strip()

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
        # Ambil ground truth dinamis dari file qrels
        ground_truth = self.evaluator.qrels.get(query.lower(), [])
        
        print("\n" + "="*100)
        print(f"HASIL EVALUASI PERBANDINGAN MODEL UNTUK QUERY: '{query}'")
        print("="*100)
        print(f"Ground Truth (Dokumen Sebenarnya Relevan): {ground_truth}")
        print("-"*100)
        
        # Cetak Ranking Top 10
        print(f"1. BIM Peringkat Dokumen          : {ranked_bim[:10]}")
        print(f"2. Two-Poisson Peringkat Dokumen  : {ranked_tp[:10]}")
        print(f"4. BM10 Peringkat Dokumen         : {ranked_bm10[:10]}")
        print(f"3. BM25 Peringkat Dokumen         : {ranked_bm25[:10]}")
        print("-"*100)
        
        # Hitung Metrik menggunakan instance evaluator
        metrics_bim = self.evaluator.calculate_metrics(ranked_bim, query)
        metrics_tp = self.evaluator.calculate_metrics(ranked_tp, query)
        metrics_bm25 = self.evaluator.calculate_metrics(ranked_bm25, query)
        metrics_bm10 = self.evaluator.calculate_metrics(ranked_bm10, query)
        
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
        print(f"Recall Levels : [0.0,   0.1,   0.2,   0.3,   0.4,   0.5,   0.6,   0.7,   0.8,   0.9,   1.0]")
        print(f"BIM           : {[round(x,3) for x in metrics_bim['eleven_point']]}")
        print(f"Two-Poisson   : {[round(x,3) for x in metrics_tp['eleven_point']]}")
        print(f"BM10          : {[round(x,3) for x in metrics_bm10['eleven_point']]}")
        print(f"BM25          : {[round(x,3) for x in metrics_bm25['eleven_point']]}")
        print("="*100 + "\n")

        """
        Setelah dicoba beberapa query dari cleanedQrel, kami mendapat bahwa model yang dibuat masih jelek
        Ini dikarenakan recall dan presisi di kebanyakan query masih 0. 

        
        Berikut query yang nilai precision/recall nya tidak 0:
        - "what similarity laws must be obeyed when constructing aeroelastic models of heated high speed aircraft"
          BIM memiliki precision, recall, dan precision @ K teratas

        - "why does the compressibility transformation fail to correlate the high speed data for helium and air"
          semua model memiliki precision, recall, dan precision @ K yang sama,
          tapi BM10 memiliki 11-point interpolated average tertinggi, diikuti dengan Two Poisson Model 

        - "did anyone else discover that the turbulent skin friction is not over sensitive to the nature of the variation of the viscosity with temperature"
          BM10 memiliki precision tertinggi dengan nilai 0.1 dan recall tertinggi dengan nilai 0.5
          
        - "what is the effect of cross sectional shape on the flow over simple delta wings with sharp leading edges"
          BIM memiliki precision, recall, dan precision @ K teratas

        - "what size of end plate can be safely used to simulate two-dimensional flow conditions over a bluff cylindrical body of finite aspect ratio"
          BIM hanya satu-satunya model yang memiliki nilai precision, recall, dan precision @ K teratas, 
          model lainnya precision, recall, dan precision @ K teratas nya 0

        - "does transition in the hypersonic wake depend on body geometry and size"
          Two Poisson Model satu-satunya model yang memiliki nilai precision, recall, dan precision @ K teratas, 
          model lainnya precision, recall, dan precision @ K teratas nya 0

        - "how is the heat transfer downstream of the mass transfer region effected by mass transfer at the nose of a blunted cone"
          semua model memiliki precision, recall, dan precision @ K yang sama,
          tapi Two Poisson Model dan BM25 memiliki 11-point interpolated average tertinggi

        Jadi dapat disimpulkan setelah komparasi kasar, model BIM paling baik dari keempatnya dan model BM25 adalah yang terburuk karena hanya "menang" di satu query
        Tapi sekali lagi seluruh model kami rasa masih burukkarenakan recall dan presisi di kebanyakan query masih 0 dan bagi yang tidak 0, nilanya memang rendah
        """ 

if __name__ == "__main__":
    mainClass = Main()
    mainClass.main()

from Utils import Utils
from BIM import BIM
from porterStemmer import PorterStemmer
from collections import defaultdict
from BM25 import BM25
from TwoPoisson import TwoPoisson
from BM10 import BM10  # <-- Tambahan Import BM10

class BIM_Main:
    def __init__(self):
        self.BIM = BIM()
        self.ps = PorterStemmer()
        self.utils = Utils()
        self.invertedIndex = self.utils.makeInvertedIndex()
        self.bm25 = BM25(k1=1.5, b=0.75)
        self.two_poisson = TwoPoisson(k=1.2)
        self.bm10 = BM10(k1=1.5)  # <-- Inisialisasi BM10

    def main(self):
        while(True):
            query = self.getQuery()
            if not query:
                continue
                
            query_tokens = self.utils.tokenize(query)
            query_stems = self.ps.stem(query_tokens)
            query_posting_lists = self.get_query_posting_lists(query_stems)
            
            # Perhitungan skor relevansi untuk masing-masing model
            rel_bim = self.build_relDQ(query_posting_lists)
            rel_bm25 = self.build_relDQ_BM25(query_posting_lists, query_stems)
            rel_tp = self.build_relDQ_TwoPoisson(query_posting_lists, query_stems)
            rel_bm10 = self.build_relDQ_BM10(query_posting_lists, query_stems)  # <-- Hitung BM10
    
            # Proses perangkingan dokumen
            ranked_bim = self.rank_rel(rel_bim)
            ranked_bm25 = self.rank_rel(rel_bm25)
            ranked_tp = self.rank_rel(rel_tp)
            ranked_bm10 = self.rank_rel(rel_bm10)  # <-- Ranking BM10
            
            # Menampilkan komparasi hasil ranking sesuai permintaan tugas
            self.print_comparison_output(query, ranked_bim, ranked_tp, ranked_bm25, ranked_bm10)
        
    def getQuery(self):
        str = input("Enter Query: ")
        str = str.strip()
        return str

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
        rel = defaultdict(int)
        N = self.utils.get_N()
        for query_posting_list in query_posting_lists:
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

    # <-- Fungsi Baru: Menghitung skor untuk model BM10
    def build_relDQ_BM10(self, query_posting_lists, query_stems):
        rel = defaultdict(float)
        N = self.utils.get_N()

        for stem, posting_list in zip(query_stems, query_posting_lists):
            if not posting_list: 
                continue
            Nt = self.utils.get_Nt(posting_list)
            for d in posting_list:
                tf = self.utils.get_tf(stem, d)
                # BM10 tidak membutuhkan parameter dl dan avgdl
                score = self.bm10.calculate_score(tf, N, Nt)
                rel[d] += score
        return rel
    
    def rank_rel(self, rel):
        return sorted(rel, key=rel.get, reverse=True)
    
    # <-- Fungsi Baru: Menampilkan hasil komparasi antar-model secara rapi
    def print_comparison_output(self, query, ranked_bim, ranked_tp, ranked_bm25, ranked_bm10):
        print("\n" + "="*100)
        print(f"HASIL EVALUASI PERBANDINGAN MODEL UNTUK QUERY: '{query}'")
        print("="*100)
        print(f"1. BIM Peringkat Dokumen          : {ranked_bim[:10]}")
        print(f"2. Two-Poisson Peringkat Dokumen  : {ranked_tp[:10]}")
        print(f"3. BM25 Peringkat Dokumen         : {ranked_bm25[:10]}")
        print(f"4. BM10 Peringkat Dokumen         : {ranked_bm10[:10]}")
        print("-"*100)
        
        # print("\nTeks Singkat 5 Dokumen Teratas Berdasarkan Model BM10:")
        # for doc_idx in ranked_bm10[:5]:
        #     print(f" Dokumen [{doc_idx}]: {self.utils.get_shortend_document_text(doc_idx)}")
        # print("="*100 + "\n")

if __name__ == "__main__":
    mainClass = BIM_Main()
    mainClass.main()
from Utils import Utils
from BM10 import BM10
from porterStemmer import PorterStemmer
from collections import defaultdict

class Main:
    def __init__(self):
        self.ps = PorterStemmer()
        self.utils = Utils()
        self.invertedIndex = self.utils.makeInvertedIndex()
        self.bm10 = BM10(k1=1.5)  

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
            
            rel_bm10 = self.build_relDQ_BM10(query_posting_lists, query_stems)  
    
            ranked_bm10 = self.rank_rel(rel_bm10)  
            
            # Tampilkan perbandingan ranking dan evaluasi metrik
            self.print_output(ranked_bm10, query)
        
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
    
    def print_output(self, ranked_docs, query):
        print("=====================================================================================================================================")
        print(f"Berdasarkan query: {query}, ")
        print(f"dokumen diretrieve terurut dari yg paling relevan adalah: {ranked_docs}")

        print()
        for doc_idx in ranked_docs[:10]:
            print(f"{doc_idx}:")
            print(self.utils.get_shortend_document_text(doc_idx))
            print()

        print("=====================================================================================================================================")
        print("="*100 + "\n")

if __name__ == "__main__":
    mainClass = Main()
    mainClass.main()

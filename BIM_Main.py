from Utils import Utils
from BIM import BIM
from porterStemmer import PorterStemmer
from collections import defaultdict

class BIM_Main:
    def __init__(self):
        self.BIM = BIM()
        self.ps = PorterStemmer()
        self.utils = Utils()
        self.invertedIndex = self.utils.makeInvertedIndex()

    def main(self):
        while(True):
            query = self.getQuery()
            query_tokens = self.utils.tokenize(query)
            query_stems = self.ps.stem(query_tokens)
            query_posting_lists = self.get_query_posting_lists(query_stems)

            rel = self.build_relDQ(query_posting_lists)
            ranked_docs = self.rank_rel(rel)
            self.print_output(ranked_docs, query)
        
    def getQuery(self):
        str = input("Enter Query: ")
        str = str.strip()
        return str

    def get_query_posting_lists(self, query_stems):
        res = []

        for query_stem in query_stems:
            res.append(list(self.invertedIndex.get(query_stem)))    # dibuat list() krn invertedIndex keynya set

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
        

if __name__ == "__main__":
    mainClass = BIM_Main()
    mainClass.main()
    

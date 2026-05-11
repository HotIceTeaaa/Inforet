from collections import defaultdict 
from porterStemmer import PorterStemmer
from BooleanModel import BooleanModel
import TolerantRetrieval
class Main:
    def __init__(self):
        namaCorpus = "cleanCorpus.txt"
        with open(namaCorpus, 'r') as file:
            self.corpus = [line.rstrip('\n') for line in file]

        self.invertedIndex = {}
        self.ps = PorterStemmer()
        
    # Inisialisasi Engine dan Menjalankan UI
    def main(self):
        self.makeInvertedIndex()
        all_doc_ids = list(range(len(self.corpus)))
        
        
        engine = BooleanModel(all_doc_ids, self.invertedIndex, self.ps)
        
        
        TolerantRetrieval.run_cli(self, engine)
    

    def makeInvertedIndex(self):
        index = defaultdict(set)   # a set avoids duplicate IDs automatically

        for doc_id, paragraf in enumerate(self.corpus):
            tokens = self.tokenize(paragraf)
            stems = self.ps.stem(tokens)
            for stem in stems:
                index[stem].add(doc_id)

        # Convert sets to sorted lists (more readable, easier for merging)
        self.invertedIndex = {term: sorted(list(postings)) for term, postings in index.items()}
    
    def tokenize(self, paragraf):
        return paragraf.split(" ")

if __name__ == "__main__":
    mainClass = Main()
    mainClass.main()
    

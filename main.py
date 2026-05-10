"""
step 1: jalanin kode generateCorpusDict.py, bakal ngebuat file corpusDict.txt. 
isinya dictionary, keynya index dokumen, valuenya isi dokumennya. 
Harusnya mudahin pas nunjukin hasil querynya nanti

(udh dijalanin, udh ada file txtnya)


step 2: jalanin kode generateCleanCorpus.py bakal ngebuat file cleanCorpus.txt
isinya baris2 string. setiap baris itu isinya dokumen yg udh di preproces.

(udh dijalanin, udh ada file txtnya)
"""

from collections import defaultdict 
from porterStemmer import PorterStemmer

class Main:
    def __init__(self):
        namaCorpus = "cleanCorpus.txt"
        with open(namaCorpus, 'r') as file:
            self.corpus = [line.rstrip('\n') for line in file]

        self.invertedIndex = {}
        self.ps = PorterStemmer()

    def main(self):
        self.makeInvertedIndex()
        print(self.invertedIndex)

    def makeInvertedIndex(self):
        index = defaultdict(set)

        for doc_id, paragraf in enumerate(self.corpus):
            tokens = self.tokenize(paragraf)
            stems = self.ps.stem(tokens)
            for stem in stems:
                index[stem].add(doc_id)

        # postingnya di sort menaik
        self.invertedIndex = {term: sorted(list(postings)) for term, postings in index.items()}
    
    def tokenize(self, paragraf):
        return paragraf.split(" ")

if __name__ == "__main__":
    mainClass = Main()
    mainClass.main()

import ast
from collections import defaultdict 
from porterStemmer import PorterStemmer

class Utils:
    def __init__(self):
        namaCorpus = "cleanCorpus.txt"
        with open(namaCorpus, 'r') as file:
            self.corpus = [line.rstrip('\n') for line in file]

        with open('corpusDict.txt', 'r') as file:
            data = file.read()
        self.corpusDict = ast.literal_eval(data)

        self.ps = PorterStemmer()
    
    # inget doc_idx mulai dari 0 bukan dari 1
    def get_tf(self, term, doc_idx):
        doc = self.corpus[doc_idx]
        words = doc.split(' ')
        return words.count(term)
    
    # Nt adalah df (document frekuensi)
    # drpd ngitung dr corpus, tinggal ambil panjang dari posting list
    def get_Nt(self, posting_list):
        return len(posting_list)
    
    # N adalah brp banyak document di corpus
    def get_N(self):
        return len(self.corpus)
    
    # inget doc_idx mulai dari 0 bukan dari 1
    def get_document_length(self, doc_idx):
        doc = self.corpus[doc_idx]
        return len(doc)
    
    def get_avg_document_length(self):
        sum = 0

        for doc_idx in range(self.get_N()):
            sum += self.get_document_length(doc_idx)
        
        return sum // self.get_N()
    
    def makeInvertedIndex(self):
        index = defaultdict(set)

        for doc_idx, doc in enumerate(self.corpus):
            tokens = self.tokenize(doc)
            stems = self.ps.stem(tokens)
            for stem in stems:
                index[stem].add(doc_idx)

        # postingnya di sort menaik
        return {term: sorted(list(postings)) for term, postings in index.items()}
    
    def tokenize(self, doc):
        return doc.split(" ")
    
    def get_shortend_document_text(self, doc_idx):
        text = self.corpusDict[doc_idx]
        
        if len(text) > 300:
            text = text[0:300]
            text += "..."

        return text
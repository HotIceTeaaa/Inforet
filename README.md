## Installation

Clone repository:

git clone https://github.com/HotIceTeaaa/Inforet.git


## Usage

Step 1: Generate cleaned corpus

python generateCleanCorpus.py

Step 2: Generate corpus dictionary

python generateCorpusDict.py

Step 3: Stemming

python porterStemmer.py

Step 4: Run search engine

python main.py


## Workflow

1. Preprocessing
   - Read cran.all.100.xml
   - Clean text
   - Save to cleanCorpus.txt

2. Indexing
   - Tokenization
   - Porter stemming
   - Build inverted index

3. Query Processing
   - Wildcard expansion
   - Spelling correction
   - Boolean evaluation

4. Result Display
   - Retrieve document IDs
   - Map IDs to original documents

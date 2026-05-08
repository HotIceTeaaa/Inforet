import re
import ast

def get_levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return get_levenshtein_distance(s2, s1)
    if not s2: return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def get_spelling_correction(term, vocabulary):
    best_match = None
    min_dist = 999
    for v in vocabulary:
        dist = get_levenshtein_distance(term, v)
        if dist < min_dist and dist <= 2:
            min_dist = dist
            best_match = v
    return best_match

def get_wildcard_matches(pattern, vocabulary):
    regex_pattern = "^" + pattern.replace("*", ".*") + "$"
    try:
        regex = re.compile(regex_pattern)
        return [term for term in vocabulary if regex.match(term)]
    except:
        return []


def get_postings(raw_token, invertedIndex, stemmer):
    raw_token = raw_token.lower()
    vocabulary = list(invertedIndex.keys())

    # 1. Wildcard
    if "*" in raw_token:
        matches = get_wildcard_matches(raw_token, vocabulary)
        res = set()
        for m in matches: res.update(invertedIndex.get(m, []))
        return sorted(list(res))
    
    # 2. Normal / Stemming
    stemmed = stemmer.stem([raw_token])[0]
    
    # 3. Typo Detection
    if stemmed not in invertedIndex:
        corrected = get_spelling_correction(stemmed, vocabulary)
        if corrected:
            print(f" -> Typo terdeteksi ! \n -> (Mengubah kata menjadi: '{corrected}')")
            return invertedIndex.get(corrected, [])
            
    return invertedIndex.get(stemmed, [])


def run_cli(main_instance):
    import BooleanEngine 
    
    # Load corpusDict 
    doc_details = {}
    try:
        with open('corpusDict.txt', 'r', encoding='utf-8') as f:
            doc_details = ast.literal_eval(f.read())
    except:
        pass

    print("~ MESIN PENCARI SEDERHANA ~")
    
    while True:
        user_query = input("\nMasukkan Query / 'exit': ")
        if user_query.lower() == 'exit':
            break
            
        results = BooleanEngine.evaluateQuery(user_query, main_instance.invertedIndex, main_instance.ps)
        
        if results:
            print(f"\nJumlah Dokumen: {len(results)}")
            print(f"ID Dokumen: {results}")
            print("\n")
            print("Menampilkan 7 Dokumen Teratas:")
            
            for doc_id in results[:7]:
                content = doc_details.get(doc_id, "Isi tidak ditemukan")
                print(f" - [Doc ID {doc_id}]: {content[:110]}...")
        else:
            print("\n-> Hasil tidak ditemukan.")
import archive.TolerantRetrieval as TolerantRetrieval

class BooleanModel:
    def __init__(self, all_doc_ids, invertedIndex, stemmer):
        self.all_doc_ids = all_doc_ids
        self.invertedIndex = invertedIndex
        self.ps = stemmer
    #Fungsi ini merepresentasikan intersect atau logika AND
    def intersect(self, list1, list2):
        if not list1 or not list2: return []
        result = []
        i = j = 0
        while i < len(list1) and j < len(list2):
            if list1[i] == list2[j]:
                result.append(list1[i]); i += 1; j += 1
            elif list1[i] < list2[j]: i += 1
            else: j += 1
        return result

    #Fungsi ini merepresentasikan union atau logika OR
    def union(self, list1, list2):
        result = []
        i = j = 0
        while i < len(list1) and j < len(list2):
            if list1[i] == list2[j]:
                result.append(list1[i]); i += 1; j += 1
            elif list1[i] < list2[j]:
                result.append(list1[i]); i += 1
            else:
                result.append(list2[j]); j += 1
        result.extend(list1[i:])
        result.extend(list2[j:])
        return result
    
    #Fungsi ini merepresentasikan logika NOT
    def difference(self, all_docs, list_to_exclude):
        result = []
        i = j = 0
        while i < len(all_docs) and j < len(list_to_exclude):
            if all_docs[i] < list_to_exclude[j]:
                result.append(all_docs[i]); i += 1
            elif all_docs[i] == list_to_exclude[j]:
                i += 1; j += 1
            else: j += 1
        result.extend(all_docs[i:])
        return result

    #fungsi parser untuk memproses query dari pengguna
    def evaluateQuery(self, query):
        # Pecah string query menjadi list berdasarkan spasi
        tokens = query.split()
        if not tokens: return []
    # fitur Wildcard dan Typo Correction
        #Konversi kata menjadi daftar ID (Posting List)
        elements = []
        for token in tokens:
            t_upper = token.upper()
            # Jika token adalah operator, masukkan sebagai string
            # tetapi jika token adalah kata kunci, lakukan stemming lalu ambil list ID-nya
            if t_upper in ["AND", "OR", "NOT"]: 
                elements.append(t_upper)
            else:
                p_list = TolerantRetrieval.get_postings(token, self.invertedIndex, self.ps)
                elements.append(p_list)

        #Proses NOT
        i = 0
        while i < len(elements):
            if elements[i] == "NOT":
                if i + 1 < len(elements) and isinstance(elements[i+1], list):
                    # Lakukan penghapusan dokumen dengan kata kunci'
                    negated = self.difference(self.all_doc_ids, elements[i+1])
                    elements[i:i+2] = [negated]
                else: elements.pop(i)
            else: i += 1

        # Proses AND
        i = 1
        while i < len(elements):
            if elements[i] == "AND":
                # Ambil list di kiri dan kanan operator AND
                res = self.intersect(elements[i-1], elements[i+1])
                elements[i-1:i+2] = [res]
            else: i += 1

        # 3. Proses OR
        if not elements: return []
        final_res = elements[0] # Mulai dari elemen pertama
        i = 1
        while i < len(elements):
            if elements[i] == "OR":
                # Gabungkan hasil saat ini dengan list setelah operator OR
                final_res = self.union(final_res, elements[i+1])
                i += 2
            else: i += 1
        return final_res
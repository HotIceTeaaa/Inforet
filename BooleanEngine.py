import TolerantRetrieval

def intersect(list1, list2):
    result = []
    i, j = 0, 0
    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            result.append(list1[i]); i += 1; j += 1
        elif list1[i] < list2[j]: i += 1
        else: j += 1
    return result

def union(list1, list2):
    result = []
    i, j = 0, 0
    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            result.append(list1[i]); i += 1; j += 1
        elif list1[i] < list2[j]:
            result.append(list1[i]); i += 1
        else:
            result.append(list2[j]); j += 1
    result.extend(list1[i:]); result.extend(list2[j:])
    return result

def evaluateQuery(query, invertedIndex, stemmer):
    tokens = query.split()
    if not tokens: return []

    result = TolerantRetrieval.get_postings(tokens[0], invertedIndex, stemmer)
    
    i = 1
    while i < len(tokens):
        op = tokens[i].upper()
        if i + 1 < len(tokens):
            next_p = TolerantRetrieval.get_postings(tokens[i+1], invertedIndex, stemmer)
            if op == "AND": result = intersect(result, next_p)
            elif op == "OR": result = union(result, next_p)
        i += 2
    return result
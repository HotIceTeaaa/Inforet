def intersect(list1, list2):
    result = []
    i = 0
    j = 0

    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            result.append(list1[i])
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            i += 1
        else:
            j += 1

    return result


def union(list1, list2):
    result = []
    i = 0
    j = 0

    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            result.append(list1[i])
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            result.append(list1[i])
            i += 1
        else:
            result.append(list2[j])
            j += 1

    while i < len(list1):
        result.append(list1[i])
        i += 1

    while j < len(list2):
        result.append(list2[j])
        j += 1

    return result


def evaluateQuery(query, invertedIndex, stemmer):
    tokens = query.split()

    if len(tokens) == 0:
        return []

    first_term = stemmer.stem([tokens[0].lower()])[0]
    result = invertedIndex.get(first_term, [])

    i = 1
    while i < len(tokens):
        operator = tokens[i].upper()

        if i + 1 >= len(tokens):
            break

        next_term = stemmer.stem([tokens[i + 1].lower()])[0]
        posting = invertedIndex.get(next_term, [])

        if operator == "AND":
            result = intersect(result, posting)

        elif operator == "OR":
            result = union(result, posting)

        i += 2

    return result
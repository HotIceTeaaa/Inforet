# buat testing doang

with open('cleanCorpus.txt', 'r') as file:
    paragraphs = [line.rstrip('\n') for line in file]

print(paragraphs)
print(len(paragraphs))
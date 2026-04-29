from collections import Counter

# buat testing hasil corpus doang, baut make sure semua simbol sama nomor udh ilang
filename = "cleanCorpus.txt"

with open(filename) as f:
    text = f.read()

counter = Counter(text)

for char, count in sorted(counter.items(), key=lambda x: -x[1]):
    # Represent control characters nicely
    repr_char = repr(char)[1:-1]  # removes quotes
    print(f"{repr_char:<12} {count}")
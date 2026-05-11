from collections import Counter

# buat testing hasil corpus doang, buat make sure semua simbol sama nomor udh ilang
filename = "cleanCorpus.txt"

with open(filename) as f:
    text = f.read()

counter = Counter(text)

for char, count in sorted(counter.items(), key=lambda x: -x[1]):
    repr_char = repr(char)[1:-1]  # ilanging quotes di belakang sama di depan
    print(f"{repr_char:<12} {count}")

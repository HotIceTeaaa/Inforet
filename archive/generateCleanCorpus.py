import re

input_file = "cran.all.100.xml"
output_file = "cleanCorpus.txt"

with open(input_file, "r", encoding="utf-8") as f:
    data = f.read()

# isi paragrafnya ad di <text>
texts = re.findall(r"<text>(.*?)</text>", data, re.DOTALL)

with open(output_file, "w", encoding="utf-8") as f:
    for t in texts:
        line = t.strip().replace('\n', ' ').replace('\r', ' ')
        if not line:
            continue

        # semua spaci yg dobel/triple/dll diganti sama single spaci aja
        line = re.sub(r'\s+', ' ', line).strip()

        # setiap kata di awal kalimat di lowercase (heuristik)        
        line = re.sub(r'\. ([A-Z][A-Za-z]*)', lambda m: '. ' + m.group(1).lower(), line) # cari '. Capital'
        first, rest = line.split(None, 1) 
        first = str.lower(first)
        line = first + " " + rest

        # semua simbol diganti spaci
        line = re.sub(r'[^a-zA-Z\s]', ' ', line)

        # semua spaci yg dobel/triple/dll diganti sama single spaci lagi
        line = re.sub(r'\s+', ' ', line).strip()

        if line:
            f.write(line + "\n")

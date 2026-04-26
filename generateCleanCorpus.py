import re

input_file = "cran.all.100.xml"
output_file = "cleanCorpus.txt"

with open(input_file, "r", encoding="utf-8") as f:
    data = f.read()

# Step 1 & 2: extract <text> content and remove internal newlines
texts = re.findall(r"<text>(.*?)</text>", data, re.DOTALL)

with open(output_file, "w", encoding="utf-8") as f:
    for t in texts:
        # Remove newlines inside the text and strip surrounding whitespace
        line = t.strip().replace('\n', ' ').replace('\r', ' ')
        if not line:
            continue

        # Step 5 (first pass): condense all whitespace to single spaces
        line = re.sub(r'\s+', ' ', line).strip()

        # Step 3: lowercase the first word of the sentence        
        line = re.sub(r'\. ([A-Z][A-Za-z]*)', lambda m: '. ' + m.group(1).lower(), line) # cari '. Capital'
        first, rest = line.split(None, 1)   # Python, splits on any whitespace, max 1 split
        first = str.lower(first)
        line = first + " " + rest

        # Step 4: replace all symbols and numbers with ' '
        line = re.sub(r'[^a-zA-Z\s]', ' ', line)

        # Step 5 (final): condense spaces again (removing punctuation may create gaps)
        line = re.sub(r'\s+', ' ', line).strip()

        # Write the final cleaned line
        if line:
            f.write(line + "\n")
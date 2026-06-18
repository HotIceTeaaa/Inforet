#!/usr/bin/env python3
"""
Convert cran.qrel.xml and cranqrel.trec.txt into cleanedQrel.txt
- XML entries with num > 100 are skipped.
- Third-column values from TXT that are > 100 are ignored.
- Titles that end up with no matching values are omitted.
- Trailing " ." at the end of every title is removed.
- Internal newlines in titles are replaced with spaces (title becomes one line).
Hardcoded filenames – just run the script in VSCode.
"""

import os
from collections import defaultdict
import xml.etree.ElementTree as ET


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    xml_path = os.path.join(script_dir, "cran.qry.xml")
    txt_path = os.path.join(script_dir, "cranqrel.trec.txt")
    out_path = os.path.join(script_dir, "cleanedQrel.txt")

    # 1. Parse XML, keep only num <= 100
    tree = ET.parse(xml_path)
    root = tree.getroot()
    xml_entries = []
    for top in root.findall("top"):
        num_el = top.find("num")
        title_el = top.find("title")
        if num_el is None or title_el is None:
            continue
        num = int(num_el.text.strip())
        if num > 100:
            continue
        raw_title = title_el.text.strip() if title_el.text else ""
        # Collapse all whitespace (including newlines) to single spaces
        clean_title = ' '.join(raw_title.split())
        # Remove trailing space + dot " ." if present
        if clean_title.endswith(" ."):
            clean_title = clean_title[:-2]
        xml_entries.append((num, clean_title))

    # 2. Parse TXT: collect third column values where flag != 0 and value <= 100
    num_to_vals = defaultdict(list)
    with open(txt_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) != 4:
                continue
            first, _, third, fourth = parts
            if int(fourth) == 0:
                continue
            third_val = int(third)
            if third_val > 100:
                continue
            num_to_vals[int(first)].append(third)

    # 3. Write output – skip entries that have no values
    with open(out_path, "w", encoding="utf-8") as out:
        for num, title in xml_entries:
            vals = num_to_vals.get(num, [])
            if not vals:
                continue
            out.write(title + "\n")
            out.write(" ".join(vals) + "\n")

    print(f"Done! Output written to: {out_path}")


if __name__ == "__main__":
    main()
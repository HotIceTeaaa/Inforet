import xml.etree.ElementTree as ET

def xml_to_dict(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    # harus di wrap sama <root> krn g keambil 
    wrapped = f"<root>{content}</root>"
    
    root = ET.fromstring(wrapped)
    
    doc_dict = {}
    for doc in root.findall('doc'):
        docno = int(doc.find('docno').text.strip()) - 1     # -1 biar indexnya mulai dr 0
        text = doc.find('text').text.strip()
        doc_dict[docno] = text
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(doc_dict))


xml_to_dict('cran.all.100.xml', 'corpusDict.txt')

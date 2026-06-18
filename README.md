## Installation

Clone repository:

git clone https://github.com/HotIceTeaaa/Inforet.git


## Cara Menggunakan

Kami mengimplementasi 4 model (BIM, Two Poisson, BM10, BM25)
Masing-masing model sudah ada kelas Mainnya masing-masing. Kelas tersebut bisa langsung dijalankan. 
Ketika dijalankan akan muncul permintaan input untuk memasukan query. 

Kami juga mengimplementasi Kelas main untuk mengevaluasi Keempat model.
Kelas ini bisa langsung dijalankan dan akan diminta memasukan query.
Query yang dimasukan harus sama dengan query yang ada di file cleanedQrel.txt
Silahkan bisa dipilih salah satu (di copy and paste)

Format file ini adalah:
{query 1}
{dokumen id yang relevan terhadap query 1}
{query 2}
{dokumen id yang relevan terhadap query 2}
dst...

Folder archieve berisi file dan folder bekas yang sudah tidak digunakan.

## Penjelasan Singkat Keempat Formula Model

BIM: Menghitung skor probabilitas murni berdasarkan ketiadaan atau keberadaan kata biner tanpa memperdulikan frekuensi kemunculan.
Two-Poisson: Menghitung skor dengan mempertimbangkan term frequency menggunakan parameter saturasi k konstan, sehingga skor term tidak naik tanpa batas.
BM10: Menghitung skor saturasi frekuensi kata menggunakan parameter k1 tanpa melakukan normalisasi ukuran dokumen.
BM25: Menghitung skor frekuensi kata yang dimodifikasi dengan parameter b untuk melakukan normalisasi, sehingga dokumen yang terlalu panjang akan menerima penalti.

Seluruh skor dari kata kunci yang cocok diakumulasikan, dan sistem melakukan ranking dokumen secara menurun.

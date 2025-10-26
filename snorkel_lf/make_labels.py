# mini.csv 읽어서 간단 휴리스틱으로 0/1 라벨 추론 → data/interim/weak_labels.csv 저장
import csv, re, os
src = "data/raw/mini.csv"; dst="data/interim/weak_labels.csv"
os.makedirs("data/interim", exist_ok=True)
URL = re.compile(r'https?://')
urgent = re.compile(r'(긴급|즉시|정지|미납|법적)')
with open(src, newline='') as f, open(dst, 'w', newline='') as g:
    r=csv.DictReader(f); w=csv.DictWriter(g, fieldnames=['text','weak_label']); w.writeheader()
    for row in r:
        t=row['text']
        score = 0
        if URL.search(t): score+=1
        if urgent.search(t): score+=1
        w.writerow({'text': t, 'weak_label': int(score>=1)})
print("wrote", dst)

import csv, os
from ko_perturb import perturb
src="data/raw/mini.csv"
dst="data/interim/mini_perturbed.csv"
os.makedirs("data/interim", exist_ok=True)
with open(src, newline='') as f, open(dst, "w", newline='') as g:
    r=csv.DictReader(f)
    w=csv.DictWriter(g, fieldnames=["text","label","text_perturbed"])
    w.writeheader()
    for row in r:
        w.writerow({"text": row["text"], "label": row["label"], "text_perturbed": perturb(row["text"])})
print("wrote", dst)

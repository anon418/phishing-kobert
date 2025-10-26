import csv, json, requests
API="http://localhost:8000/predict"
src="data/raw/mini.csv"
aug="data/interim/mini_perturbed.csv"
out="data/interim/aug_compare.csv"

def call(text):
    r=requests.post(API, headers={"Content-Type":"application/json"},
        data=json.dumps({"text": text}), timeout=10).json()
    return r["prob"], r["decision"], "|".join(r.get("intents",[]))

with open(src) as f1, open(aug) as f2, open(out,"w",newline="") as g:
    r1=csv.DictReader(f1); r2=csv.DictReader(f2)
    w=csv.DictWriter(g, fieldnames=["orig","perturbed","label",
                                    "prob_orig","dec_orig","intents_orig",
                                    "prob_aug","dec_aug","intents_aug"])
    w.writeheader()
    for a,b in zip(r1,r2):
        p1,d1,i1 = call(a["text"])
        p2,d2,i2 = call(b["text_perturbed"])
        w.writerow({"orig":a["text"],"perturbed":b["text_perturbed"],
                    "label":a["label"],
                    "prob_orig":round(p1,4),"dec_orig":d1,"intents_orig":i1,
                    "prob_aug":round(p2,4),"dec_aug":d2,"intents_aug":i2})
print("wrote", out)

import csv, json, requests, itertools, statistics as st

SRC = "data/interim/weak_labels.csv"
OUT = "data/interim/sweep_results.csv"
API = "http://localhost:8000/predict"

def eval_once(threshold:float, lm:float, rule:float, band:float=0.05):
    tp=fp=tn=fn=ab=0
    with open(SRC) as f:
        r=csv.DictReader(f)
        for row in r:
            text=row["text"]; y=int(row["weak_label"])
            body={"text":text, "threshold":threshold,
                  "abstain_band":band, "lm_w":lm, "rule_w":rule}
            resp=requests.post(API, headers={"Content-Type":"application/json"},
                               data=json.dumps(body), timeout=10).json()
            dec=resp["decision"]
            if dec=="abstain": ab+=1; continue
            yhat=1 if dec=="phishing" else 0
            if   y==1 and yhat==1: tp+=1
            elif y==0 and yhat==0: tn+=1
            elif y==0 and yhat==1: fp+=1
            else: fn+=1
    n=tp+tn+fp+fn
    acc=(tp+tn)/n if n else 0.0
    prec=tp/(tp+fp) if (tp+fp)>0 else 0.0
    rec =tp/(tp+fn) if (tp+fn)>0 else 0.0
    f1=2*prec*rec/(prec+rec) if (prec+rec)>0 else 0.0
    cov = n/(n+ab) if (n+ab)>0 else 0.0  # 처리율(보류 제외 비율)
    return {"threshold":threshold,"lm_w":lm,"rule_w":rule,
            "acc":round(acc,4),"prec":round(prec,4),
            "rec":round(rec,4),"f1":round(f1,4),
            "coverage":round(cov,4),"n":n,"abstain":ab}

def main():
    ths=[0.45,0.5,0.55]
    lms=[0.5,0.6,0.7,0.8]; rules=[1-x for x in lms]
    rows=[]
    for th,(lm,rule) in itertools.product(ths, zip(lms,rules)):
        rows.append(eval_once(th,lm,rule,band=0.05))
    rows.sort(key=lambda x:(-x["f1"], -x["coverage"]))
    with open(OUT,"w",newline="") as g:
        w=csv.DictWriter(g, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print("wrote", OUT, "top:", rows[0])
if __name__=="__main__":
    main()

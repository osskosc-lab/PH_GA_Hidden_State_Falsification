# PH × 全身麻酔 Hidden-State Falsification

観察研究用の反証実験テンプレートです。臨床判断・薬剤投与には使用しません。

```bash
python -m pip install -r requirements.txt
python scripts/run_synthetic.py --out results
python scripts/evaluate.py --data results/synthetic.csv --out results
```

合成データで潜在量が回復できない場合は `NOT_IDENTIFIABLE` とします。

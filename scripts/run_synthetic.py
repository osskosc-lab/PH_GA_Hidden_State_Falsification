import argparse,os,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from phga.synthetic import generate
p=argparse.ArgumentParser();p.add_argument('--out',default='results');p.add_argument('--scenario',default='identifiable');p.add_argument('--seed',type=int,default=42);a=p.parse_args()
os.makedirs(a.out,exist_ok=True);generate(seed=a.seed,scenario=a.scenario).to_csv(f'{a.out}/synthetic.csv',index=False);print(f'Wrote {a.out}/synthetic.csv')

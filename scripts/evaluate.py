import argparse,json,os,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np,pandas as pd
from sklearn.metrics import mean_absolute_error
from phga.models import PHFactorizedModel,TARGETS
p=argparse.ArgumentParser();p.add_argument('--data',required=True);p.add_argument('--out',default='results');a=p.parse_args();os.makedirs(a.out,exist_ok=True)
d=pd.read_csv(a.data); test=set(sorted(d.patient.unique())[::5]); tr=d[~d.patient.isin(test)]; te=d[d.patient.isin(test)]; m=PHFactorizedModel().fit(tr); pred=m.predict(te)
mae={k:float(mean_absolute_error(te[k],pred[:,i])) for i,k in enumerate(TARGETS)}; sh=te.copy();sh['u_ext']=np.random.default_rng(1).permutation(sh.u_ext); shuffled=float(mean_absolute_error(te.C_B,m.predict(sh)[:,2]))
decision='SUPPORTED_SYNTHETIC_IDENTIFIABILITY' if max(mae.values())<=.15 and shuffled>mae['C_B']*1.10 else 'NOT_IDENTIFIABLE'; metrics={'decision':decision,'latent_mae':mae,'cb_mae_input_shuffled':shuffled,'warning':'Synthetic validation only; no clinical claim.'}
json.dump(metrics,open(f'{a.out}/metrics.json','w'),indent=2);pd.DataFrame(pred,columns=TARGETS).assign(patient=te.patient.to_numpy(),time=te.time.to_numpy()).to_csv(f'{a.out}/latent_trajectories.csv',index=False);pd.DataFrame([{'test':'F1_input_shuffle','base_cb_mae':mae['C_B'],'shuffled_cb_mae':shuffled,'passed':shuffled>mae['C_B']*1.10}]).to_csv(f'{a.out}/falsification_results.csv',index=False);print(json.dumps(metrics,indent=2))

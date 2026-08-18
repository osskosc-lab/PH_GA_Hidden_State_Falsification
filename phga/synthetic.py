import numpy as np
import pandas as pd

PHASES=("P0_pre","P1_induction","P2_maintenance","P3_emergence","P4_recovery")
def generate(n_patients=60,points=250,seed=42,scenario="identifiable"):
    rng=np.random.default_rng(seed); rows=[]; cuts=np.array([.18,.30,.70,.82])*points
    for p in range(n_patients):
        base=rng.normal(0,.12,3); gain=rng.uniform(.8,1.2)
        for t in range(points):
            phase=PHASES[np.searchsorted(cuts,t)]
            ind=1/(1+np.exp(-(t-cuts[0])/(points*.018))); em=1/(1+np.exp(-(t-cuts[2])/(points*.018)))
            cb=np.clip(gain*(ind-em)+base[2],0,1); hv=np.clip(.82-base[0]-.52*ind+.47*em,0,1); ho=np.clip(.50+base[1]+.22*ind-.16*em,0,1)
            if scenario=="phase_only": cb=hv=ho=.5
            u=cb+rng.normal(0,.05); y1=1.2*hv-.7*u+rng.normal(0,.07); y2=.9*ho+.3*hv+rng.normal(0,.07); y3=-.8*hv+1.4*u+rng.normal(0,.07)
            rows.append((p,t,phase,hv,ho,cb,u,y1,y2,y3))
    return pd.DataFrame(rows,columns="patient time phase H_V H_O C_B u_ext phys_1 eeg_1 phys_2".split())

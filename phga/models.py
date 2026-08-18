import numpy as np
from sklearn.linear_model import Ridge
FEATURES=["phys_1","eeg_1","phys_2","u_ext"]; TARGETS=["H_V","H_O","C_B"]
class PHFactorizedModel:
    def fit(self,df):
        self.models={k:Ridge(alpha=1.).fit(df[FEATURES],df[k]) for k in TARGETS}; return self
    def predict(self,df):
        return np.c_[*[np.clip(self.models[k].predict(df[FEATURES]),0,1) for k in TARGETS]]

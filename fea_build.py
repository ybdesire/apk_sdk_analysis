from tqdm import *
import os
import numpy as np
import joblib as jl

FEA_ROOT = 'features2'

X_label = []
X = []
for f1 in tqdm(os.listdir(FEA_ROOT)):
    f1_full_path =  os.path.join(FEA_ROOT, f1)
    for f2 in os.listdir( f1_full_path ):
        f2_full_path = os.path.join(f1_full_path, f2)
        if(os.path.isfile(os.path.join(f2_full_path, 'fea.jl'))):
            X_label.append('{}___{}'.format(f1, f2))
            X.append(jl.load(os.path.join(f2_full_path, 'fea.jl')))
X = np.array(X)
jl.dump(X, 'X.jl.z')
jl.dump(X_label, 'X_label.jl.z')

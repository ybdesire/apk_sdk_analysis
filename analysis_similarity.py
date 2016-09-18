from tqdm import *
import os
import numpy as np
import joblib as jl
import time
import math


def is_similar(x, y):
    assert x.shape==y.shape
    for i in range(x.shape[0]):
        d = x[i]-y[i]
        if(d!=0):
            return False
    return True


X = jl.load('X.jl.z')
X_label = jl.load('X_label.jl.z')

result = jl.load('result_similarity/result3.jl.z')
i=114980*3
for m in tqdm(X[i:]): 
    if(i==0):
        d = {}
        d['count']=1
        d['name']=[]
        d['name'].append(X_label[i])
        d['index']=[]
        d['index'].append(i)
        result.append(d)
    else:
        x = X[i]
        found = False
        for j in range(len(result)):
            y = X[result[j]['index'][0]]
            if(is_similar(x, y)):
                result[j]['count'] += 1
                result[j]['name'].append(X_label[i])
                result[j]['index'].append(i)
                found = True
                break
        if(found==False):
            d = {}
            d['count']=1
            d['name']=[]
            d['name'].append(X_label[i])
            d['index']=[]
            d['index'].append(i)
            result.append(d)
    i += 1
    if( (i%(X.shape[0]/10))==0 ):
        jl.dump(result, 'result_similarity/result{}.jl.z'.format((i/(X.shape[0]/10))))

jl.dump(result, 'result_similarity/result_similarity.jl.z')

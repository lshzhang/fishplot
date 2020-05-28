#/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def fishplot(data,ax=None,cmap='tab20',smooth = 100,**kwargs):
    if not ax:
        ax = plt.gca()
        
    try:
        mycmp = plt.get_cmap(cmap)
    except:
        mycmp = cmap
    
    npdate = []
    for time in data.date:
        tmp = time.split('/')
        npdate.append(np.datetime64('-'.join(tmp)))
    data.date = npdate
    
    ## genYmatrix
    vardict = {}
    dflist = data.groupby('date')
    col = len(dflist)
    for x,dfx in dflist:
        for row in dfx.itertuples():
            if row.variants in vardict.keys():
                vardict[row.variants].append(row.freq)
            else:
                vardict[row.variants] = [row.freq]
    variants = []
    vararray = [(k,v) for k, v in vardict.items()]
    row = len(vararray)
    ys = np.zeros((row,col))
    for i in range(row):
        variants.append(vararray[i][0])
        try:
            ys[i] = np.array(vararray[i][1],dtype=np.float32)
        except:
            pass
        
    
    ## smooth edge
    row,col = ys.shape
    n = smooth // (col-1)
    xgap = n
    y = ys
    Sum = [0] * col
    power = np.zeros((col-1)*n)
    for i in y:
        Sum += i
    for i in range(1,col):
        base = np.linspace(Sum[i-1],Sum[i],n+1)
        if Sum[i] > Sum[i-1]:
            trans = Sum[i-1] + (Sum[i] - Sum[i-1]) * (1- np.cos((base-Sum[i-1])/(Sum[i]-Sum[i-1])*np.pi)) / 2
        elif Sum[i] < Sum[i-1]:
            trans = Sum[i] + (Sum[i-1] - Sum[i]) * (1 - np.cos((base-Sum[i])/(Sum[i-1]-Sum[i])*np.pi)) / 2
        else:
            trans = base
        power[(i-1)*n:i*n] = trans[0:n]
    new = np.zeros((row,(col-1)*n))
    for i in range(row):
        newrow = np.zeros((col-1)*n)
        for j in range(1,col):
            base = np.linspace(y[i,j-1],y[i,j],n+1)
            newrow[(j-1)*n:j*n] = base[0:n]
        new[i,:] = newrow
    for i in range(1,(col-1)*n):
        new[:,i] = new[:,i] / (sum(new[:,i]) + 10 ** (-6)) * power[i]
    new[np.isnan(new)] = 0
    
    
    ## stackplot
    x = range(new.shape[1])
    fish = ax.stackplot(x,new,baseline='sym',colors=mycmp.colors[0:len(variants)],**kwargs)
    
    ax.tick_params(axis='both', which='both', labelsize=14,
                   top = False, bottom = False, left = False, right = False)
    for edge, spine in ax.spines.items():
        spine.set_visible(False)
        
    ## xaxis
    col = ys.shape[1]
    xbreak = [ i * xgap for i in range(col)]
    xlabels = np.datetime_as_string(data.date.unique(),unit='D')
    ax.set_xticks(xbreak)
    ax.set_xticklabels(xlabels)
    
    ## yaxis
    ax.set_yticklabels([])
    ax.set_yticks([])
    ymin,ymax = ax.get_ybound()
    if ymax < 0.05:
        ax.set_ylim(-0.03,0.03)
    else:
        ax.set_ylim(ymin*1.2,ymax*1.2)
    
    return fish

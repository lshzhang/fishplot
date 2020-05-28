# fishplot
using matplotlib to draw fish plot
----------
```python
from fishplot import fishplot

d = {'date':['2010/09/20','2010/09/20','2010/10/20','2010/10/20','2011/11/20','2011/11/20'],'variants':['TP53','NTRK','TP53','NTRK','TP53','NTRK'],'freq':[0.3,0.2,0.1,0.2,0.2,0.5]}
df = pd.DataFrame(data=d)

fishplot(df)
```

import numpy as np

def benjamini(l, a=0.05):
    """
For Benjamini-Hochberg significance testing for an array_like of p-values.
Returns an array_like of bools of the type and shape of l.
`a` = 0.05 unless specified.
     """
    if type(l) in [int,float]:
        return l <= a
    elif len(np.array(l).shape) == 1:
        ret = [(i <= a/(len(l)-n),list(l).index(i)) for n,i in enumerate(sorted(l))]
        for n,i in enumerate(reversed(ret)):
            if i[0]:
                break
        n = len(ret) - n
                
        ret = [(True, i[1]) if m < n else i for m,i in enumerate(ret)]
        ret = sorted(ret, key=lambda x: x[1])
        ret = [i[0] for i in ret]
        if type(l) is list:
            return ret
        else:
            return np.array(ret)
    elif len(np.array(l).shape) > 1:
        ret = [benhoch(i,a) for i in l]
        if type(l) is list:
            return ret
        else:
            return np.array(ret)

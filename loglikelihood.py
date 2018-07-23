import numpy as np
import scipy as sp

def loglikelihood(kij, distfunc=sp.stats.chi2.sf):
    """
For running a log-likelihood test for a 2D array_like observation matrix kij.
Returns the p-value for the given test from the scipy.stats.chi2 unless `distfunc` is specified.
Raises an Exception if it cannot calculate the test as given.

TODO: Implement recursive calling for higher dimensions.
    """
    kij = np.array(kij)
    if len(kij.shape) < 2:
        raise Exception('Not a valid test for a ' + str(len(kij.shape)) + ' dimensional table.')
    elif len(kij.shape) > 2:
        ret = [loglikelihood(i,distfunc) for i in kij]
        if type(kij) is list:
            return ret
        else:
            return np.array(ret)
    
    n = kij/np.sum(kij,0)
    m = np.sum(kij,1)/np.sum(kij)
    for j in range(n.shape[0]):
        if all(i == 0 for i in n[j,:]) and m[j] == 0:
            m[j] = 1
    if any(m==0):
        raise Exception('One of the probabilities is unfixably 0.')
        
    a = np.array([n[:,i]/m for i in range(n.shape[1])])
    a[a == 0] = 10**-8
    a = np.log(a)
    a = np.sum(a*kij.T)
    
    ret = distfunc(a,kij.shape[0]-1)
    if type(kij) is list:
        return ret
    else:
        return np.array(ret)

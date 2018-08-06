import numpy as np
import pandas as pd
import copy as _copy
from types import GeneratorType as _GEN

class DataFrameN():
    """
An multi-dimensional approximation of a dataframe that is a subclass of np.ndarray.
Pass labels for each axis and an n-D array-like, and it returns an object that can be indexed by index or value on each axis.
@labels can be any 2D array-like of axes x labels. Also accepts a 1D array-like for a 1D @data.

Unlike np.ndarray, this implements all mathematical functions.
    If the entire DataFrameN is not of an applicable type (ie numeric), it applies it only to the ones that can be converted to floats.
    """
    def __init__(self, data, labels=[]):
        if type(data) is pd.core.frame.DataFrame and len(labels) == 0:
            labels = [data.columns.values.tolist(), data.index.values.tolist()]
        self.data = np.array(data)
        
        if type(labels) is np.ndarray:
            labels = labels.tolist()
        if not type(labels) is list or len(labels) == 0:
            self._labels = None
            return

        if self.data.ndim == 1 and len(labels) != 1:
            # check if they passed [a,b,...]
            labels = [labels]
        else: # have to flip last two entries for some reason
            labels[-2:] = [labels[-1], labels[-2]]
        
        if not len(labels) == len(self.data.shape):
            raise Exception('Labels and data shapes do not match.')
        for n in range(len(labels)):
            if type(labels[n]) is np.ndarray:
                labels[n] = labels[n].tolist()
            if not len(labels[n]) == self.data.shape[n]:
                raise Exception('Not the same number of labels and data in axis '+str(self.data.ndim - n))
            
        self._labels = labels
        
    def __str__(self):
        if self.data.ndim == 1:
            if self._labels: return str(pd.Series(self.data, index = self._labels[0]))
            return str(pd.Series(self.data))
        
        if self.data.ndim == 2:
            if self._labels: return str(pd.DataFrame(self.data, index = self._labels[0],columns = self._labels[1]))
            return str(pd.DataFrame(self.data))
        
        return str(self.data)
    
    def __repr__(self):
        if self.data.ndim == 1:
            if self._labels: return repr(pd.Series(self.data, index = self._labels[0]))
            return repr(pd.Series(self.data))
        
        if self.data.ndim == 2:
            if not self._labels is None: return repr(pd.DataFrame(self.data, index = self._labels[0],columns = self._labels[1]))
            return repr(pd.DataFrame(self.data))
        
        return repr(self.data)
        
    def __getitem__(self,key):
        if not type(key) is tuple:
            key = tuple([key])
            
        # deal with backwards axes
        if len(key) == 1 and self.data.ndim != 1:
            key = (slice(None),key[0])
        elif len(key) >= 2:
            key = list(key)
            key[-2:] = [key[-1],key[-2]]
            key = tuple(key)
            
        temp = []
        for n,i in enumerate(key):
            if type(i) is str: # if the key entry is a str, get the index
                temp += [self._labels[n].index(i)]
            elif type(i) in [list, range, _GEN]: # if it's a list, range, or generator
                temp2 = []
                for j in i:
                    if type(j) is str: # if entry is a str, get the index
                        temp2 += [self._labels[n].index(j)]
                    else: temp2 += [j] # else it's an int
                temp += temp2
            else:
                temp += [i] # else it's an int or slice
                
        ret = self.data[tuple(temp)]
        if not type(ret) is np.ndarray:
            return ret
        elif ret.ndim == 1:
            return pd.Series(ret)
        elif ret.ndim == 2:
            return pd.DataFrame(ret)
        else:
            return ret

    @classmethod
    def read_csv(cls, file, shape=(1,1), tiling=1, labels=[], **kwargs):
        """
Reads in data from a csv file using pd.read_csv.
@file is the filepath or a buffer to be passed to pd.read_csv.
tuple(int) @shape is the shape of the data. Currently up to 4D is supported for any number of entries.
    For 2D or 1D arrays (ie len(shape) <= 2), shape, tiling, and label are ignored and everything else is directly passed to pd.read_csv.
        kwarg 'header' is allowed here. This is just to wrap existing functionality.
    Labels are applied if given.
    For 3D tiling in both directions, pass a tuple of each direction for that axis.

str @tiling can be either 'h'/0 or 'v'/1.
    This specifies if the third dimension is represented by multiple 2D tables next to each other (0) or multiple 2D tables stacked on top of each other (1).
    For dimensions higher than the third, can also be a list of these values for each successive axis.
    To tile a 3D matrix in both directions, pass a tuple of ('h'/0,'v'/1) or ('v'/1,'h'/0) to show the order of concatenation.
@labels is passed for object creation if dim > 2. usecols and skiprows should be set to only read the data.
    For dim < 3, labels can be passed with pd only reading data, or they can be set using pd.read_csv options by explicitly passing labels=None.

Note: Axis number here is from highest -> col -> row
Note: Whole file is read at once. If it is large enough to cause an error in pd.read_csv, you have to manually chunk it.
        """

        # simple case
        if len(shape) <=2 :
            if labels:
                return DataFrameN(pd.read_csv(file, **kwargs), labels)
            else:
                return DataFrameN(pd.read_csv(file, **kwargs))

        # Validating all the things
        if 'header' in kwargs:
            if not kwargs['header'] is None: raise Exception('Do not try to read in a header.')
            del kwargs['header']

        if not type(shape) is tuple:
            raise TypeError('shape must be a tuple of ints')
        if not type(tiling) is tuple:
            if not all([type(i) is int for i in shape]):
                raise TypeError('shape must be a tuple of ints')
            elif not all([i > 0 for i in shape]):
                raise ValueError('All entries in shape must be positive (ie > 0)')
        elif type(tiling) is  tuple and not type(shape[0]) is tuple and not all([type(i) is int for i in shape[1:]]):
            raise TypeError('shape must be a tuple of ints, except the first parameter')
        if not len(shape) < 5:
            raise NotImplementedError('Only implemented for 4D and smaller')

        if type(tiling) in [int, str]:
            tiling = [tiling]*(len(shape)-2)
        if type(tiling) is list:
            if len(tiling)+2 != len(shape):
                raise Exception('Invalid tiling parameter')
            for i in range(len(tiling)):
                if type(tiling[i]) is str:
                    if not tiling[i] in ['h','v']: raise ValueError('Invalid tiling parameter ' + i)
                    else: tiling[i] = 0 if tiling[i] is 'h' else 1 # convert string to int
                elif type(tiling[i]) is int:
                    if not tiling[i] in [0, 1]: raise ValueError('Invalid tiling parameter ' + str(i))
                    else: pass
                else:
                    raise TypeError('Invalid tiling parameter ' + str(i))
        elif type(tiling) is tuple:
            if len(tiling) != 2:
                raise Exception('Tuple for tiling must have len == 2')
            elif any([i not in [0,1] if type(i) is int else i not in ['h','v'] for i in tiling]):
                raise ValueError('Invalid tiling parameter')
            tiling = tuple([i if type(i) is int else ['vh'.index(i)] for i in tiling])

        else:
            raise TypeError('Invalid tiling parameter '+str(i))

        if labels:
            if not type(labels) is list or not all([type(i) is list for i in labels]): # since dim > 2
                raise TypeError('labels must be a list of lists')
            if not len(labels) <= len(shape):
                raise Exception('Too many labels passed')

        # Grab all the data
        xy = list(shape[-2:]) # endpoint of where to read
        if not type(tiling) is tuple:
            for n,i in zip(shape, tiling): # length, direction
                xy[i] *= n # multiply the endpoint by the number in this tiling direction
        else:
            for n,i in zip(shape[0], tiling):
                xy[i] *= n

        if 'nrows' in kwargs:
            assert xy[0] <= len(kwargs['nrows']), 'shape and nrows do not match'
            del kwargs['nrows']
        if 'usecols' in kwargs:
            assert xy[1] == len(kwargs['usecols']) if not type(kwargs['usecols']) is int else 1, 'shape and usecols do not match'

        data = np.array(pd.read_csv(file, header=None, nrows=xy[0], **kwargs))

        # Split the data
        xy = shape[-2:] # shape of 2D table
        assert data.shape[0] % xy[0] == 0, 'Returned data is wrong shape in axis=0'
        assert data.shape[1] % xy[1] == 0, 'Returned data is wrong shape in axis=1'

        x, y = data.shape[0] // xy[0], data.shape[1] // xy[1] # how many in each direction
        data = np.array(np.split(data, [xy[0]*i for i in range(1,x)], axis=0))
        data = np.array(np.split(data, [xy[1]*i for i in range(1,y)], axis=2)) # now have a new axis=0
        # now have a 4D array of 2D slices in order of original csv

        # Group the data appropriately
        if len(shape) == 3:
            if type(tiling) is tuple: # 2D tiling
                if tiling[0] == 0: # rows then columns
                    data = np.array([j for i in range(data.shape[1]) for j in data[:,i,:,:]]) # take whole row for each column
                else: # columns then rows
                    data = np.array([j for i in range(data.shape[0]) for j in data[i,:,:,:]]) # take whole column for each row
            elif tiling[0] == 0: # if tiled in rows
                data = data[:,0,:,:]
            else: # if tiled in cols
                data = data[0,:,:,:]

        elif len(shape) == 4:
            if tiling[0] == tiling[1]:
                if tiling[0] == 0:
                    data = data[:,0,:,:]
                else:
                    data = data[0,:,:,:]
                # check this
                data = np.split(data, [shape[0]*i for i in range(1, data.shape[0] // shape[0])], axis=0) # shape[0] = shape[-3]
            else: # 2D tiling
                if tiling[0] == 0: # rows for 3rd axis
                    data = np.transpose(data, axes=[1,0, 2,3])
                else: # columns for 3rd axis
                    pass

        if labels:
            return DataFrameN(data, labels)
        else:
            return DataFrameN(data)

    
    def index(self,item):
        """
Returns the first index of @item in self.data.
If self.data is 1D, it returns an int. Else it returns a tuple of ints.
        """
        if not item in self.data:
            raise ValueError(str(item) + ' not in DataFrameN')
        if self.data.ndim == 1:
            return self.data.tolist().index(item)
        
        return tuple(self._index_helper(self.data,item))
                            
    def _index_helper(self,array,item):
        if array.ndim == 1:
            return [array.tolist().index(item)]
        
        for n,i in enumerate(array):
            if np.sum(i == item) >= 1:
                return [n] + self._index_helper(i,item)
        
    def labels(self,axis=None,key=None):
        """
Returns the label for the specified location.
If int @axis is provided, it returns an list of labels for that axis.
If tuple @key is provided, it returns a list of labels for the given cell(s).
If neither @axis or @key is specified, returns an np.array of all the labels labels.
@axis supercedes @key.
        """

        if type(axis) is tuple: # see if they gave a key but didn't specify it
            key = axis
            axis = None

        if not axis is None:
            assert type(axis) is int, 'axis must be an int'
            if axis < len(self._labels):
                if self._labels:
                    if len(self._labels) == 1:
                        return self._labels[axis]
                    elif len(self._labels) == 2:
                        return list(reversed(self._labels))[axis]
                    else:
                        return (self._labels[0:-2] + [self._labels[-1],self._labels[-2]])[axis]
                else:
                    return list(range(self.data.shape[axis]))
            else:
                raise IndexError('Axis out of range')

        if key is None:
            if not self._labels is None:
                if len(self._labels) == 1:
                    return self._labels[0]
                elif len(self._labels) == 2:
                    return list(reversed(self._labels))
                else:
                    return self._labels[0:-2] + [self._labels[-1], self._labels[-2]]
            else:
                return [[j for j in range(i)] for i in self.data.shape]

        assert type(key) is tuple, 'key must be a tuple'
        assert len(key) == self.data.ndim, 'len(key) must equal self.ndim. Slices are allowed'

        temp = []
        for n,i in enumerate(key):
            idx = i
            if type(i) is str: # if the key entry is a str, get the index
                temp += [i]
                continue
            elif type(i) in [list, range, _GEN]: # if it's a list, range, or generator
                temp2 = []
                for j in i:
                    if type(j) is str: # if entry is a str, get the index
                        temp2 += [j]
                    else: temp2 += [j] # else it's an int
                idx = temp2

            if len(self._labels) == 1:
                temp += [self._labels[n][idx]]
            elif len(self._labels) == 2:
                temp += [list(reversed(self._labels))[n][idx]]
            else:
                temp += [(self._labels[:-2] + [self._labels[-1], self._labels[-2]])[n][idx]]

        return temp
    
    def transpose(self,axes=None, in_place=True):
        if axes is None:
            axes = list(reversed(range(len(self._labels))))
        else: 
            for i in range(len(self._labels)):
                if i not in axes:
                    axes += [i]

        if in_place:
            self.data = self.data.transpose(axes=axes)
            self._labels = np.array([self._labels[i] for i in axes])
            return self
        
        return DataFrameN(self.data.transpose(axes=axes), [self._labels[i] for i in axes])
    
    def deepcopy(self):
        return _copy.deepcopy(self)
    
    @property
    def shape(self):
        return self.data.shape
    @property
    def ndim(self):
        return self.data.ndim
    
    @property
    def T(self):
        return DataFrameN(self.data.T, list(reversed(self.labels())))
    
    # passing for dunder functions and implementing recursive checking
    def __add__(self,other):
        try:
            return DataFrameN(self.data + other, self.labels())
        except TypeError:
            return DataFrameN(self._op_helper('add',self.data, other), self.labels())

    def __sub__(self,other):
        try:
            return DataFrameN(self.data - other, self.labels())
        except TypeError:
            return DataFrameN(self._op_helper('sub',self.data, other), self.labels())

    def __mul__(self,other):
        try:
            return DataFrameN(self.data * other, self.labels())
        except TypeError:
            return DataFrameN(self._op_helper('mul',self.data, other), self.labels())

    def __truediv__(self,other):
        try:
            return DataFrameN(self.data / other, self.labels())
        except TypeError:
            return DataFrameN(self._op_helper('truediv',self.data, other), self.labels())

    def __floordiv__(self,other):
        try:
            return DataFrameN(self.data // other, self.labels())
        except TypeError:
            return DataFrameN(self._op_helper('floordiv',self.data, other), self.labels())

    def __pow__(self,other):
        try:
            return DataFrameN(self.data ** other, self.labels())
        except TypeError:
            return DataFrameN(self._op_helper('pow',self.data, other), self.labels())

    def _op_helper(self, op, data, other):
        if type(other) in [list, range, _GEN]:
            raise ValueError('Must use an np.ndarray')

        if type(other) is np.ndarray:
            return self._op_helper_ndarray(op, data, other)
        elif data.ndim != 1:
            return np.array([self._op_helper(op, i, other) for i in data])
        elif data.ndim == 1: # so other is a single number
            temp = []
            for i in data:
                try:
                    temp += [getattr(float(i), '__'+op+'__')(float(other))]
                except (ValueError, TypeError):
                    temp += [i]
            return np.array(temp)
            
    def _op_helper_ndarray(self, op, data1, data2):
        # data1.shape == data2.shape
        if not data1.ndim == 1:
            return np.array([self._op_helper_ndarray(op, data1[i], data2[i]) for i in range(len(data1))])

        if not data1.shape == data2.shape:
            raise Exception('Not same shape arrays')

        temp = []
        for i in range(len(data1)):
            try:
                temp += [getattr(float(data1[i]), '__'+op+'__')(float(data2[i]))]
            except (ValueError, TypeError):
                temp += [data1[i]]
        return np.array(temp)



    def __matmul__(self,other):
        return self.data @ other
    def __mod__(self,other):
        return self.data % other
    def __divmod__(self,other):
        return divmod(self.data,other)
    def __lshift__(self,other):
        return self.data << other
    def __rshift__(self,other):
        return self.data >> other
    def __and__(self,other):
        return self.data & other
    def __xor__(self,other):
        return self.data ^ other
    def __or__(self,data):
        return self.data | other
    
    def __iadd__(self,other):
        self .data= (self + other).data
        return self
    def __isub__(self,other):
        self.data = (self - other).data
        return self
    def __imul__(self,other):
        self.data = (self * other).data
        return self
    def __itruediv__(self,other):
        self.data =  (self / other).data
        return self
    def __ifloordiv__(self,other):
        self.data = (self // other).data
        return self
    
    def __len__(self):
        return len(self.data)
    def __iter__(self):
        return iter(self.data)
    def __reversed__(self):
        return reversed(self.data)
    def __contains__(self,item):
        return item in self.data

    def __lt__(self,other):
        try:
            return DataFrameN(self.data < other, self.labels())
        except TypeError:
            return DataFrameN(self._op_helper('lt',self.data, other), self.labels())

    def __le__(self,other):
        try:
            return DataFrameN(self.data <= other, self.labels())
        except TypeError:
            return DataFrameN(self._op_helper('le',self.data, other), self.labels())

    def __eq__(self,other):
        try:
            return DataFrameN(self.data == other, self.labels())
        except TypeError:
            return DataFrameN(self._op_helper('eq',self.data, other), self.labels())

    def __ne__(self,other):
        try:
            return DataFrameN(self.data != other, self.labels())
        except TypeError:
            return DataFrameN(self._op_helper('ne',self.data, other), self.labels())

    def __gt__(self,other):
        try:
            return DataFrameN(self.data > other, self.labels())
        except TypeError:
            return DataFrameN(self._op_helper('gt',self.data, other), self.labels())

    def __ge__(self,other):
        try:
            return DataFrameN(self.data >= other, self.labels())
        except TypeError:
            return DataFrameN(self._op_helper('ge',self.data, other), self.labels())
    
    def __neg__(self):
        try:
            return DataFrameN(-self.data, self.labels())
        except TypeError:
            return DataFrameN(self._op_helper2('neg',self.data), self.labels())

    def __abs__(self):
        try:
            return DataFrameN(abs(self.data), self.labels())
        except TypeError:
            return DataFrameN(self._op_helper2('abs',self.data), self.labels())

    def _op_helper2(self, op, data):
        if data.ndim != 1:
            return np.array([self._op_helper2(op, i) for i in data])

        temp = []
        for i in data:
            try:
                temp += [getattr(float(i),op)()]
            except ValueError:
                temp += [i]

        return np.array(temp)

    def __round__(self, ndigits=0):
        try:
            return DataFrameN(np.round(self.data,ndigits), self.labels())
        except TypeError:
            return DataFrameN(self._round_helper(self.data,ndigits), self.labels())
            
    def _round_helper(self,data,ndigits):
        if data.ndim > 1:
            return np.array([self._round_helper(i,ndigits) for i in data])
        
        temp = []
        for i in data:
            try:
                temp += [round(float(i),ndigits)]
                if ndigits == 0:
                    temp[-1] = int(temp[-1])
            except ValueError:
                temp += [i]
        return np.array(temp)

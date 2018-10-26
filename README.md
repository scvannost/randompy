# randompy
Random Python snippets that I write

## Items
### DataFrameN.py

Extends/Hybridizes `np.ndarray` and `pd.DataFrame` for an arbitrary number of dimensions.

Includes `read_csv` functionality for 4D or less. Also allows for element-wise algebra for any dtype, only affect those that can be cast as a `float`.

### printer.py

Extends the printer function.

Intended use `from printer.py import *`. Can also import the class and use as `colorprinter.print`.

### benjamini.py

Runs Benjamini-Hochberg corrections for a set of p-values, and returns which tests pass the significance threshold.

### loglikelihood.py

Given an observation matrix, runs a loglikelihood test and returns the p-value. H0 is that all the given rows come from the same set of probabilities, and H1 is that not all of the rows have the same probabilities. By default, it checks -2log(H0/H1) against the chi-squared distribution to get a p-value.

I use this to see if different cell type counts for different samples could have come from the same composition.

Can also be given a list of observation matrices and returns the list of p-values.

###### All maths come from Wikipedia.


## Licensing
This collection of scripts under the umbrella term randompy is code
I wrote in pursuit of my own work while at MIT.  
Copyright (C) 2018 SC van Nostrand

This code is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 3 as
published by the Free Software Foundation.

This code is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

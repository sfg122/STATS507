# ---
# jupyter:
#   jupytext:
#     cell_metadata_json: true
#     notebook_metadata_filter: markdown
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.12.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# ## Topics in Pandas
# **Stats 507, Fall 2021** 
#   

# ## Contents
# Add a bullet for each topic and link to the level 2 title header using 
# the exact title with spaces replaced by a dash. 
#
# + [Missing Data](#Missing-Data)

# ## Missing Data
# I will be looking at how pandas dataframes handle missing values.
# **Stefan Greenberg**
#
# sfgreen@umich.edu


# ## Imports
import numpy as np
import pandas as pd
# ## Detecting missing data
# - missing data includes `NaN`, `None`, and `NaT`
#     - can change settings so that `inf` and -`inf` count as missing
# - `.isna()` returns True wherever there is a missing value
# - `.notna()` returns True wherever there is not a missing value

# +
df = pd.DataFrame([[0.0, np.NaN, np.NaN, 3.0, 4.0, 5.0],
                   [0.0, 1.0, 4.0, np.NaN, 16.0, 25.0]], 
                 index=['n', 'n^2'])

df.append(df.isna())
# -

# ## Filling missing data
#
# - pandas makes it easy to replace missing values intelligently
# - the `.fillna()` method replaces all missing values with a given value
# - the `.interpolate()` method will use neighboring values to fill in gaps
# in data

# +
df_zeros = df.fillna(0)
df_interp = df.copy()

df_interp.loc['n'] = df_interp.loc['n']\
                     .interpolate(method='linear')
df_interp.interpolate(method='quadratic', axis=1, inplace=True)

df_zeros
#df_interp
# -

# ## Remove missing data with `.dropna()`
#
# - `.dropna()` will remove rows or columns that have missing values
# - set `axis` to determine whether to drop rows or columns
# - drop a row or column if it has any missing values or only if it has 
# entirely missing values by setting `how` to either *'any'* or *'all'*
# - set a minimum number of non-missing values required to drop row/column
# by setting `thresh`
# - specify what labels along other aixs to look at using `subset` i.e. 
# only drop a row if there is a missing value in a subset of the columns 
# or vise versa

# +
drop_cols   = df.dropna(axis=1)
drop_all    = df.dropna(how='all')
drop_thresh = df.dropna(thresh=5)
drop_subset = df.dropna(subset=[0, 1, 5])

print(df, '\n\n', 
      drop_cols.shape, drop_all.shape, drop_thresh.shape, drop_subset.shape)
# -
# ## Math operations with missing data
# - cumulative methods - `.cumsum()` and `.cumprod()` - by default will skip 
# over missing values
# - `.sum()` and `.prod()` treat missing values as identities
#     - `.sum()` treats missing values as zero
#     - `.prod()` treats missing values as one
#


# +
sumprod = df.append(
          df.sum()
            .to_frame()
            .transpose()
            .rename(index={0:'sum'}))

sumprod.append(
        df.prod()
          .to_frame()
          .transpose()
          .rename(index={0:'prod'}))


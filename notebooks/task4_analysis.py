#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

get_ipython().run_line_magic('timeit', '[x * 2 for x in range(1000)]')
df = pd.read_csv("../data/employees.csv")
print(df.groupby("department")["salary"].agg(["count", "mean", "max"]))


import xlrd
import numpy as np
import pandas as pd
f=open('comment.csv','r',encoding='utf-8')
data=pd.read_csv(f)
print(data.comment)

#!/usr/bin/env python
# coding: utf-8

# ### Import package, setting package, import data

# In[1]:


import pandas as pd
import numpy as np
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth


# In[2]:


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10000)
pd.options.display.float_format = "{:.2f}".format

np.set_printoptions(threshold=np.inf)


# In[4]:


df = pd.read_csv("df_bersih.csv")
df["Tanggal"] = pd.to_datetime(df["Tanggal"])


# ### Memulai market-basket analysis

# Mengubah bentuk data frame menjadi kelompok list transaksi

# In[ ]:


list_transaksi=[["WAJAN"]]
inside_list = ["TAPISAN"]
for i in range(2,len(df)):
    if df["No.Transaksi"][i] == df["No.Transaksi"][i-1]:
        inside_list.append(df["Kategori Produk"][i])
    else:
        inside_list = list(set(inside_list))
        list_transaksi.append(inside_list)
        inside_list = []
        inside_list.append(df["Kategori Produk"][i])


# Encoding data menjadi dataframe boolean

# In[ ]:


te = TransactionEncoder()
te_ary = te.fit(list_transaksi).transform(list_transaksi)
df_transaksi = pd.DataFrame(te_ary, columns=te.columns_)
df_transaksi


# Eksekusi algoritma fpgrowth dengan batas support minimum 0.3

# In[ ]:


df_fpg = fpgrowth(df_transaksi, min_support=0.03, use_colnames=True)


# In[ ]:


df_fpg_2 = pd.DataFrame(df_fpg['itemsets'].values.tolist(), index=df_fpg.index)
mask = df_fpg_2.astype(str).isin(["KOMPOR","SELANG","KRJG","WADAH","LOYANG"]).any(axis=1)
df_fpg[mask]


# Perhitungan support, confidence, dan lift

# In[ ]:


df_fpg_3 = pd.DataFrame({"Hubungan": ["Kompor->Selang", "Selang->Kompor", "Krjg->Loyang", "Loyang->Krjg","Loyang->Wadah","Wadah->Loyang"],
                        "Support":[0.03,0.03,0.04,0.04,0.03,0.03], "Confidence":[0.03/0.07,0.03/0.06,0.04/0.09,0.04/0.12,0.03/0.12,0.03/0.11],
                        "Lift":[0.03/(0.06*0.07),0.03/(0.06*0.07),0.04/(0.09*0.12),0.04/(0.09*0.12),0.03/(0.12*0.11),0.03/(0.12*0.11)]})
df_fpg_3


# Perhitungan signifikansi kontribusi pendapatan dari produk dengan asosiasi tinggi

# In[ ]:


df_kategori_produk = df[df["Kategori Produk"].isin(["KOMPOR","LOYANG","SELANG","KRJG","WADAH"])].groupby("Kategori Produk")["DPP"].sum()
df_kategori_produk = pd.DataFrame(df_kategori_produk).reset_index()
df_kategori_produk['Persentase DPP'] = df_kategori_produk["DPP"]/df["DPP"].sum()
df_kategori_produk


# In[ ]:


df_kategori_produk2 = df.groupby("Kategori Produk")["DPP"].sum().sort_values(ascending=False)
df_kategori_produk2 = pd.DataFrame(df_kategori_produk2).reset_index()
df_kategori_produk2['Persentase DPP'] = df_kategori_produk2["DPP"]/df["DPP"].sum()
df_kategori_produk2["DPP Kumulatif"] = df_kategori_produk2["DPP"].cumsum()/df_kategori_produk2["DPP"].sum()*100
df_kategori_produk2


# In[ ]:


del df_kategori_produk2, df_kategori_produk, df_fpg_3, df_fpg_2, df_fpg


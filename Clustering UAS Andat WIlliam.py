#!/usr/bin/env python
# coding: utf-8

# ### Import package , data, setting package

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams, cycler
from datetime import datetime as dt


# In[ ]:


from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from mpl_toolkits.mplot3d import Axes3D


# In[ ]:


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10000)
pd.options.display.float_format = "{:.2f}".format

np.set_printoptions(threshold=np.inf)


# In[ ]:


rcParams["figure.figsize"] = 16,8
rcParams["axes.spines.top"] = False
rcParams["axes.spines.right"] = False
rcParams["axes.titlesize"] = "xx-large"
rcParams["axes.labelsize"] = "xx-large"
rcParams["axes.formatter.useoffset"] = False
rcParams["lines.linewidth"] = 2.5
rcParams["xtick.labelsize"] = "large"
rcParams["ytick.labelsize"] = "large"
rcParams["legend.fontsize"] = "xx-large"
rcParams["legend.handlelength"] = 3
rcParams["legend.title_fontsize"] = "xx-large"
plt.style.use("seaborn-white")


# In[ ]:


df = pd.read_csv("df_bersih.csv")
df["Tanggal"] = pd.to_datetime(df["Tanggal"])


# ### Pemeriksaan data singkat

# In[ ]:


df["Kategori Pelanggan"].unique()


# In[ ]:


df.head()


# ### Melihat kontribusi pelanggan per kategori

# In[ ]:


lggn = pd.DataFrame(df[df["Kategori Pelanggan"]=="LGGN"].groupby("Nama Pelanggan")["DPP"].sum().sort_values(ascending=False))
lggn = lggn.reset_index()
lggn["Persentase DPP"] = lggn["DPP"]/lggn["DPP"].sum()
print(len(lggn))
lggn


# In[ ]:


gro = pd.DataFrame(df[df["Kategori Pelanggan"]=="GRO"].groupby("Nama Pelanggan")["DPP"].sum().sort_values(ascending=False))
gro = gro.reset_index()
gro["Persentase DPP"] = gro["DPP"]/gro["DPP"].sum()
print(len(gro))
gro


# In[ ]:


htrsto = pd.DataFrame(df[df["Kategori Pelanggan"]=="HTRSTO"].groupby("Nama Pelanggan")["DPP"].sum().sort_values(ascending=False))
htrsto = htrsto.reset_index()
htrsto["Persentase DPP"] = htrsto["DPP"]/htrsto["DPP"].sum()
print(len(htrsto))
htrsto


# In[ ]:


del gro, htrsto, lggn


# ### Proses clustering

# Persiapan df khusus clustering

# In[ ]:


df_user = df.groupby('Nama Pelanggan')["Tanggal"].max().reset_index()
df_user.columns = ['Nama Pelanggan','Tanggal Terbaru']
df_user['Recency'] = (df_user['Tanggal Terbaru'].max() - df_user['Tanggal Terbaru']).dt.days
df_user = df_user.drop("Tanggal Terbaru", axis=1)


# In[ ]:


df_frequency = df.groupby('Nama Pelanggan')["No.Transaksi"].count().reset_index()
df_frequency.columns = ['Nama Pelanggan','Frequency']
df_user = pd.merge(df_user, df_frequency, on='Nama Pelanggan')
del df_frequency


# In[ ]:


df_mon = df.groupby('Nama Pelanggan')["DPP"].sum().reset_index()
df_mon.columns = ['Nama Pelanggan','Monetary']
df_user = pd.merge(df_user, df_mon, on='Nama Pelanggan')
del df_mon


# In[ ]:


nama_aneh=["GROSIR","HOTEL RESTOR","LANGGANAN","UMUM"]
df_user = df_user[~df_user['Nama Pelanggan'].isin(nama_aneh)]


# In[ ]:


df_user


# In[ ]:


df_user_cluster = df_user.iloc[:,[1,2,3]]
df_user_cluster


# Proses Z-score standarisation

# In[ ]:


sc = StandardScaler()
df_user_cluster = sc.fit_transform(df_user_cluster)
df_user_cluster


# In[ ]:


fig = plt.figure()
ax1 = fig.add_subplot(311, title = "Recency")
ax2 = fig.add_subplot(312, title = "Frequency")
ax3 = fig.add_subplot(313, title = "Monetary")
sns.distplot(df_user_cluster[:,0], ax=ax1)
sns.distplot(df_user_cluster[:,1], ax=ax2)
sns.distplot(df_user_cluster[:,2], ax=ax3)
plt.tight_layout()


# Elbow method untuk menentukan jumlah cluster optimal <BR>
# Kesimpulan : 3 cluster

# In[ ]:


wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
    kmeans.fit(df_user_cluster)
    wcss.append(kmeans.inertia_)
plt.plot(range(1, 11), wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()


# Ekseskusi clustering dengan 3 cluster

# In[ ]:


kmeans = KMeans(n_clusters = 3, init = 'k-means++', random_state = 43)
y_kmeans = kmeans.fit_predict(df_user_cluster)


# Pemeriksaan hasil clustering

# In[ ]:


df_user["Cluster"] = y_kmeans
df_user["Cluster"].value_counts()


# In[ ]:


df_user.groupby("Cluster")[["Recency","Frequency","Monetary"]].mean()


# In[ ]:


sns.boxplot(x="variable", y="value", data=pd.melt(pd.DataFrame(df_user_cluster)))

plt.show()


# Visualisasi hasil clustering dengan t-sne dan 3d scatterplot

# In[ ]:


df_user_tsne = TSNE(n_components=2).fit_transform(df_user_cluster)


# In[ ]:


sns.scatterplot(df_user_tsne[:,0], df_user_tsne[:,1], hue=y_kmeans, legend='full')


# In[ ]:


fig = plt.figure(figsize=(20,11))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df_user_cluster[:,0], df_user_cluster[:,1], df_user_cluster[:,2], c=y_kmeans, marker='o', cmap="jet")
ax.set_xlabel('Recency')
ax.set_ylabel('Frequency')
ax.set_zlabel('Monetary')


plt.show()


# Hasil akhir cluster

# In[ ]:


df_user = pd.merge(df_user,df[["Nama Pelanggan","Kategori Pelanggan"]], how="left", on="Nama Pelanggan")
df_user = df_user.drop_duplicates().reset_index()
df_user


#!/usr/bin/env python
# coding: utf-8

# ### Import package

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams, cycler
import re
from datetime import datetime as dt


# ### Setting package pandas dan numpy

# In[ ]:


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10000)
pd.options.display.float_format = "{:.2f}".format

np.set_printoptions(threshold=np.inf)


# ### Setting package matplotlib

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


# ### Import dataset

# In[ ]:


ori1 = pd.read_csv("1. Data penjualan Sept 2018.csv", thousands=r',')
ori2 = pd.read_csv("2. Data penjualan Okt 2018.csv", thousands=r',')
ori3 = pd.read_csv("3. Data penjualan Nop 2018.csv", thousands=r',')
ori4 = pd.read_csv("4. Data penjualan Des 2018.csv", thousands=r',')
ori5 = pd.read_csv("5. Data penjualan Jan 2019.csv", thousands=r',')
ori6 = pd.read_csv("6. Data penjualan Feb 2019.csv", thousands=r',')
ori7 = pd.read_csv("7. Data penjualan Mar 2019.csv", thousands=r',')
ori8 = pd.read_csv("8. Data penjualan Apr 2019.csv", thousands=r',')
ori9 = pd.read_csv("9. Data penjualan Mei 2019.csv", thousands=r',')
ori10 = pd.read_csv("10. Data penjualan Jun 2019.csv", thousands=r',')
ori11 = pd.read_csv("11. Data penjualan Jul 2019.csv", thousands=r',')
ori12 = pd.read_csv("12. Data penjualan Ags 2019.csv", thousands=r',')

df = pd.concat([ori1,ori2,ori3,ori4,ori5,ori6,ori7,ori8,ori9,ori10,ori11,ori12],axis=0)
df = df.rename(columns={'Kategori':'Kategori Pelanggan','Kategori.1':'Kategori Produk'})
del ori1, ori2, ori3, ori4, ori5, ori6, ori7, ori8, ori9, ori10, ori11, ori12


# ### Eksplorasi data secara umum

# Memeriksa bentuk df, deskripsi statistik umum df

# In[ ]:


df.head()


# In[ ]:


df.shape


# In[ ]:


df.describe()


# In[ ]:


df.describe(include=['object'])


# Memeriksa missing data dalam df serta melakukan visualisasi missing data

# df_missing_data = pd.DataFrame(df.isnull().sum())
# df_missing_data = df_missing_data.reset_index()
# df_missing_data.columns = ["Kolom","Jumlah Missing Data"]
# df_missing_data["Persentase Missing Data"] = df_missing_data["Jumlah Missing Data"]*100/len(df)
# df_missing_data

# In[ ]:


plt.bar(x=df.columns,height=df.isnull().sum()/len(df))
plt.title("Persentase Missing Data", pad = 50)
plt.ylabel("Persentase", labelpad=20)
plt.xlabel("Kolom")
plt.xticks(rotation=90)
plt.yticks()

for i, v in enumerate(df.isnull().sum()/len(df)):
    plt.text(i-0.35, v+0.02, '{:.0f}%'.format(100*v), color='black')


# In[ ]:


del df_missing_data


# ### Pemeriksaan kolom per kolom

# Memeriksa apakah kode pelanggan dan nama pelanggan berpasangan 1 ke 1<br>
# Kesimpulan : Sudah benar

# In[ ]:


kode_pelanggan_dobel = df[["Kode Pelanggan","Nama Pelanggan"]].drop_duplicates()


# In[ ]:


kode_pelanggan_dobel[kode_pelanggan_dobel["Kode Pelanggan"].duplicated(keep=False)]


# In[ ]:


kode_pelanggan_dobel[kode_pelanggan_dobel["Nama Pelanggan"].duplicated(keep=False)]


# In[ ]:


del kode_pelanggan_dobel


# Memeriksa apakah kode produk dan nama produk berpasangan 1 ke 1 <br>
# Kesimpulan : Ada typo di 2 produk, yaitu PERLAK POLOS WRN BR (PERMTR) dan PERLAK POLOS WRN PTH (PERMTR)

# In[ ]:


kode_produk_dobel = df[["Kode Produk","Nama Produk"]].drop_duplicates()


# In[ ]:


kode_produk_dobel[kode_produk_dobel["Nama Produk"].duplicated(keep=False)]


# In[ ]:


kode_produk_dobel[kode_produk_dobel["Kode Produk"].duplicated(keep=False)]


# In[ ]:


del kode_produk_dobel


# Melihat kontribusi setiap pabrik

# In[ ]:


df["Pabrik"] = df["Pabrik"].fillna(-1)
df_pabrik = df.groupby("Pabrik")["DPP"].sum().sort_values(ascending=False)
df_pabrik = pd.DataFrame(df_pabrik).reset_index()
df_pabrik['Persentase DPP'] = df_pabrik["DPP"]/df["DPP"].sum()
df_pabrik["DPP Kumulatif"] = df_pabrik["DPP"].cumsum()/df_pabrik["DPP"].sum()*100
df_pabrik


# In[ ]:


del df_pabrik


# Melakukan drop terhadap berbagai kolom dengan alasan sebagai berikut: <br>
# 1. Kode Pelanggan, Kode Produk, dan No.Bukti memiliki informasi yang sama persis dengan Nama Pelanggan, Nama Produk, dan Kode Transaksi <br>
#     sehingga Kode Pelanggan, Kode Produk, dan No.Bukti dibuang. <br><br>
#     PS: Sebenarnya beberapa kode pelanggan memiliki beberapa informasi menarik, misalnya huruf EXP, nomor telepon,<br>
#     dan Kartu Hilang. Namun karena tak ada data dictionary yang jelas mengenai alasan serta implikasi kode tersebut, <br>
#     maka kode tersebut diabaikan <br><br>
# 2. Unit dan Gudang dianggap tak mengandung informasi yang berarti, maka dibuang <br><br>
# 3. Kode Pos, Kota, No.Faktur Pajak, Jatuh Tempo, No.Pesanan, No.Konsinyasi, No.Peminjaman memiliki terlalu banyak missing data, maka dibuang <br><br>
# 4. Informasi Harga Netto dan Subtotal sudah tersimpan dalam variabel lain, yaitu Qty, Harga Bruto, Diskon, dan DPP, maka dibuang <br><br>
# 5. Pajak, Kode Pajak, dan DPP+Pajak tidak menghasilkan keuntungan untuk perusahaan, maka diabaikan dari analisis <br><br>
# 6. Analis tak tertarik dalam mengukur performa salesman dan operator, maka keduanya diabaikan dari analisis <br><br>

# Selain itu, perlu juga mengubah kolom tanggal menjadi bentuk data baru yaitu date

# In[ ]:


df = df.drop(["Harga Netto","Gudang","Subtotal","Kode Pelanggan","No.Bukti","Kode Produk","Unit","Kode Pajak", "Pajak", "DPP+Pajak","Nama Salesman","Operator","Kode Pos","Kota","No.Faktur Pajak","Jatuh Tempo","No.Pesanan","No.Konsinyasi","No.Peminjaman"],axis=1)
df['Tanggal'] = df['Tanggal'].apply(lambda x: dt.strptime(x, '%d-%m-%Y'))


# Melihat transaksi dengan diskon, namun diskonnya tak 100%

# In[ ]:


df[(df["Diskon"]>0) & (df["Diskon"] != df["Harga Bruto"])]


# ### Membuang kolom yang tak diinginkan

# Membuang produk yang harganya dibawah atau sama dengan Rp 2, yaitu tas plastik

# In[ ]:


df[df["Harga Bruto"]<=2]["Nama Produk"]


# Beberapa transaksi memiliki diskon 100%, sehingga pelanggan membayar 0 Rp. Transaksi ini lebih baik dihilangkan

# In[ ]:


df[df["Diskon"] == df["Harga Bruto"]]


# Eksekusi pembuangan kolom

# In[ ]:


df = df[df["Harga Bruto"]>2]
df = df[df["Diskon"] != df["Harga Bruto"]]


# ### Analisis pendapatan, pelanggan, kategori pelanggan

# Memeriksa tren pendapatan toko Manohara per bulannya

# In[ ]:


df.head()


# In[ ]:


tren_DPP = df.groupby(['Tanggal'])['DPP'].sum()
tren_DPP = tren_DPP.resample('M').sum()
tren_DPP = tren_DPP.reset_index()
tren_DPP = tren_DPP.set_index("Tanggal")
tren_DPP


# In[ ]:


tren_DPP.plot()


# Memeriksa Nama Pelanggan yang tidak terdiri dari angka <br>
# Kesimpulan: Terdapat beberapa nama pelanggan yang aneh, seperti GROSIR, HOTEL RESTO, UMUM, LANGGANAN

# In[ ]:


ada_huruf = re.compile('[a-zA-Z]')
fungsi_ada_huruf = np.vectorize(lambda x:bool(ada_huruf.match(x)))

df["Nama Pelanggan"].unique()[fungsi_ada_huruf(df["Nama Pelanggan"].unique())]


# Ada pula nama pelanggan yang terdiri dari angka

# In[ ]:


df[df["Nama Pelanggan"].str.match('[^a-zA-Z]')]


# Memeriksa nama pelanggan yang memiliki nama persis dengan kategori pelanggan

# In[ ]:


df[df["Nama Pelanggan"]=="UMUM"]


# In[ ]:


df[(df["Kategori Pelanggan"]=="HTRSTO") & (df["Nama Pelanggan"]=="HOTEL RESTO")]


# In[ ]:


df[(df["Kategori Pelanggan"]=="LGGN") & (df["Nama Pelanggan"]=="LANGGANAN")]


# In[ ]:


df[(df["Kategori Pelanggan"]=="GRO") & (df["Nama Pelanggan"]=="GROSIR")]


# Membandingkan kontribusi setiap kategori pelanggan

# In[ ]:


kategori_pelanggan = pd.DataFrame(df.groupby("Kategori Pelanggan")["DPP"].sum())
lala = pd.DataFrame(df.groupby("Kategori Pelanggan")["No.Transaksi"].nunique())
lala.reset_index(level=0, inplace=True)
kategori_pelanggan = pd.merge(kategori_pelanggan,lala, on='Kategori Pelanggan', how='left')
del lala
kategori_pelanggan["Revenue/Order"] = kategori_pelanggan["DPP"]/kategori_pelanggan["No.Transaksi"]
kategori_pelanggan["Persentase DPP"]= kategori_pelanggan["DPP"]/kategori_pelanggan["DPP"].sum()
kategori_pelanggan["Persentase Transaksi"]= kategori_pelanggan["No.Transaksi"]/kategori_pelanggan["No.Transaksi"].sum()
kategori_pelanggan = kategori_pelanggan[['Kategori Pelanggan', 'DPP', 'Persentase DPP', 'No.Transaksi', 'Persentase Transaksi','Revenue/Order']]
kategori_pelanggan


# Membandingkan dan visualisasi tren kontribusi setiap kategori pelanggan

# In[ ]:


tren_kategori_pelanggan = df.groupby(['Tanggal','Kategori Pelanggan'])['DPP'].sum()
tren_kategori_pelanggan = pd.DataFrame(tren_kategori_pelanggan)
tren_kategori_pelanggan.reset_index(level=['Tanggal','Kategori Pelanggan'], inplace= True)
tren_kategori_pelanggan = tren_kategori_pelanggan.pivot(index="Tanggal",columns="Kategori Pelanggan")['DPP']
tren_kategori_pelanggan = tren_kategori_pelanggan.resample('M').sum()
tren_kategori_pelanggan = tren_kategori_pelanggan.reset_index()
tren_kategori_pelanggan = tren_kategori_pelanggan.set_index("Tanggal")
tren_kategori_pelanggan


# In[ ]:


tren_kategori_pelanggan.plot()
plt.ylabel("Total DPP", labelpad=20)


# Visualisasi distribusi kontribusi pelanggan selama setahun khusus pelanggan grosir, langganan, dan hotel resto

# In[ ]:


fig = plt.figure()
ax1 = fig.add_subplot(311, title="Grosir")
ax2 = fig.add_subplot(312, title="Langganan")
ax3 = fig.add_subplot(313, title="Hotel / Restoran")
sns.distplot(df[df["Kategori Pelanggan"]=="GRO"].groupby('Nama Pelanggan')[["DPP"]].sum().sort_values(by="DPP", ascending = False), norm_hist=False, ax=ax1)
sns.distplot(df[df["Kategori Pelanggan"]=="LGGN"].groupby('Nama Pelanggan')[["DPP"]].sum().sort_values(by="DPP", ascending = False), norm_hist=False, ax=ax2)
sns.distplot(df[df["Kategori Pelanggan"]=="HTRSTO"].groupby('Nama Pelanggan')[["DPP"]].sum().sort_values(by="DPP", ascending = False), ax=ax3)
plt.tight_layout()


# In[ ]:


sns.distplot(df[df["Kategori Pelanggan"]=="GRO"].groupby('Nama Pelanggan')[["DPP"]].sum().sort_values(by="DPP", ascending = False), norm_hist=False)


# In[ ]:


sns.distplot(df[df["Kategori Pelanggan"]=="LGGN"].groupby('Nama Pelanggan')[["DPP"]].sum().sort_values(by="DPP", ascending = False), norm_hist=False)


# In[ ]:


sns.distplot(df[df["Kategori Pelanggan"]=="HTRSTO"].groupby('Nama Pelanggan')[["DPP"]].sum().sort_values(by="DPP", ascending = False))


# ### Eksport data untuk tahap berikutnya

# In[ ]:


df.to_csv('df_bersih.csv', index=False)


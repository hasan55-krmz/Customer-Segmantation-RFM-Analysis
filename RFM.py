##########

import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None)

df_ = pd.read_excel("online_retail_II.xlsx",sheet_name="Year 2010-2011")
df = df_.copy()

df.head()
df.shape
df.info()

df.isnull().sum()
df.dropna(inplace = True)

df.describe([0.05,0.1,0.25,0.5,0.75,0.90,0.95,0.99]).T

df = df[~df["Invoice"].str.contains("C", na=False)]
df.head()

df["TotalPrice"] = df["Quantity"]*df["Price"]


df["InvoiceDate"].max()
todaydate = dt.datetime(2011,12,11)

rfm = df.groupby("Customer ID").agg({"InvoiceDate": lambda date:(todaydate-date.max()).days,
                                     "Invoice": lambda num: len(num),
                                     "TotalPrice":lambda TotalPrice: TotalPrice.sum()})

rfm.head()
rfm.columns = ["Recency", "Frequency","Monetary"]

rfm["RecencyScore"] = pd.qcut(rfm["Recency"],5,labels=[5,4,3,2,1])
rfm["FrequencyScore"] = pd.qcut(rfm["Frequency"], 5, labels=[1,2,3,4,5])
rfm["MonetaryScore"] = pd.qcut(rfm["Monetary"], 5, labels=[1,2,3,4,5])

rfm.head()

rfm["RFM_Score"] = (rfm["RecencyScore"].astype(str)+rfm["FrequencyScore"].astype(str)+rfm["MonetaryScore"].astype(str))

rfm["Segment"] = (rfm["RecencyScore"].astype(str)+rfm["FrequencyScore"].astype(str))


seg_map = {
    r'[1-2][1-2]': 'Hibernating',
    r'[1-2][3-4]': 'At_Risk',
    r'[1-2]5': 'Cant_Loose',
    r'3[1-2]': 'About_to_Sleep',
    r'33': 'Need_Attention',
    r'[3-4][4-5]': 'Loyal_Customers',
    r'41': 'Promising',
    r'51': 'New_Customers',
    r'[4-5][2-3]': 'Potential_Loyalists',
    r'5[4-5]': 'Champions'
}

rfm['Segment'] = rfm['Segment'].replace(seg_map, regex=True)
rfm.head()


rfm[["Segment","Recency", "Frequency","Monetary"]].groupby("Segment").agg(["mean","count"])

rfm[rfm["Segment"] == "Loyal_Customers"].head()
rfm[rfm["Segment"] == "Loyal_Customers"].index

new_df = pd.DataFrame()

new_df["Loyal Customers"] = rfm[rfm["Segment"] == "Loyal_Customers"].index

new_df.to_excel("Loyal Customers.xlsx")
new_df.head()



Segment_Table=pd.DataFrame(rfm[["Segment","Recency", "Frequency","Monetary"]].groupby("Segment").agg(["mean","count"]))

Segment_Table.head()
Segment_Table.to_excel("Segmentler.xlsx")

##########################################################################
# Yorunlama
##########################################################################

df.head()
rfm.head()

# Her bir Gruba Ait,  Satış Verisinden Gözlemleri Çekmek için bir Fonksiyon Yazdım

def rfm_group(rfm_group):
    indeksler =[df[df["Customer ID"] == i].index for i in rfm[rfm["Segment"] == rfm_group].index]
    son = []
    for i in range(len(indeksler)):
        for j in range(len(indeksler[i])):
            son.append(indeksler[i][j])
    df_rfmg = df.loc[son]
    return df_rfmg
#################################
new_df1 = pd.DataFrame
new_df1["Customer ID"] = rfm[rfm["Segment"] == "Loyal_Customers"].index
pd.merge(df, new_df1, on='Customer ID', how='inner')

rfm_group("Loyal_Customers")
del new_df
rfm[rfm["Segment"] == "Loyal_Customers"].index


rfm.loc[new_df["Loyal Customers"]]


rfm[rfm["Segment"] == "Loyal_Customers"].index
rfm_

new_df.dtypes
new_df

new_df = new_df.astype("int")


loyal_customer=rfm_group("Loyal_Customers")

at_risk = rfm_group("At_Risk")

cant_loose = rfm_group("Cant_Loose")

need_attention = rfm_group("Need_Attention")

at_risk.groupby("StockCode").agg({"Invoice":"count","Quantity":"sum","TotalPrice":"sum"}).sort_values(by="TotalPrice", ascending = False)

loyal_customer["TotalPrice"].sum()

# Her bir gruba ait satış verisindeki ürünlere göre inceleme yapmak için bir fonksiyon yazdım
def urun_inceleme(group_name):
    data = rfm_group(group_name)
    data1=data.groupby("StockCode").agg({"Invoice":"count","Quantity":"sum","TotalPrice":"sum"}).sort_values(by="TotalPrice", ascending = False)
    toplam_fiyat = data1["TotalPrice"].sum()
    data1["Tot_pri_percent"] = data1["TotalPrice"]*100/toplam_fiyat
    data1["Per_cumsum"] = data1["Tot_pri_percent"].cumsum()
    print(data1)
    return data1

At_Risk =urun_inceleme("At_Risk")
At_Risk[At_Risk["Per_cumsum"]<=80]

785/2908


Cant_Loose = urun_inceleme("Cant_Loose")
Cant_Loose[Cant_Loose["Per_cumsum"]<=80]
725/2485


Need_Attention = urun_inceleme("Need_Attention")
Need_Attention[Need_Attention["Per_cumsum"]<=80]

Hibernating = urun_inceleme("Hibernating")
Hibernating[Hibernating["Per_cumsum"] <=80]

Loyal_Customer = urun_inceleme("Loyal_Customers")
Loyal_Customer[Loyal_Customer["Per_cumsum"]<=80]

# Her bir ortak ürünü bulmak adına bu işlemi yaptım
indeks_urun = []
for i in Loyal_Customer[Loyal_Customer["Per_cumsum"]<=80].index:
    if i in Need_Attention[Need_Attention["Per_cumsum"]<=80].index & At_Risk[At_Risk["Per_cumsum"]<=80].index:
        indeks_urun.append(i)

len(Need_Attention[Need_Attention["Per_cumsum"]<=80].index)


# Bulduğum ortak ürürnleri Tüm veri seti açısında inceledim
df_urun =df.groupby("StockCode").agg({"Invoice":"count","Quantity":"sum","TotalPrice":"sum"}).sort_values(by="TotalPrice", ascending = False)
df.head()
toplam_fiyat = df["TotalPrice"].sum()
df_urun["Tot_pri_percent"] =df_urun["TotalPrice"]*100/toplam_fiyat
df_urun["Per_cumsum"] = df_urun["Tot_pri_percent"].cumsum()
print(df_urun)

df_sekseklin_urun=[]
for i in indeks_urun:
    if i in df_urun[df_urun["Per_cumsum"]<=80].index:
        df_sekseklin_urun.append(i)


len(df_urun[df_urun["Per_cumsum"]<=80].index)
len(df_sekseklin_urun)


pd.DataFrame(df_sekseklin_urun).to_excel("Yüzde_Seksenlikde_urunler.xlsx")

df_urun.loc[df_sekseklin_urun]["Tot_pri_percent"].sum()

new_df = pd.DataFrame()
new_df["Customer ID"] = pd.DataFrame([rfm["Segment"] == "Loyal_Customers"].index)
pd.merge(df, new_df, on='Customer ID', how='inner')

new_df["Customer ID"] = rfm[rfm["Segment"] == "Loyal_Customers"].index
pd.merge(df, new_df, on='Customer ID', how='inner').groupby(["Customer ID"]).agg({"Invoice": "count"})

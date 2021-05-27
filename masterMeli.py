#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import unidecode


# In[2]:

title_container = st.beta_container()
col1, col2 = st.beta_columns([1, 20])
with title_container:
    with col1:
        st.image("https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_170,w_170,f_auto,b_white,q_auto:eco/v1456160088/dauw8qmiutpmqx4wvwlf.png")
    with col2:
        st.markdown('<h1 style="color: purple;">Buscador de precios</h1>',
                    unsafe_allow_html=True)


# In[3]:


keywords_input = st.text_input("Búsqueda", "Ingrese una búsqueda")


# In[62]:


categories_dict_final = pd.read_csv("categories.csv")


# In[63]:


def _base(keywords_input):
    keywords_input= keywords_input[0].upper()+keywords_input[1:].lower()
    keywords = unidecode.unidecode(keywords_input).replace(" ","+")
    url = "https://api.mercadolibre.com/sites/MLA/search?q="+keywords+"&limit=50&currencies=AR" 
    response = requests.get(url)
    results_1=pd.DataFrame(response.json()["results"])
    
    categories = results_1['category_id'].value_counts()[results_1['category_id'].value_counts()>1].index
    
    base_final = pd.DataFrame()
    for cat in categories: 
#     for cat in [categories[0]]:
        try:
            url_cat = url+"&category="+cat
            response = requests.get(url_cat)
            results_cat=pd.DataFrame(response.json()["results"])
            results_cat = results_cat[results_cat['sold_quantity']>0]
            base_final=base_final.append(results_cat)
        except:
            pass
    
    base_final['condition']=base_final['condition'].replace({'new':'Nuevo','used':'Usado'})
    base_final.reset_index(drop=True,inplace=True)
    base_final=base_final.merge(categories_dict_final,on='category_id',how='left')
    base_final=base_final[['id','price','category_name','sold_quantity','condition']]

    base_final.dropna(inplace=True)
    base_final.drop_duplicates(inplace=True)
    base_final['keywords_input']=keywords_input
    return base_final


# In[64]:


def _chart(base):
    base_final = base.copy()
    keywords_input = base_final['keywords_input'].unique()[0]
    
    categories = base_final['category_name'].unique()
    ncharts = base_final['category_name'].nunique()
    nbins = 20 if ncharts==1 else ncharts*15

    base_final['Porcentaje']=base_final.groupby('category_name')['sold_quantity'].apply(lambda x: x/x.sum())
    base_final = base_final[base_final['Porcentaje']>0.01].copy()
    base_final['Porcentaje']=base_final.groupby('category_name')['sold_quantity'].apply(lambda x: x/x.sum())
    base_final['Porcentaje']=(base_final['Porcentaje']*100).astype(int)

    fig = px.histogram(x=base_final['price'],y=base_final['Porcentaje'],color=base_final['category_name'],
                       nbins=nbins,barmode="overlay")

    fig.layout.update(showlegend=True,
                      hovermode="closest",
                      hoverlabel=dict(bgcolor="white"),
                      legend = {"title":{'text':"Categoría"}}) 

    fig.update_traces(hovertemplate ='<b>Rango de precios</b>: '+'%{x}'+'<extra></extra><br><b>Porcentaje de unidades vendidas</b>: '+'%{y}'+"%",
                      selector=dict(type="histogram"))

    
    fig.update_xaxes({"title": {"text": "Precio"}},visible=True)
    fig.update_yaxes({"title": {"text": "Porcentaje de unidades vendidas"}})
    fig.update_layout(title={'text': "Búsqueda: "+keywords_input,
                            'x':0.5,'xanchor': 'center','yanchor': 'top','font':{'size':16}})
    
    

    st.plotly_chart(fig)
    fig.show()


# In[65]:


def _table(base_final):
    categories = base_final['category_name'].unique()    
    lista_precio_promedio= []
    for cat in categories:
        base_cat = base_final[base_final['category_name']==cat]
        precio_promedio = (base_cat['price']*base_cat['sold_quantity']).sum()/base_cat['sold_quantity'].sum()
        precio_promedio_currency = "${:,.2f}". format(precio_promedio).split(".")[0].replace(",",".")
        ventas=base_cat['sold_quantity'].sum()
        publicaciones=base_cat.shape[0]
        lista_precio_promedio.append([cat,publicaciones,ventas,precio_promedio_currency])
    
    lista_final = pd.DataFrame(lista_precio_promedio,columns=['Categoría','Publicaciones','Ventas','Precio promedio ponderado'])
    st.text('Publicaciones analizadas:')
    st.dataframe(lista_final)


# In[93]:


if keywords_input!="Ingrese una búsqueda":
    base = _base(keywords_input)
    _chart(base)
    _table(base)
else:
    base = _base("Televisor 50 pulgadas")
    _chart(base)
    _table(base)    



#!/usr/bin/env python
# coding: utf-8

# In[52]:


from datetime import datetime
import requests
import pandas as pd
import streamlit as st
import plotly.express as px


# In[53]:


st.write("""
## Buscador de precios
""")


# In[54]:


keywords_input = st.text_input("Búsqueda", "Ingrese una búsqueda")


# In[55]:


url_dict = "https://api.mercadolibre.com/sites/MLA/"
response = requests.get(url_dict)
results_dict=pd.DataFrame(response.json()['categories'])
results_dict.rename(columns={'id':'category_id','name':'category_name'},inplace=True)


# In[60]:


def chart(keywords_input):
    keywords_input= keywords_input[0].upper()+keywords_input[1:].lower()
    keywords = keywords_input.replace(" ","+")
    url = "https://api.mercadolibre.com/sites/MLA/search?q="+keywords+"&condition=new&limit=50" 
    response = requests.get(url)
    results_1=pd.DataFrame(response.json()["results"])
    categories = results_1['category_id'].value_counts()[results_1['category_id'].value_counts()>5].index
    
    url_cat = url+"&category="+categories[0]  
    response = requests.get(url_cat)
    base_final=pd.DataFrame(response.json()["results"])
    
    if len(categories)>1:
        for cat in categories[1:]:
            url_cat = url+"&category="+cat
            response = requests.get(url_cat)
            results_cat=pd.DataFrame(response.json()["results"])
            base_final=base_final.append(results_cat)
    
    base_final.reset_index(drop=True,inplace=True)
    base_final=base_final.merge(results_dict,on='category_id',how='left')
    
    fig = px.histogram(base_final['price'],base_final['category_name'],histnorm="percent",nbins=20)# y="tip", color="sex", marginal="rug",hover_data=df.columns
    fig.layout.update(showlegend=True, 
                      legend = {"title":{'text':""}},
                      yaxis =  {"title": {"text": "Densidad"}},
                      xaxis =  {"title": {"text": "Precio"}},
                      title={'text': keywords_input,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'}
                     ) 
    st.plotly_chart(fig)
    return base_final


# In[65]:


if keywords_input!="Ingrese una búsqueda":
    chart(keywords_input)
else:
    chart("Televisor 40 pulgadas")



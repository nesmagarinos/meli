#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datetime import datetime
import requests
import pandas as pd
import streamlit as st
import plotly.express as px


# In[2]:


st.write("""
# Titulo de prueba

Script de MeLi
""")


# In[3]:


keywords_input = st.text_input("Búsqueda", "Ingrese una búsqueda")


# In[4]:


def chart(keywords_input):
    keywords_input= keywords_input[0].upper()+keywords_input[1:].lower()
    keywords = keywords_input.replace(" ","+")
    url = "https://api.mercadolibre.com/sites/MLA/search?q="+keywords+"&condition=new&limit=50"  # Endpoint a consultar
    response = requests.get(url)
    results=pd.DataFrame(response.json()["results"])

    fig = px.histogram(results['price'],histnorm="percent",nbins=10)# y="tip", color="sex", marginal="rug",hover_data=df.columns
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


# In[5]:


if keywords_input!="Ingrese una búsqueda":
    chart(keywords_input)





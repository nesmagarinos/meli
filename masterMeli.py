#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datetime import datetime
import requests
import json
import pandas as pd


# In[56]:


url = "https://api.mercadolibre.com/sites/MLA/search?q=nintendo+switch&condition=new&limit=50"  # Endpoint a consultar
response = requests.get(url)


# In[61]:


data = json.loads(response.text)
results=pd.DataFrame(data["results"])


# In[63]:


results.columns


# In[62]:


resultsa


# In[ ]:





#!/usr/bin/env python
# coding: utf-8

# In[69]:


from datetime import datetime
import requests
import json
import pandas as pd
import seaborn as sns


# In[56]:


url = "https://api.mercadolibre.com/sites/MLA/search?q=nintendo+switch&condition=new&limit=50"  # Endpoint a consultar
response = requests.get(url)


# In[61]:


data = json.loads(response.text)
results=pd.DataFrame(data["results"])


# In[71]:


sns.histplot(results['price'])


# In[72]:


#get_ipython().system(' jupyter nbconvert --to script masterMeli.ipynb')


# In[ ]:





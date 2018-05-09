
# coding: utf-8

# In[112]:


from pymongo import MongoClient
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import statistics


# In[3]:


#mongodb config
client = MongoClient('localhost', 27017)
db = client['typeaidata']
collection = db['typist1']


# In[4]:


# Get typed data
query = {'corrections': {'$gt': 0}, 'text':{'$ne': ''}}
projection = {'corrections':1, 'text':1, 'typedlist':1, '_id':0}
query = collection.find(query, projection)
df =  pd.DataFrame(list(query))
df


# In[5]:


# Check for text
for i in range(len(df)):
    x = df['text'][i].split()
    st =  ' '.join(x)
    print('\n',st)


# In[6]:


# Check for typed text
for i in range(len(df)):
    x = ''.join(df['typedlist'][i]).split()
    st =  ' '.join(x)
    print('\n',st)


# In[7]:


# Clean column text and typedlist in typist data
rows = len(df)
for i in range(rows):
    df.text[i] = ' '.join(df.text[i].split())
    c = df.text[i][0]
    pos = 0
    while((df.typedlist[i][pos:])[0] != c):
        pos = pos + 1
    df.typedlist[i] = df.typedlist[i][pos:]
df


# In[8]:


# Preprocess cleaned column typedlist
df['typed'] = ''
for i in range(rows):
    temp = (''.join(df['typedlist'][i])).split()
    df['typed'][i] =  ' '.join(temp)
del df['typedlist']
df


# In[13]:


df.text[1]


# In[30]:


df.typed[1]


# In[92]:


# Generate a list of incorrect words with their frequency

bag = []
count = []

for i in range(rows):
    txt = df.text[i]
    typ = df.typed[i]
    words = txt.split()
    words2 = txt.split()
    counter = 0
    j = 0
    k = 0
    temp = ''
    while(j < len(words) and k < len(typ)):
        c = typ[k]
        if(c=='\x08' or c=='\r' or c=='\x01'):
            temp = temp[:-1]
            counter += 1
        else:
            temp = temp + str(c)
        if(temp.strip() == words[j]):
            bag.append(words[j])
            count.append(counter)
            temp = ''
            j+=1
            counter = 0
        k += 1


# In[93]:


list(zip(bag, count))


# In[ ]:


# Graph of bag vs count


# In[125]:


# Normalizing the count of incorrect words (method 1)
diff = float(max(count) - min(count))
count_normalized = [int(round((i/diff)*5))+1 for i in count]
list(zip(bag, count_normalized))


# In[ ]:


# Graph of bag vs normalized count


# In[126]:


# Generate curated text for obtaining the training data (for method 1)
with open('curated_v1.txt', 'w') as f:
    for temp in zip(bag, count_normalized):
        lst = [temp[0]] * temp[1]
        st = ' '.join(lst)
        f.write(st + ' ')


# In[102]:


# Calculate the mode of the words
incorrect_count = []
for i in count:
    if(i>0):
        incorrect_count.append(i)
temp = Counter(incorrect_count)
mode = temp.most_common()
mode


# In[124]:


# Graph of mode data (Incorrections vs Words)


# In[108]:


# Z-score Calculation
mean = sum(count)/len(count)
std = statistics.stdev(count)
zscore = [(i-mean)/std for i in count]
zscore


# In[122]:


# Graph of bag vs zscore
plt.figure()
plt.title('Bag vs Z-Score')
plt.plot(count, zscore, color='blue', marker='o', linestyle='-', linewidth=1, markersize=4)
plt.show()


# In[127]:


# Normalizing the count of incorrect words (method 2)
diff = float(max(zscore) - min(zscore))
count_normalized = [int(round((i/diff)*5))+1 for i in zscore]
list(zip(bag, count_normalized))


# In[128]:


# Normalizing the count of incorrect words (method 2)
with open('curated_v2.txt', 'w') as f:
    for temp in zip(bag, count_normalized):
        lst = [temp[0]] * temp[1]
        st = ' '.join(lst)
        f.write(st + ' ')


# In[ ]:


# End-of-file


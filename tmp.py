from IPython.display import SVG
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pdb

df = pd.read_csv('행정구역_시군구_별__성별_인구수_2011_2020', header=[0,1], index_col=0)
state_arr = np.unique([col for col in df.index if col !='전국'])
print(state_arr)

people_dict = {}
for state in state_arr:
    people_201101 = df.loc[state]['2011. 01']['총인구수 (명)']
    people_202005 = df.loc[state]['2020. 05']['총인구수 (명)']
    if people_201101=='-':
        people_201101 = '1'
    if people_202005=='-':
        people_202005 = '1'
    diff_people = int(people_202005.replace(',','')) - int(people_201101.replace(',',''))
    people_dict[state]= [int(people_202005.replace(',','')), int(people_201101.replace(',','')), diff_people]


df = pd.DataFrame.from_dict(people_dict, orient='index', columns=['2011_01','2020_05','변화인구수'])


df['인구변화율'] = (df['2020_05'] - df['2011_01']) / df['2011_01'] * 100

limit = df['인구변화율'].quantile(0.94) # 94% 해당하는 값
df['인구변화율_정규'] = df['인구변화율'].apply(lambda x : limit if x > limit else x)


fig = plt.figure()
ax1 = fig.add_subplot(211) #2행 1열 1번
ax2 = fig.add_subplot(212) #2행 1열 2번
#bins = 도수분포구간(7개)
ax1.hist(df['인구변화율'], bins=7)
ax1.legend(['인구변화율'])
# bins = 도수분포구간(7개)
ax2.hist(df['인구변화율_정규'], bins=7)
ax2.legend(['인구변화율_정규'])
plt.show()
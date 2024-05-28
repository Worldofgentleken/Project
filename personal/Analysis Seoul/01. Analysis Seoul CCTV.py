import pandas as pd
# CCTV 데이터 읽어오기
CCTV_Seoul = pd.read_csv('../data/01. Seoul_CCTV.csv', encoding = 'utf-8')
CCTV_Seoul.head() # head() : 앞부분 5개만 보고 싶어!

CCTV_Seoul.columns

CCTV_Seoul.columns
Index(['순번', '구분', '총 계', '2015년 이전 설치된 CCTV', '2015년', '2016년', '2017년',
       '2018년', '2019년', '2020년', '2021년', '2022년', '2023년'],
      dtype='object')
CCTV_Seoul.columns[0]

CCTV_Seoul.rename(columns = {CCTV_Seoul.columns[1] : '구별'}, inplace = True)
CCTV_Seoul.head()

CCTV_Seoul = CCTV_Seoul.drop(['순번'], axis = 1)
CCTV_Seoul.head()

CCTV_Seoul.rename(columns = {CCTV_Seoul.columns[2] : '2015년 이전 설치'}, inplace = True)
CCTV_Seoul.head()

CCTV_Seoul.info()
CCTV_Seoul.loc[:, '총 계':'2023년'] = CCTV_Seoul.loc[:, '총 계':'2023년'].applymap(lambda x: int(x.replace(',', '')))
CCTV_Seoul.head()

CCTV_Seoul.sort_values(by = '총 계', ascending=True).head()
CCTV_Seoul.sort_values(by = '총 계', ascending=False).head()

print(CCTV_Seoul['2015년 이전 설치'].unique())
CCTV_Seoul.sort_values(by = '최근증가율', ascending = False)

CCTV_Seoul = CCTV_Seoul.drop([0])
CCTV_Seoul

# 서울 인구 데이터 읽어오기
pop_Seoul = pd.read_excel('../data/01. Seoul_Population.xlsx')
pop_Seoul.head()

pop_Seoul = pd.read_excel('../data/01. Seoul_Population.xlsx',header = 2, usecols = 'B, D, G, J, N')
pop_Seoul.head()

pop_Seoul.rename(columns = {
    pop_Seoul.columns[0]: '구별',
    pop_Seoul.columns[1]: '인구수',
    pop_Seoul.columns[2]: '한국인',
    pop_Seoul.columns[3]: '외국인',
    pop_Seoul.columns[4]: '고령자',
    }, inplace = True)
pop_Seoul.head()
pop_Seoul.tail()

pop_Seoul = pop_Seoul.drop([0])
pop_Seoul

pop_Seoul['구별'].unique()
len(pop_Seoul['구별'].unique())

pop_Seoul['외국인비율'] = pop_Seoul['외국인'] / pop_Seoul['인구수'] * 100
pop_Seoul['고령자비율'] = pop_Seoul['고령자'] / pop_Seoul['인구수'] * 100
pop_Seoul.head()

pop_Seoul.sort_values(by = '인구수', ascending=False).head()
pop_Seoul.sort_values(by = '외국인', ascending=False).head()
pop_Seoul.sort_values(by = '외국인비율', ascending=False).head()
pop_Seoul.sort_values(by = '고령자비율', ascending=False).head()
pop_Seoul.sort_values(by = '고령자', ascending=False).head()

# 데이터 병합
data_result = pd.merge(CCTV_Seoul, pop_Seoul, on='구별')
data_result.head()

# 년도별 컬럼 삭제
del data_result['2015년 이전 설치']
del data_result['2015년']
del data_result['2016년']
del data_result['2017년']
del data_result['2018년']
del data_result['2019년']
del data_result['2020년']
del data_result['2021년']
del data_result['2022년']
del data_result['2023년']

data_result

data_result.set_index('구별', inplace=True)
data_result.head()

# 상관계수가 0.2 이상인 데이터 비교
data_result.corr()

# 인구대비 CCTV 비율을 보기 위해 CCTV 비율 컬럼 생성
data_result['CCTV비율'] = data_result['총 계'] / data_result['인구수'] * 100
data_result.head()
data_result.sort_values(by = 'CCTV비율', ascending=False).head()
data_result.sort_values(by = 'CCTV비율').head()

# 데이터 시각화
import matplotlib.pyplot as plt
from matplotlib import rc
plt.rcParams['axes.unicode_minus'] = False
rc('font', family = 'Arial Unicode MS')
get_ipython().run_line_magic('matplotlib', 'inline')
data_result.head()

# 총계 컬럼 시각화
data_result['총 계'].plot(kind = 'barh', grid = True, figsize = (10, 10));

# CCTV가 많은 구 시각화
def drawGraph():
    data_result['총 계'].sort_values().plot(
        kind = 'barh', grid = True, title = '가장 CCTV가 많은 구', figsize = (10, 10));

drawGraph()

data_result.head()

# CCTV 비율이 높은 구 시각화
    data_result['CCTV비율'].sort_values().plot(
        kind = 'barh', grid = True, title = '가장 CCTV 비율이 높은 구', figsize = (10, 10));

# 데이터 경향 탐색
# 인구수와 총계 컬럼으로 sctter plot으로 시각화
def drawGraph():

    plt.figure(figsize = (14, 10))
    plt.scatter(data_result['인구수'],data_result['총 계'], s = 50)
    plt.xlabel = '인구수'
    plt.ylabel = 'CCTV'
    plt.grid(True)
    plt.show()

drawGraph()

# numpy를 이용 1차 직선 생성
import numpy as np
population = np.array(data_result['인구수'], dtype=float)
total = np.array(data_result['총 계'], dtype=float)

coefficients = np.linalg.lstsq(np.vstack([population, np.ones_like(population)]).T, total, rcond=None)[0]
slope, intercept = coefficients

f1 = np.poly1d(coefficients)
f1

# 인구수 40만 구 기준 서울시 전체 경향에 맞는 적당한 CCTV 수 탐색
f1(400000)

# 경향선을 그리기 위한 데이터 생성
fx = np.linspace(100000, 700000, 100)

# 경향선 생성
def drawGraph():

    plt.figure(figsize = (14, 10))
    plt.scatter(data_result['인구수'],data_result['총 계'], s = 50)
    plt.plot(fx, f1(fx), ls = 'dashed', lw = 3, color = 'g')
    plt.xlabel = '인구수'
    plt.ylabel = 'CCTV'
    plt.grid(True)
    plt.show()

drawGraph()

# 강조 데이터 시각화
data_result['오차'] = data_result['총 계'] - f1(data_result['인구수'])
data_result.head()

df_sort_f = data_result.sort_values(by = '오차', ascending= False)
df_sort_t = data_result.sort_values(by = '오차', ascending= True)
df_sort_f.head()
df_sort_t.head()

from matplotlib.colors import ListedColormap
# colormap 을 사용자 정의로 커스텀 세팅
color_step = ['#e74c3c', '#2ecc71', '#95a9a6', '#2ecc71', '#3498db', '#3498db']
my_cmap = ListedColormap(color_step)
data_result

#상위 5개구 및 하위 5개구 강조
def drawGraph():

    plt.figure(figsize = (14, 10))
    plt.scatter(data_result['인구수'],data_result['총 계'], s = 50, c = data_result['오차'], cmap = my_cmap)
    plt.plot(fx, f1(fx), ls = 'dashed', lw = 3, color = 'g')
    for n in range(5):
        plt.text(
            df_sort_f['인구수'][n] * 1.02,
            df_sort_f['총 계'][n] * 0.98,
            df_sort_f.index[n],
            fontsize = 15
        )
    for n in range(5):
        plt.text(
            df_sort_t['인구수'][n] * 1.02,
            df_sort_t['총 계'][n] * 0.98,
            df_sort_t.index[n],
            fontsize = 15
        )
    plt.xlabel = '인구수'
    plt.ylabel = 'CCTV'
    plt.colorbar()
    plt.grid(True)
    plt.show()

drawGraph()

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

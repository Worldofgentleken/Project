
import numpy as np
import pandas as pd

# 데이터 읽기
crime_raw_data = pd.read_csv('../data/02. crome_in_Seoul.csv', thousands = ',', encoding = 'euc-kr')
crime_raw_data.head()

# 데이터 개요 확인
crime_raw_data.info()

# null 값이 있는지 확인
crime_raw_data['죄종'].unique
crime_raw_data.isnull()

crime_raw_data.head()

# 서울시 범죄 현황 데이터 정리
crime_station = crime_raw_data.pivot_table(
    crime_raw_data, 
    index = '구분', 
    columns= ['죄종', '발생검거'], 
    aggfunc = np.sum)
crime_station = crime_station.fillna(0)
crime_station

crime_station.columns
crime_station['건수', '강도', '검거'][:5]

# 건수 제거
crime_station.columns = crime_station.columns.droplevel(0)
crime_station.columns
crime_station

# 현재 인덱스가 경찰서 이름으로 되어 있음
# 구 이름을 찾아야함
crime_station.index

# Google Maps를 이용한 데이터 정리
import googlemaps
gmaps_key = 'AIzaSyCnTTJgg19JeTWrX3Yl4TH-6G99ONeBLkI'
gmaps = googlemaps.Client(key = gmaps_key)

# 영등포 경찰서 예시로 위도 경도 잘 나오는지 확인
gmaps.geocode('서울영등포경찰서', language = 'ko')
len(tmp)
print(tmp[0].get('geometry')['location']['lat'])
print(tmp[0].get('geometry')['location']['lng'])

# 영등포구 만 슬라이싱
tmp[0].get('formatted_address').split()[2]

crime_station.head()

# 구별, lnt, lng 컬럼 추가
crime_station['구별'] = np.nan
crime_station['lat'] = np.nan
crime_station['lng'] = np.nan

crime_station.head()

# 경찰서 이름에서 소속된 구 이름 얻기
# 구 이름과 위도 경도 정보를 저장할 준비
# 반복문을 이용해서 위 표의 NaN을 모두 채워준다
# iterros() 활용

count = 0

for idx, rows in crime_station.iterrows():
    station_name = '서울' + str(idx) + '경찰서'
    tmp = gmaps.geocode(station_name, language = 'ko')

    tmp_gu = tmp[0].get('formatted_address')
    lat = tmp[0].get('geometry')['location']['lat']
    lng = tmp[0].get('geometry')['location']['lng']

    crime_station.loc[idx, 'lat'] = lat
    crime_station.loc[idx, 'lng'] = lng
    crime_station.loc[idx, '구별'] = tmp_gu.split()[2]

    print(count)
    count += 1

crime_station.head()
crime_station.columns.get_level_values(0)[2] + crime_station.columns.get_level_values(1)[2]
len(crime_station.columns.get_level_values(0))

tmp = [
    crime_station.columns.get_level_values(0)[n] + crime_station.columns.get_level_values(1)[n]
    for n in range(len(crime_station.columns.get_level_values(0)))    
]
tmp, len(tmp), len(crime_station.columns.get_level_values(0))

crime_station.columns = tmp
crime_station.head()

# 로우 데이터로 저장
crime_station.to_csv('../data/02. crime_in_Seoul_raw.csv', sep = ',', encoding='utf-8')
crime_anal_station = pd.read_csv('../data/02. crime_in_Seoul_raw.csv', sep = ',', encoding='utf-8')
crime_anal_station.head()

# 구별 데이터로 정리
crime_anal_station = pd.read_csv('../data/02. crime_in_Seoul_raw.csv', index_col = 0, encoding='utf-8') # index_col '구분'을 인덱스 컬럼으로 설정
crime_anal_station.head()

crime_anal_gu = pd.pivot_table(crime_anal_station, index = '구별', aggfunc=np.sum)
crime_anal_gu.drop(['lat', 'lng'], axis = 1, inplace = True)
crime_anal_gu.head()

# 강강,추행검거 / 강간, 추행 발생 / 강간검거 / 강건 발행 병합
rape = crime_anal_gu['강간,추행검거'] + crime_anal_gu['강간검거']
crime_anal_gu['강간검거1'] = rape
del crime_anal_gu['강간검거']
rape_ha = crime_anal_gu['강간,추행발생'] + crime_anal_gu['강간발생']
crime_anal_gu['강간발생1'] = rape_ha
del crime_anal_gu['강간발생']
crime_anal_gu.head()

crime_anal_gu = crime_anal_gu.drop(['강간,추행검거', '강간,추행발생'], axis=1)
crime_anal_gu

crime_anal_gu.rename(columns={
    crime_anal_gu.columns[8] : '강간검거',
    crime_anal_gu.columns[9] : '강간발생'},
    inplace = True
    )
crime_anal_gu

# 검거율 생성
# 하나의 컬럼을 다른 컬럼으로 나누기
crime_anal_gu['강도검거'] / crime_anal_gu['강도발생']

# 다수의 컬럼을 다수의 컬럼으로 각각 나누기
num = ['강간검거', '강도검거', '살인검거', '절도검거', '폭력검거']
den = ['강간발생', '강도발생', '살인발생', '절도발생', '폭력발생']

crime_anal_gu[num].div(crime_anal_gu[den].values).head()

target = ['강간검거율', '강도검거율', '살인검거율', '절도검거율', '폭력검거율']

crime_anal_gu[target] = crime_anal_gu[num].div(crime_anal_gu[den].values) * 100
crime_anal_gu.head()

# 필요 없는 컬럼 제거
crime_anal_gu.drop(['강간검거', '강도검거', '살인검거', '절도검거', '폭력검거'], axis= 1, inplace=True)

# 100보다 큰 숫자 찾아 바꾸기
crime_anal_gu[crime_anal_gu[target] > 100] = 100
crime_anal_gu.head()

# 컬럼 이름 변경
crime_anal_gu.rename(columns={
    '강도발생' : '강도',
    '살인발생' : '살인',
    '절도발생' : '절도',
    '폭력발생' : '폭력',
    '강간발생' : '강간'
}, inplace=True)
crime_anal_gu.head()

# 결측치 있는지 확인
crime_anal_gu.info()

# 강도 검거율에 NaN값 확인되어 0으로 바꾸기 / 발생 건수가 없기때문에 0으로 처리
crime_anal_gu['강도검거율'].fillna(0, inplace= True)
crime_anal_gu.info()

# 범죄 데이터 정렬을 위한 데이터 정리
# 정규화 : 최고값은 1, 최소값은 0
crime_anal_gu.head()

col = ['강도', '살인', '절도', '폭력', '강간']
crime_anal_norm = crime_anal_gu[col] / crime_anal_gu[col].max()
crime_anal_norm.head()

# 검거율 추가
col2 = ['강도검거율', '살인검거율', '절도검거율', '폭력검거율', '강간검거율']
crime_anal_norm[col2] = crime_anal_gu[col2]
crime_anal_norm.head()

# 구별 CCTV 자료에서 인구수와 CCTV수 추가
result_CCTV = pd.read_csv('../data/01. CCTV_result.csv', index_col = '구별', encoding='utf8')
result_CCTV.head()

crime_anal_norm[['인구수', 'CCTV']] = result_CCTV[['인구수', '총 계']]
crime_anal_norm.head()

# 정규화된 범죄 발생 건수 전체의 평균을 구해서 범죄 컬럼 대표값으로 사용
col = ['강도', '살인', '절도', '폭력', '강간']
crime_anal_norm['범죄'] = np.mean(crime_anal_norm[col], axis = 1)
crime_anal_norm.head()

# 검거율의 평균을 구해서 검거 컬럼의 대표값으로 사용
col = ['강도검거율', '살인검거율', '절도검거율', '폭력검거율', '강간검거율']
crime_anal_norm['검거'] = np.mean(crime_anal_norm[col], axis = 1)
crime_anal_norm

# Google API 문제로 노원경찰서가 노원구로 안바껴 있는걸 확인
# 노원경찰서를 노원구로 변경
crime_anal_norm.rename(index={'노원경찰서': '노원구'}, inplace=True)
crime_anal_norm

# 서울시 범죄현황 데이터 시각화
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rc
plt.rcParams['axes.unicode_minus'] = False
%matplotlib inline
rc('font', family = 'Arial Unicode MS')

# pairplot를 이용 강도, 살인, 폭력에 대한 상관관계 확인
sns.pairplot(data = crime_anal_norm, vars = ['강도', '살인', '폭력'], kind = 'reg', height = 3)
plt.show()

# 인구수, CCTV 와 살인, 강도의 상관관계 확인
def drawGraph():
    sns.pairplot(data = crime_anal_norm, x_vars=['인구수', 'CCTV'], y_vars= ['살인', '강도'], kind = 'reg', height = 4)
    plt.show()

drawGraph()

# 인구수, CCTV와 살인검거율, 폭력검거율의 상관관계 확인
def drawGraph():
    sns.pairplot(data = crime_anal_norm, x_vars=['인구수', 'CCTV'], y_vars= ['살인검거율', '폭력검거율'], kind = 'reg', height = 4)
    plt.show()

drawGraph()

# 인구수, CCTV와 절도검거율, 강도검거율의 상관관계 확인
def drawGraph():
    sns.pairplot(data = crime_anal_norm, x_vars=['인구수', 'CCTV'], y_vars= ['절도검거율', '강도검거율'], kind = 'reg', height = 4)
    plt.show()

drawGraph()
crime_anal_norm.head()

# 검거율 heatmap
# 검거율 컬럼들을 '검거' 컬럼을 기준으로 정렬
def drawGraph():
    #데이터 프레임 생성
    target_col = ['강도검거율', '살인검거율', '절도검거율', '폭력검거율', '강간검거율', '검거']
    crime_anal_norm_sort = crime_anal_norm.sort_values(by = '검거', ascending = False)

    #그래프 생성
    plt.figure(figsize=(10, 10))
    sns.heatmap(data = crime_anal_norm_sort[target_col],
               annot = True,
               fmt = 'f',
               linewidths= 0.5, # 간격 설정
               cmap = 'RdPu'
               )
    plt.title('범죄 검거 비율(정규화된 검거의 합으로 정렬)')
    plt.show()

drawGraph()

# 범죄발생 건수를 heatmap으로 표현
# 범죄 컬럼을 기준으로 정렬
def drawGraph():
    #데이터 프레임 생성
    target_col = ['강도', '살인', '절도', '폭력', '강간', '범죄']
    crime_anal_norm_sort = crime_anal_norm.sort_values(by = '범죄', ascending = False)

    #그래프 생성
    plt.figure(figsize=(10, 10))
    sns.heatmap(data = crime_anal_norm_sort[target_col],
               annot = True,
               fmt = 'f',
               linewidths= 0.5, # 간격 설정
               cmap = 'RdPu'
               )
    plt.title('범죄 발생 비율(정규화된 범죄의 합으로 정렬)')
    plt.show()

drawGraph()

# 데이터 저장
crime_anal_norm.to_csv('../data/02. crime_in_Seoul_final.csv', sep = ',', encoding='utf8')

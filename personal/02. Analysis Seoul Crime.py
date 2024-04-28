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

# 강도 검거율에 NaN값 확인되어 0으로 바꾸기
crime_anal_gu['강도검거율'].fillna(0, inplace= True)
crime_anal_gu.info()














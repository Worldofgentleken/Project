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

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

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("무임승차 비율 상위 20개 지하철역")

# 엑셀 파일 로드
@st.cache_data
def load_data():
    file_path = "tnwjdqh.xls"
    df = pd.read_excel(file_path, skiprows=2)  # 앞의 2줄은 헤더가 아님
    df.columns = df.columns.str.strip()  # 컬럼 이름 공백 제거
    return df

df = load_data()

# 역명, 유임승차, 무임승차 컬럼 자동 탐색
역_컬럼 = [col for col in df.columns if '역' in col or '지하철역' in col][0]
유임_컬럼 = [col for col in df.columns if '유임' in col and '승차' in col][0]
무임_컬럼 = [col for col in df.columns if '무임' in col and '승차' in col][0]

# 필요한 컬럼만 선택
df_filtered = df[[역_컬럼, 유임_컬럼, 무임_컬럼]].copy()
df_filtered.columns = ['역명', '유임승차인원', '무임승차인원']

# 결측치 제거 및 타입 정리
df_filtered = df_filtered.dropna()
df_filtered[['유임승차인원', '무임승차인원']] = df_filtered[['유임승차인원', '무임승차인원']].astype(int)

# 무임승차 비율 계산
df_filtered['무임비율(%)'] = df_filtered['무임승차인원'] / (df_filtered['유임승차인원'] + df_filtered['무임승차인원']) * 100

# 무임비율 상위 20개 역 추출
top20 = df_filtered.sort_values(by='무임비율(%)', ascending=False).head(20)

# 시각화
st.subheader("무임승차 비율 상위 20개 역")
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(top20['역명'], top20['무임비율(%)'], color='skyblue')
ax.set_xlabel("역명")
ax.set_ylabel("무임승차 비율 (%)")
ax.set_title("무임승차 / (유임 + 무임) 비율 상위 20개 역")
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)

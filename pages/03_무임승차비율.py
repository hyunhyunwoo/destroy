import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("무임승차 비율 상위 20개 지하철역")

@st.cache_data
def load_data():
    file_path = "tnwjdqh.xls"

    # 컬럼 수동 지정 (원래 데이터 구조 기준)
    col_names = ['날짜', '호선', '역ID', '역명', '유임승차', '유임하차', '무임승차', '무임하차', '등록일자']
    df = pd.read_excel(file_path, header=None, names=col_names, skiprows=2)
    df = df[['역명', '유임승차', '무임승차']]
    return df

df = load_data()

# 전처리
df = df.dropna()
df['유임승차'] = df['유임승차'].astype(str).str.replace(',', '').astype(int)
df['무임승차'] = df['무임승차'].astype(str).str.replace(',', '').astype(int)

# 무임 비율 계산
df['무임비율(%)'] = df['무임승차'] / (df['유임승차'] + df['무임승차']) * 100

# 상위 20개 역
top20 = df.sort_values(by='무임비율(%)', ascending=False).head(20)

# 시각화
st.subheader("무임승차 비율 상위 20개 역")
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(top20['역명'], top20['무임비율(%)'], color='tomato')
ax.set_xlabel("역명")
ax.set_ylabel("무임승차 비율 (%)")
ax.set_title("무임 / (유임 + 무임) 비율 상위 20개 역")
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)

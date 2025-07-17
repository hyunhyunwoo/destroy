import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="무임승차 비율 분석", layout="wide")
st.title("2025년 6월 지하철 무임승차 비율 상위 20개 역")

# 엑셀 데이터 로드
@st.cache_data
def load_data():
    file_path = "tnwjdqh.xls"
    df = pd.read_excel(file_path, skiprows=2, header=None)  # 헤더 자동 인식 X
    return df

df = load_data()

# 컬럼 수동 지정
df_filtered = df[[3, 4, 6]].copy()
df_filtered.columns = ['역명', '유임승차인원', '무임승차인원']

# 숫자형 변환
df_filtered['유임승차인원'] = df_filtered['유임승차인원'].astype(str).str.replace(',', '').astype(int)
df_filtered['무임승차인원'] = df_filtered['무임승차인원'].astype(str).str.replace(',', '').astype(int)

# 무임 비율 계산
df_filtered['무임비율(%)'] = df_filtered['무임승차인원'] / (df_filtered['유임승차인원'] + df_filtered['무임승차인원']) * 100

# 상위 20개
top20 = df_filtered.sort_values(by='무임비율(%)', ascending=False).head(20)

# 시각화
st.subheader("무임승차 비율 상위 20개 역")
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(top20['역명'], top20['무임비율(%)'], color='tomato')

ax.set_xlabel("역명")
ax.set_ylabel("무임승차 비율 (%)")
ax.set_title("무임 / (유임 + 무임) 비율 상위 20개 역")
ax.set_xticks(range(len(top20['역명'])))
ax.set_xticklabels(top20['역명'], rotation=45, ha='right', fontsize=10)

plt.tight_layout()
st.pyplot(fig)

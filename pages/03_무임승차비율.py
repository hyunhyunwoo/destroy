import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="무임승차 비율 분석", layout="wide")

st.title("2025년 6월 지하철 무임승차 비율 상위 20개 역")

# 데이터 불러오기
@st.cache_data
def load_data():
    file_path = "tnwjdqh.xls"
    df = pd.read_excel(file_path, skiprows=2)  # 앞 2줄은 헤더 아님
    return df

df = load_data()

# 컬럼명 확인 및 자동 추출
st.subheader("원본 데이터 미리보기")
st.dataframe(df.head())

# 컬럼 자동 추출 (유임, 무임, 역명)
try:
    역_컬럼 = [col for col in df.columns if '역' in str(col) or '지하철' in str(col)][0]
    유임_컬럼 = [col for col in df.columns if '유임' in str(col) and '승차' in str(col)][0]
    무임_컬럼 = [col for col in df.columns if '무임' in str(col) and '승차' in str(col)][0]
except IndexError:
    st.error("❌ 필요한 컬럼(역명, 유임승차, 무임승차)을 찾을 수 없습니다.\n컬럼명을 확인해주세요.")
    st.stop()

# 필요한 데이터만 추출
df_filtered = df[[역_컬럼, 유임_컬럼, 무임_컬럼]].copy()
df_filtered.columns = ['역명', '유임승차인원', '무임승차인원']

# 결측치 제거 및 숫자형 변환
df_filtered.dropna(inplace=True)
df_filtered['유임승차인원'] = df_filtered['유임승차인원'].astype(str).str.replace(',', '').astype(int)
df_filtered['무임승차인원'] = df_filtered['무임승차인원'].astype(str).str.replace(',', '').astype(int)

# 무임 비율 계산
df_filtered['무임비율(%)'] = df_filtered['무임승차인원'] / (df_filtered['유임승차인원'] + df_filtered['무임승차인원']) * 100

# 상위 20개 역 추출
top20 = df_filtered.sort_values(by='무임비율(%)', ascending=False).head(20)

# 시각화
st.subheader("무임승차 비율 상위 20개 역")
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(top20['역명'], top20['무임비율(%)'], color='tomato')

# x축 라벨 및 스타일 조정
ax.set_xlabel("역명", fontsize=12)
ax.set_ylabel("무임승차 비율 (%)", fontsize=12)
ax.set_title("무임 / (유임 + 무임) 비율 상위 20개 역", fontsize=14)
ax.set_xticks(range(len(top20['역명'])))
ax.set_xticklabels(top20['역명'], rotation=45, ha='right', fontsize=10)

plt.tight_layout()
st.pyplot(fig)

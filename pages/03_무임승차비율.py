import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 페이지 타이틀
st.title("2025년 6월 지하철 무임승차 비율 상위 20개 역")

# 데이터 불러오기
@st.cache_data
def load_data():
    file_path = "2025년 06월  교통카드 통계자료.xls"
    df = pd.read_excel(file_path, skiprows=2)  # 첫 두 줄 건너뜀
    return df

df = load_data()

# 컬럼명 확인
st.subheader("원본 데이터 미리보기")
st.dataframe(df.head())

# 자동으로 열 이름 추출
역_컬럼 = [col for col in df.columns if '역' in col][0]
유임_컬럼 = [col for col in df.columns if '유임' in col and '승차' in col][0]
무임_컬럼 = [col for col in df.columns if '무임' in col and '승차' in col][0]

# 추출된 컬럼명 확인
st.write("자동 추출된 컬럼명:")
st.write(f"역명: {역_컬럼}, 유임승차: {유임_컬럼}, 무임승차: {무임_컬럼}")

# 필요한 데이터만 추출
df_filtered = df[[역_컬럼, 유임_컬럼, 무임_컬럼]].copy()
df_filtered.columns = ['역명', '유임승차인원', '무임승차인원']  # 표준화

# 결측치 제거 및 숫자형 변환
df_filtered = df_filtered.dropna()
df_filtered[['유임승차인원', '무임승차인원']] = df_filtered[['유임승차인원', '무임승차인원']].astype(int)

# 무임승차 비율 계산: 무임 / (유임 + 무임)
df_filtered['무임비율(%)'] = df_filtered['무임승차인원'] / (df_filtered['유임승차인원'] + df_filtered['무임승차인원']) * 100

# 무임비율 상위 20개 역 추출
top20 = df_filtered.sort_values(by='무임비율(%)', ascending=False).head(20)

# 시각화
st.subheader("무임승차 비율 상위 20개 역 (무임 / 전체)")
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(top20['역명'], top20['무임비율(%)'], color='tomato')
ax.set_xlabel("역명")
ax.set_ylabel("무임승차 비율 (%)")
ax.set_title("무임승차 / (유임 + 무임) 비율 상위 20개 역")
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)


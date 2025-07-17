import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("2025년 6월 지하철 무임승차 비율 상위 20개 역")

@st.cache_data
def load_data():
    file_path = "2025년 06월  교통카드 통계자료.xls"
    df = pd.read_excel(file_path, skiprows=2)
    return df

df = load_data()

# 컬럼 확인
st.subheader("컬럼명 확인")
st.write(df.columns.tolist())

# 자동 컬럼 감지 함수
def find_column(columns, include_keywords):
    for col in columns:
        if all(keyword in col for keyword in include_keywords):
            return col
    return None

# 실제 컬럼 이름 찾기
역_컬럼 = find_column(df.columns, ['역'])
유임_컬럼 = find_column(df.columns, ['유임', '승차'])
무임_컬럼 = find_column(df.columns, ['무임', '승차'])

# 컬럼명 유효성 확인
if not 역_컬럼 or not 유임_컬럼 or not 무임_컬럼:
    st.error("필요한 컬럼(역명, 유임승차, 무임승차)을 찾을 수 없습니다.")
    st.stop()

# 필요한 컬럼만 선택 후 이름 통일
df_filtered = df[[역_컬럼, 유임_컬럼, 무임_컬럼]].copy()
df_filtered.columns = ['역명', '유임승차인원', '무임승차인원']

# 결측치 제거 및 변환
df_filtered = df_filtered.dropna()
df_filtered[['유임승차인원', '무임승차인원']] = df_filtered[['유임승차인원', '무임승차인원']].astype(int)

# 비율 계산
df_filtered['무임비율(%)'] = (
    df_filtered['무임승차인원'] /
    (df_filtered['유임승차인원'] + df_filtered['무임승차인원']) * 100
)

# 상위 20개 역 추출
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

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Matplotlib 한글 폰트 설정
# 시스템에 나눔고딕이 설치되어 있지 않을 경우 다른 폰트 사용 또는 설치 필요
# 보통 Streamlit Cloud에서는 설치되어 있지 않을 수 있어요!
# colab에서는 !apt-get update -qq && !apt-get install -qq fonts-nanum* 명령어로 설치 가능
# 하지만 로컬에서 실행 시에는 다음 코드로 폰트 경로를 찾거나 설치해야 해요.
try:
    font_path = fm.findSystemFonts(fontpaths=None, fontext='ttf')
    nanum_font_path = next((path for path in font_path if "Nanum" in path), None)
    if nanum_font_path:
        fm.fontManager.addfont(nanum_font_path)
        plt.rcParams['font.family'] = 'NanumGothic' # 폰트 이름은 'NanumGothic'일수도, 'NanumGothicOTF'일수도 있어요!
    else:
        st.warning("나눔고딕 폰트를 찾을 수 없습니다. 그래프에 한글이 깨져 보일 수 있습니다.")
        plt.rcParams['font.family'] = 'Malgun Gothic' # Windows 기본 폰트
except Exception as e:
    st.error(f"폰트 설정 중 오류가 발생했습니다: {e}")
    plt.rcParams['font.family'] = 'Malgun Gothic' # 오류 발생 시 대체 폰트 설정
plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지

st.title("2025년 6월 지하철 무임승차 비율 상위 20개 역")

@st.cache_data
def load_data():
    file_path = "2025년 06월  교통카드 통계자료.xls"
    try:
        df = pd.read_excel(file_path, skiprows=2)
        df.columns = df.columns.str.strip() # 👈 컬럼명 앞뒤 공백 제거!
        return df
    except FileNotFoundError:
        st.error(f"'{file_path}' 파일을 찾을 수 없습니다. 파일 경로를 확인해 주세요!")
        return pd.DataFrame() # 빈 데이터프레임 반환
    except Exception as e:
        st.error(f"데이터 로드 중 오류가 발생했습니다: {e}")
        return pd.DataFrame()

df = load_data()

# 데이터프레임이 비어있으면 다음 단계 진행 안 함
if df.empty:
    st.stop()

st.subheader("원본 데이터 미리보기")
st.dataframe(df.head())

# 👇👇👇 여기 부분이 가장 중요해요! 👇👇👇
st.subheader("⚠️ 중요: 실제 데이터 컬럼명 확인!")
st.info("아래에 출력되는 리스트에서 '지하철역', '유임승차수', '무임승차수'에 해당하는 정확한 컬럼 이름을 찾으세요!")
st.write(df.columns.tolist()) # 불러온 데이터의 모든 컬럼 이름들을 리스트로 보여줍니다!

# 사용자가 위 리스트를 보고 정확한 컬럼 이름을 확인한 후,
# 아래 '역_컬럼', '유임_컬럼', '무임_컬럼' 변수의 값을 실제 이름으로 바꿔주세요!
# 예시: 엑셀에 '지하철 역명'이라고 되어있다면 역_컬럼 = '지하철 역명' 이렇게요!
역_컬럼 = '지하철역' # 이 부분을 실제 엑셀 컬럼 이름과 정확히 맞춰주세요!
유임_컬럼 = '유임승차수' # 이 부분도요!
무임_컬럼 = '무임승차수' # 이 부분도 마찬가지예요!

# 혹시 컬럼명이 다를 때를 대비해서 예외 처리를 추가했어요!
required_columns = [역_컬럼, 유임_컬럼, 무임_컬럼]
if not all(col in df.columns for col in required_columns):
    st.error(f"필수 컬럼이 데이터에 없습니다. 확인된 컬럼: {df.columns.tolist()}")
    st.error(f"필요한 컬럼: {required_columns}. 위 '⚠️ 중요: 실제 데이터 컬럼명 확인!' 섹션에서 올바른 이름을 확인 후 코드를 수정해주세요.")
    st.stop()

df_filtered = df[required_columns].copy()
df_filtered.columns = ['역명', '유임승차인원', '무임승차인원']

# 데이터 정리
# 오류 방지를 위해, 숫자로 변환하기 전에 숫자만 있는 값으로 필터링하는 간단한 로직 추가
df_filtered = df_filtered.dropna()
# 유임승차인원과 무임승차인원 컬럼에서 숫자 형태가 아닌 값을 제거하거나 처리하는 로직 필요할 수 있음
# 예시: pd.to_numeric을 사용하고 errors='coerce'로 처리 후, NaN 값 제거
df_filtered['유임승차인원'] = pd.to_numeric(df_filtered['유임승차인원'], errors='coerce').fillna(0).astype(int)
df_filtered['무임승차인원'] = pd.to_numeric(df_filtered['무임승차인원'], errors='coerce').fillna(0).astype(int)

# 무임 비율 계산
total_riders = df_filtered['유임승차인원'] + df_filtered['무임승차인원']
# 분모가 0이 되는 경우를 방지
df_filtered['무임비율(%)'] = df_filtered.apply(
    lambda row: (row['무임승차인원'] / total_riders[row.name]) * 100 if total_riders[row.name] > 0 else 0,
    axis=1
)

# 상위 20개
top20 = df_filtered.sort_values(by='무임비율(%)', ascending=False).head(20)

# 시각화
st.subheader("무임승차 비율 상위 20개 역 (무임 / 전체)")

if not top20.empty:
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(top20['역명'], top20['무임비율(%)'], color='tomato')
    ax.set_xlabel("역명")
    ax.set_ylabel("무임승차 비율 (%)")
    ax.set_title("무임승차 / (유임 + 무임) 비율 상위 20개 역")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout() # 그래프 요소들이 잘리지 않게 조정
    st.pyplot(fig)
else:
    st.warning("분석할 데이터가 없거나, 상위 20개 역을 찾을 수 없습니다.")

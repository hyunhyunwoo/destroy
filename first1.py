import streamlit as st
import streamlit as st
import pandas as pd

# 제목
st.title("2025년 5월 기준 연령별 인구 현황 분석")

# 데이터 불러오기
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요 (EUC-KR 인코딩)", type="csv")
if uploaded_file is not None:
    # CSV 파일 읽기
    df = pd.read_csv(uploaded_file, encoding='euc-kr')

    # 원본 데이터 표시
    st.subheader("📄 원본 데이터")
    st.dataframe(df)

    # 연령별 컬럼 추출 및 정리
    age_columns = [col for col in df.columns if col.startswith("2025년05월_계_")]
    new_age_columns = [col.replace("2025년05월_계_", "") for col in age_columns]
    df_age = df[["행정기관명", "총인구수"] + age_columns].copy()
    df_age.columns = ["행정기관명", "총인구수"] + new_age_columns

    # 총인구수 기준 상위 5개 행정구역
    top5_df = df_age.sort_values("총인구수", ascending=False).head(5)

    # 연령 데이터 정수형 변환
    age_only = [int(age) for age in new_age_columns]
    
    # 연령별 인구 선 그래프
    st.subheader("📈 상위 5개 행정구역 연령별 인구 선 그래프")
    for _, row in top5_df.iterrows():
        region = row["행정기관명"]
        age_pop = row[new_age_columns]
        age_pop.index = age_only
        age_pop = age_pop.sort_index()

        st.markdown(f"**{region}**")
        st.line_chart(age_pop)

    # 상위 5개 행정구역 요약표
    st.subheader("🏙️ 상위 5개 행정구역 인구 요약")
    st.dataframe(top5_df[["행정기관명", "총인구수"]])

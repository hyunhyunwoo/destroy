import streamlit as st
import pandas as pd

st.title("2025년 5월 기준 연령별 인구 현황 분석")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요 (EUC-KR 인코딩)", type="csv")
if uploaded_file is not None:
    # 파일 읽기
    df = pd.read_csv(uploaded_file, encoding='euc-kr')
    
    # 열 이름 출력
    st.subheader("🔎 데이터프레임 열 목록")
    st.write(df.columns.tolist())

    # '총인구수'와 '행정기관명' 추정
    region_col = [col for col in df.columns if '행정' in col][0]
    total_col = [col for col in df.columns if '총인구수' in col][0]
    age_columns = [col for col in df.columns if col.startswith("2025년05월_계_")]
    new_age_columns = [col.replace("2025년05월_계_", "") for col in age_columns]

    # 데이터 전처리
    df_age = df[[region_col, total_col] + age_columns].copy()
    df_age.columns = ["행정기관명", "총인구수"] + new_age_columns

    # 원본 데이터 출력
    st.subheader("📄 원본 데이터")
    st.dataframe(df)

    # 상위 5개 행정구역
    top5_df = df_age.sort_values("총인구수", ascending=False).head(5)

    # 연령별 선 그래프
    st.subheader("📈 상위 5개 행정구역 연령별 인구 선 그래프")
    age_only = [int(a) for a in new_age_columns]
    for _, row in top5_df.iterrows():
        region = row["행정기관명"]
        age_pop = row[new_age_columns]
        age_pop.index = age_only
        age_pop = age_pop.sort_index()

        st.markdown(f"**{region}**")
        st.line_chart(age_pop)

    # 요약표 출력
    st.subheader("🏙️ 상위 5개 행정구역 인구 요약")
    st.dataframe(top5_df[["행정기관명", "총인구수"]])

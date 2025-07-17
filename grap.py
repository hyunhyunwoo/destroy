import streamlit as st
import pandas as pd
import os

# 제목
st.title("2025년 5월 기준 연령별 인구 현황 분석")

# CSV 파일 경로 (같은 디렉터리에 있는 경우)
DATA_PATH = "202505_202505_연령별인구현황_월간.csv"

# 파일 존재 여부 확인
if not os.path.exists(DATA_PATH):
    st.error("❌ 데이터 파일이 존재하지 않습니다. 같은 폴더에 '202505_202505_연령별인구현황_월간.csv' 파일을 넣어주세요.")
else:
    # CSV 읽기 (EUC-KR 인코딩)
    df = pd.read_csv(DATA_PATH, encoding="euc-kr")

    # 원본 데이터 표시
    st.subheader("📄 원본 데이터")
    st.dataframe(df)

    # '2025년05월_계_'로 시작하는 열만 추출
    age_columns = [col for col in df.columns if col.startswith("2025년05월_계_")]
    new_age_columns = [col.replace("2025년05월_계_", "") for col in age_columns]

    # 필요한 컬럼만 정리
    df_age = df[["행정기관명", "총인구수"] + age_columns].copy()
    df_age.columns = ["행정기관명", "총인구수"] + new_age_columns

    # 총인구수 기준 상위 5개 행정구역
    top5_df = df_age.sort_values("총인구수", ascending=False).head(5)

    # 연령을 정수로 변환해 정렬
    age_only = [int(a) for a in new_age_columns]

    st.subheader("📊 상위 5개 행정구역 연령별 인구 현황")

    for _, row in top5_df.iterrows():
        region = row["행정기관명"]
        pop_by_age = row[new_age_columns]
        pop_by_age.index = age_only
        pop_by_age = pop_by_age.sort_index()

        st.markdown(f"### 📍 {region}")
        st.line_chart(pop_by_age)

    # 상위 5개 행정구역 요약 정보
    st.subheader("🏙️ 상위 5개 행정구역 인구 요약")
    st.dataframe(top5_df[["행정기관명", "총인구수"]])

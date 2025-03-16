import streamlit as st
import pandas as pd

# 공개된 구글 스프레드시트의 CSV 다운로드 URL 변환
# URL 형식: https://docs.google.com/spreadsheets/d/<스프레드시트ID>/export?format=csv&id=<스프레드시트ID>&gid=<시트ID>
SHEET_ID = "1HA1PtKWg-bFud5R3d_wMVX7wOpfcHkekKD-9T7wpxfE"
GID = "1353891871"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&id={SHEET_ID}&gid={GID}"

@st.cache_data(ttl=600)
def load_data(url):
    return pd.read_csv(url)

# 데이터 불러오기
data = load_data(CSV_URL)

# 세션 상태에 현재 인덱스 저장 (초기값 0)
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

# 현재 지원자 정보 선택 (인덱스 범위 체크)
current_index = st.session_state.current_index
if current_index < 0:
    current_index = 0
elif current_index >= len(data):
    current_index = len(data) - 1

applicant = data.iloc[current_index]

# 상단: 학교명과 이름 표시
school_name = applicant["학교명"]
name = applicant["이름"]
st.header(f"{school_name} - {name}")

# 중간: 2 컬럼 레이아웃 (왼쪽: YouTube 영상, 오른쪽: PDF 미리보기)
col1, col2 = st.columns(2)

with col1:
    youtube_url = applicant["youtube영상주소"]
    # YouTube URL이 정상적인지 간단히 확인 후 영상 임베드
    if pd.notnull(youtube_url):
        st.video(youtube_url)
    else:
        st.write("YouTube 영상이 없습니다.")

with col2:
    pdf_url = applicant["문서제출"]
    # PDF 문서 미리보기 - iframe 사용 (문서 URL이 공개되어 있어야 함)
    if pd.notnull(pdf_url):
        st.markdown(
            f'<iframe src="{pdf_url}" width="100%" height="500px"></iframe>',
            unsafe_allow_html=True
        )
    else:
        st.write("제출된 문서가 없습니다.")

# 하단: 이전/다음 버튼 (지원자 탐색)
prev_col, next_col = st.columns(2)

with prev_col:
    if st.button("⬅️ 이전", disabled=(current_index == 0)):
        st.session_state.current_index = current_index - 1

with next_col:
    if st.button("다음 ➡️", disabled=(current_index == len(data) - 1)):
        st.session_state.current_index = current_index + 1

# 페이지 하단에 현재 인덱스 정보 표시 (옵션)
st.write(f"지원자 {current_index + 1} / {len(data)}")

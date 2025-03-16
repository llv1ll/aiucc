import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

SHEET_ID = "1HA1PtKWg-bFud5R3d_wMVX7wOpfcHkekKD-9T7wpxfE"
GID = "1353891871"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&id={SHEET_ID}&gid={GID}"

@st.cache_data(ttl=600)
def load_data(url):
    return pd.read_csv(url)

data = load_data(CSV_URL)
applicant_names = (data["학교"] + " - " + data["이름"]).tolist()

if not applicant_names:
    st.write("지원자가 없습니다.")
else:
    # 메인 영역 내 2컬럼 레이아웃: 왼쪽(지원자 리스트), 오른쪽(상세 정보)
    left_col, right_col = st.columns([1, 3])
    
    with left_col:
        # st.sidebar 대신 일반 st.radio 사용
        selected_applicant = st.radio("지원자 리스트", applicant_names)
    
    selected_index = applicant_names.index(selected_applicant)
    applicant = data.iloc[selected_index]
    
    with right_col:
        st.header(f"지원자 정보 : {applicant['학교']} - {applicant['이름']}")
    
        col1, col2 = st.columns(2)
    
        with col1:
            youtube_url = applicant["영상주소"]
            if pd.notnull(youtube_url):
                st.video(youtube_url)
            else:
                st.write("YouTube 영상이 없습니다.")
    
        def extract_file_id(url: str) -> str:
            if "id=" in url:
                file_id = url.split("id=")[1]
                if "&" in file_id:
                    file_id = file_id.split("&")[0]
                return file_id
            return None
    
        with col2:
            pdf_url = applicant["문서 제출"]
            file_id = extract_file_id(pdf_url)
            if pd.notnull(pdf_url):
                if file_id:
                    embeded_file_url = f"https://drive.google.com/file/d/{file_id}/preview"
                    st.markdown(
                        f'<iframe src="{embeded_file_url}" width="100%" height="500px"></iframe>',
                        unsafe_allow_html=True
                    )
                else:
                    st.write("file_id를 추출할 수 없습니다.")
            else:
                st.write("제출된 문서가 없습니다.")

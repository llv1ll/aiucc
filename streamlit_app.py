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
    # 세션 상태 초기화
    if "selected_index" not in st.session_state:
        st.session_state.selected_index = 0

    # 이전/다음 버튼 이벤트 처리
    def prev_applicant():
        if st.session_state.selected_index > 0:
            st.session_state.selected_index -= 1

    def next_applicant():
        if st.session_state.selected_index < len(applicant_names) - 1:
            st.session_state.selected_index += 1

    # 이전/다음 버튼
    prev_col, next_col = st.columns(2)
    with prev_col:
        st.button("⬅️ 이전", on_click=prev_applicant, disabled=(st.session_state.selected_index == 0))
    with next_col:
        st.button("다음 ➡️", on_click=next_applicant, disabled=(st.session_state.selected_index == len(data) - 1))

    # 사이드바 radio 버튼은 세션상태와 동기화 (index를 세션 상태로 고정)
    selected_applicant = st.sidebar.radio(
        "지원자 리스트",
        applicant_names,
        index=st.session_state.selected_index,
        key='applicant_radio'  # 키 설정하여 Streamlit 내부 상태 유지
    )

    # 사용자가 라디오 버튼을 클릭하면 선택 인덱스를 갱신
    st.session_state.selected_index = applicant_names.index(selected_applicant)
    applicant = data.iloc[st.session_state.selected_index]

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

    # 페이지 하단에 현재 인덱스 정보 표시
    st.write(f"지원자 {st.session_state.selected_index + 1} / {len(data)}")

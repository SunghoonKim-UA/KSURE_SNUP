import PyPDF2
import streamlit as st

# Set the title of the web interface
st.title("취준생을 위한 자기소개서 상담사 AI")

# Section 1: 회사 정보
st.header("1. 회사 정보")
cominfo_1 = st.text_area("1.1. 신년사", key="cominfo_1")
cominfo_2 = st.text_input("1.2. 회사 소개 URL", key="cominfo_2")
cominfo_3 = st.text_input("1.3. 회사 인재상 URL", key="cominfo_3")

# Section 2: 자기소개서 질문 목록
st.header("2. 자기소개서 질문 목록")
self_intro_question_lists = st.text_area("자기소개서 질문 목록", key="self_intro_question_lists")

# Section 3: 내 정보
st.header("3. 내 정보")
myinfo_1 = st.text_area("3.1. 학력", key="myinfo_1")
myinfo_2 = st.text_area("3.2. 경력", key="myinfo_2")
myinfo_3 = st.text_input("3.3. 공인영어성적", key="myinfo_3")
myinfo_4 = st.text_input("3.4. 자격증", key="myinfo_4")
myinfo_5 = st.text_area("3.5. 우대사항", key="myinfo_5")
myinfo_6 = st.text_area("3.6. 나를 표현하는 사건", key="myinfo_6")
myinfo_7 = st.text_area("3.7. 이전 회사 퇴사 사유", key="myinfo_7")

# Section 4: 제약사항
st.header("4. 제약사항")
constraints_1 = st.text_input("4.1. 채용공고 문서 URL", key="constraints_1")
constraints_2 = st.text_input("4.2. 문항별 최대 글자수", key="constraints_2")

# Button to generate the output
if st.button("Generate 자기소개서"):
    
    
    # Placeholder for the output
    st.header("자기소개서")
    st.write("Generated 자기소개서 will be displayed here.")

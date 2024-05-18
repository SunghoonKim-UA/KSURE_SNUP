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

# Prompt
from langchain_upstage import ChatUpstage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

llm = ChatUpstage()
prompt_template = PromptTemplate.from_template(
    """
    나는 취업준비생을 위해서 자기소개서를 작성해주는 상담사입니다. 
    다음 회사에 대해서 자기소개서를 작성해주세요
    회사의 신년사는 다음과 같습니다. "{cominfo_1}":
    회사 소개는 다음과 같습니다. "{cominfo_2}":
    회사 인재상은 다음과 같습니다. "{cominfo_3}":
    내 정보는 다음과 같습니다.
    내 학력은 다음과 같습니다. "{myinfo_1}":
    내 경력은 다음과 같습니다. "{myinfo_2}":
    내 공인영어성적은 다음과 같습니다. "{myinfo_3}":
    내 자격증은 다음과 같습니다. "{myinfo_4}":
    내 우대사항은 다음과 같습니다. "{myinfo_5}":
    나를 표현하는 사건은 다음과 같습니다. "{myinfo_6}":
    이전 회사 퇴사 사유는 다음과 같습니다. "{myinfo_7}":
    다음 제약사항을 참고해서 작성해줘
    채용공고는 다음과 같습니다. "{constraints_1}":
    다음 질문에 대해서 자기소개서를 작성해주세요 "{self_intro_question_lists}":
    최대글자수는 "{constraints_2}" 입니다
    "
    ---
    """
)
chain = prompt_template | llm | StrOutputParser()
answer = chain.invoke({"cominfo_1": cominfo_1, "cominfo_2": cominfo_2, "cominfo_3": cominfo_3, "myinfo_1": myinfo_1, "myinfo_2": myinfo_3, "myinfo_3": myinfo_3, "myinfo_4": myinfo_4, "myinfo_5": myinfo_5, "myinfo_6": myinfo_6, "myinfo_7": myinfo_7, "constraints_1": constraints_2, "constraints_2": constraints_2, "self_intro_question_lists": self_intro_question_lists })

# Button to generate the output
if st.button("Generate 자기소개서"):
    
    
    # Placeholder for the output
    st.header("자기소개서")
    st.write(answer)

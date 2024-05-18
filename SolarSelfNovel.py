import streamlit as st
import requests
from bs4 import BeautifulSoup
import sqlite3
from langchain_upstage import ChatUpstage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

import GetCompanyInfo as gci

# Function to fetch and parse text from a URL
def get_text_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup.get_text(separator=' ', strip=True))
        return soup.get_text(separator=' ', strip=True)
    except requests.exceptions.RequestException as e:
        return f"Error fetching the URL: {e}"

# Function to initialize the SQLite database
def init_db():
    conn = sqlite3.connect('inputs_outputs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS data (
                    id INTEGER PRIMARY KEY,
                    cominfo_1 TEXT,
                    cominfo_2 TEXT,
                    cominfo_3 TEXT,
                    self_intro_question_lists TEXT,
                    myinfo_1 TEXT,
                    myinfo_2 TEXT,
                    myinfo_3 TEXT,
                    myinfo_4 TEXT,
                    constraints_1 TEXT,
                    constraints_2 TEXT,
                    answer TEXT
                )''')
    conn.commit()
    conn.close()

# Function to save data to the SQLite database
def save_to_db(data):
    conn = sqlite3.connect('inputs_outputs.db')
    c = conn.cursor()
    c.execute('''INSERT INTO data (cominfo_1, cominfo_2, cominfo_3, self_intro_question_lists, myinfo_1, myinfo_2, myinfo_3, myinfo_4, constraints_1, constraints_2, answer)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                 (data['cominfo_1'], data['cominfo_2'], data['cominfo_3'], data['self_intro_question_lists'], data['myinfo_1'], data['myinfo_2'], data['myinfo_3'], data['myinfo_4'], data['constraints_1'], data['constraints_2'], data['answer']))
    conn.commit()
    conn.close()

# Function to fetch data from the SQLite database
def fetch_from_db():
    conn = sqlite3.connect('inputs_outputs.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM data''')
    rows = c.fetchall()
    conn.close()
    return rows

# Initialize the database
init_db()

# Set the title of the web interface
st.title("취준생을 위한 자기소개서 상담사 AI")

# Section 1: 회사 정보
st.header("1. 회사 정보")
cominfo_0 = st.text_input("1.0. 회사명", key="cominfo_0")
cominfo_1 = st.text_area("1.1. 신년사 (미 입력 시, 회사명 기준으로 웹검색결과 적용)", key="cominfo_1")
cominfo_2 = st.text_input("1.2. 회사 소개 URL (미 입력 시, 회사명 기준으로 웹검색결과 적용)", key="cominfo_2")
cominfo_3 = st.text_input("1.3. 회사 인재상 URL (미 입력 시, 회사명 기준으로 웹검색결과 적용)", key="cominfo_3")

# Section 2: 자기소개서 질문 목록
st.header("2. 자기소개서 질문 목록")
self_intro_question_lists = st.text_area("자기소개서 질문 목록", key="self_intro_question_lists")

# Section 3: 내 정보
st.header("3. 내 정보")
myinfo_1 = st.text_area("3.1. 전공", key="myinfo_1")
myinfo_2 = st.text_area("3.2. 경력", key="myinfo_2")
myinfo_3 = st.text_input("3.3. 자격증", key="myinfo_3")
myinfo_4 = st.text_area("3.4. 나를 표현하는 사건", key="myinfo_4")

# Section 4: 제약사항
st.header("4. 제약사항")
constraints_1 = st.text_input("4.1. 채용공고 문서 URL", key="constraints_1")
constraints_2 = st.text_input("4.2. 문항별 최대 글자수", key="constraints_2")

# Prompt
llm = ChatUpstage()
prompt_template = PromptTemplate.from_template(
    """
    나는 취업준비생을 위해서 자기소개서를 작성해주는 상담사입니다.
    
    다음 회사에 대해서 자기소개서를 작성해주세요.

    회사의 신년사는 다음과 같습니다. "{cominfo_1}":
    회사의 신년사는 중요합니다. 회사의 신년사는 그 해의 방향성과 목표를 제시하는 중요한 역할을 합니다. 
    이를 통해 직원들은 회사의 비전과 가치를 이해하고, 각자의 역할과 책임을 인식할 수 있습니다. 
    그러므로 회사의 신년사를 자기소개 질문과 연관지어 작성해주세요
    
    회사 소개는 다음과 같습니다. "{cominfo_2}":
    회사의 소개 자료와 내 정보를 잘 매칭하여 작성해주세요

    회사 인재상은 다음과 같습니다. "{cominfo_3}":
    자기소개서를 작성할때 회사 인재상에 해당하는 항목이 적어도 1가지는 있도록 작성해주세요

    내 정보는 다음과 같습니다.
    내 전공은 다음과 같습니다. "{myinfo_1}":
    내 전공에 맞게 자기소개서를 맞춤화해야 합니다. 
    일반적인 자기소개서를 사용하지 말고, 내 전공에 맞는 내용과 스타일로 작성해야 합니다.

    내 경력은 다음과 같습니다. "{myinfo_2}":
    내 자격증은 다음과 같습니다. "{myinfo_3}":
    나를 표현하는 사건은 다음과 같습니다. "{myinfo_4}":
    경험과 역량 강조: 자신의 경험과 역량을 강조하여 자기소개서를 작성하세요. 
    어떤 프로젝트나 업무에서 어떤 역할을 맡았는지, 어떤 성과를 이루었는지 등을 구체적으로 기술해야 합니다.
    진정성과 열정 표현: 자기소개서에는 자신의 진정성과 열정을 표현하는 것이 중요합니다. 
    자신의 경험과 역량을 바탕으로 해당 직무나 학교에 대한 열정과 관심을 나타내세요.
    
    다음 제약사항을 참고해서 작성해줘

    채용공고는 다음과 같습니다. "{constraints_1}":
    다음 질문에 대해서 자기소개서를 작성해주세요 "{self_intro_question_lists}":
    최대글자수는 "{constraints_2}" 입니다
    ---
    """
)

def fetch_and_display_url_content(urls):
    content_dict = {}
    for key, url in urls.items():
        if url:
            content_dict[key] = get_text_from_url(url)
        else:
            content_dict[key] = ""
    return content_dict

# Button to generate the output
if st.button("Generate 자기소개서"):
    urls = {
        "cominfo_2": cominfo_2,
        "cominfo_3": cominfo_3,
        "constraints_1": constraints_1
    }

    url_contents = fetch_and_display_url_content(urls)

    year_greeting, comp_intro, comp_membership = gci.get_company_info(cominfo_0)


    chain = prompt_template | llm | StrOutputParser()
    answer = chain.invoke({
        "cominfo_1": year_greeting if cominfo_1 == "" else cominfo_1, 
        "cominfo_2": comp_intro if cominfo_2 == "" else url_contents["cominfo_2"], 
        "cominfo_3": comp_membership if cominfo_3 == "" else url_contents["cominfo_3"], 
        "myinfo_1": myinfo_1, 
        "myinfo_2": myinfo_2, 
        "myinfo_3": myinfo_3, 
        "myinfo_4": myinfo_4, 
        "constraints_1": url_contents["constraints_1"], 
        "constraints_2": constraints_2, 
        "self_intro_question_lists": self_intro_question_lists
    })
    
    # Save inputs and output to database
    data = {
#        "cominfo_1": cominfo_1,
#        "cominfo_2": url_contents["cominfo_2"],
#        "cominfo_3": url_contents["cominfo_3"],
        "cominfo_1": ",".join(str(element) for element in year_greeting) if cominfo_1 == "" else cominfo_1, 
        "cominfo_2": ",".join(str(element) for element in comp_intro) if cominfo_2 == "" else url_contents["cominfo_2"], 
        "cominfo_3": ",".join(str(element) for element in comp_membership) if cominfo_3 == "" else url_contents["cominfo_3"], 
        "self_intro_question_lists": self_intro_question_lists,
        "myinfo_1": myinfo_1,
        "myinfo_2": myinfo_2,
        "myinfo_3": myinfo_3,
        "myinfo_4": myinfo_4,
        "constraints_1": url_contents["constraints_1"],
        "constraints_2": constraints_2,
        "answer": answer
    }
    save_to_db(data)
    
    # Placeholder for the output
    st.header("자기소개서")
    st.write(answer)
    
    # Display the inputs and the generated output
    st.header("입력 정보 및 생성된 자기소개서")
    st.subheader("회사 정보")
    st.write("신년사:", cominfo_1)
    st.write("회사 소개 URL:", cominfo_2)
    st.write("회사 인재상 URL:", cominfo_3)
    st.subheader("자기소개서 질문 목록")
    st.write(self_intro_question_lists)
    st.subheader("내 정보")
    st.write("전공:", myinfo_1)
    st.write("경력:", myinfo_2)
    st.write("자격증:", myinfo_3)
    st.write("나를 표현하는 사건:", myinfo_4)
    st.subheader("제약사항")
    st.write("채용공고 문서 URL:", constraints_1)
    st.write("문항별 최대 글자수:", constraints_2)
    st.header("생성된 자기소개서")
    st.write(answer)

    # Fetch and display data from the database
    st.header("저장된 데이터베이스 내용")
    rows = fetch_from_db()
    for row in rows:
        st.write("ID:", row[0])
        st.write("신년사:", row[1])
        st.write("회사 소개 URL:", row[2])
        st.write("회사 인재상 URL:", row[3])
        st.write("자기소개서 질문 목록:", row[4])
        st.write("전공:", row[5])
        st.write("경력:", row[6])
        st.write("자격증:", row[7])
        st.write("나를 표현하는 사건:", row[8])
        st.write("채용공고 문서 URL:", row[9])
        st.write("문항별 최대 글자수:", row[10])
        st.write("생성된 자기소개서:", row[11])
        st.write("---")

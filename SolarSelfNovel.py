import streamlit as st
import requests
from bs4 import BeautifulSoup
import sqlite3
from langchain_upstage import ChatUpstage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

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

# Initialize the database
init_db()

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
    다음 회사에 대해서 자기소개서를 작성해주세요
    회사의 신년사는 다음과 같습니다. "{cominfo_1}":
    회사 소개는 다음과 같습니다. "{cominfo_2}":
    회사 인재상은 다음과 같습니다. "{cominfo_3}":
    내 정보는 다음과 같습니다.
    내 학력은 다음과 같습니다. "{myinfo_1}":
    내 경력은 다음과 같습니다. "{myinfo_2}":
    내 자격증은 다음과 같습니다. "{myinfo_3}":
    나를 표현하는 사건은 다음과 같습니다. "{myinfo_4}":
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

    chain = prompt_template | llm | StrOutputParser()
    answer = chain.invoke({
        "cominfo_1": cominfo_1, 
        "cominfo_2": url_contents["cominfo_2"], 
        "cominfo_3": url_contents["cominfo_3"], 
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
        "cominfo_1": cominfo_1,
        "cominfo_2": url_contents["cominfo_2"],
        "cominfo_3": url_contents["cominfo_3"],
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

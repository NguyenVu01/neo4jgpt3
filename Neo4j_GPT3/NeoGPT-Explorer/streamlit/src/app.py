import os
import openai
import streamlit as st
from streamlit_chat import message

from driver import read_query, get_article_text
from train_cypher import examples

st.title("Chatbot customer care at X Bank")

# openai.api_key = os.environ.get('OPENAI_KEY')
openai.api_key = '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'

def generate_response(prompt, cypher=True):
    if cypher:
        completions = openai.Completion.create(
            engine="text-davinci-003",
            prompt=examples + "\n#" + prompt,
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.5,
        )
        cypher_query = completions.choices[0].text
        message = read_query(cypher_query)
        return message, cypher_query
    else:
        completions = openai.Completion.create(
            engine="text-davinci-003",
            prompt="Summarize the following article: \n" + prompt,
            max_tokens=256,
            n=1,
            stop=None,
            temperature=0.5,
        )
        message = completions.choices[0].text
        return message, None


# Storing the chat: Lưu trữ đoạn chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []


def get_text():
    input_text = st.text_input(
        "Ask away", "", key="input")
    return input_text


col1, col2 = st.columns([2, 1])


with col2:
    another_placeholder = st.empty()
with col1:
    placeholder = st.empty()
user_input = get_text()


# if user_input:
#     # Summarize articles: Tổng hợp các articles
#     if "summar" in user_input.lower():
#         article_title = user_input.split(":")[1].strip()
#         article_text = get_article_text(article_title)
#         if not article_text:
#             st.session_state.past.append(user_input)
#             st.session_state.generated.append(
#                 (["Couldn't find any text for the given article"], ""))
#         else:
#             output, cypher_query = generate_response(user_input, cypher=False)
#             st.session_state.past.append(user_input)
#             st.session_state.generated.append(([output], cypher_query))
#     # English2Cypher with GPT
#     else:
#         output, cypher_query = generate_response(user_input)
#         # store the output
#         st.session_state.past.append(user_input)
#         st.session_state.generated.append((output, cypher_query))

# # Message placeholder: Khung tin nhắn chat
# with placeholder.container():
#     if st.session_state['generated']:
#         message(st.session_state['past'][-1],
#                 is_user=True, key=str(-1) + '_user')
#         for j, text in enumerate(st.session_state['generated'][-1][0]):
#             message(text, key=str(-1) + str(j))
        
# # Generated Cypher statements: Nơi chứa câu lệnh Cypher được tạo
# with another_placeholder.container():
#     if st.session_state['generated']:
#         st.text_area("Generated Cypher statement - Khởi tạo câu lệnh truy vấn Cypher thông qua đoạn text mà người dùng nhập",
#                      st.session_state['generated'][-1][1], height=200)

# if user_input:
#     # Summarize articles: Tổng hợp các articles
#     if "summar" in user_input.lower():
#         article_title = user_input.split(":")[1].strip()
#         article_text = get_article_text(article_title)
#         if not article_text:
#             st.session_state.past.append(user_input)
#             st.session_state.generated.append(
#                 (["Couldn't find any text for the given article"], ""))
#         else:
#             output, cypher_query = generate_response(user_input, cypher=False)
#             st.session_state.past.append(user_input)
#             st.session_state.generated.append(([output], cypher_query))
#     # English2Cypher with GPT
#     else:
#         output, cypher_query = generate_response(user_input)
#         # store the output
#         st.session_state.past.append(user_input)
#         st.session_state.generated.append((output, cypher_query))
# else:
#     st.session_state.generated.append((["Xin lỗi quý khách, quý khách có thể thử lại!"], ""))

if user_input:
    # Summarize articles: Tổng hợp các bài viết
    if "summar" in user_input.lower():
        article_title = user_input.split(":")[1].strip()
        article_text = get_article_text(article_title)
        if not article_text:
            st.session_state.past.append(user_input)
            st.session_state.generated.append(
                (["Không tìm thấy dữ liệu"], ""))
        else:
            output, cypher_query = generate_response(user_input, cypher=False)
            st.session_state.past.append(user_input)
            st.session_state.generated.append(([output], cypher_query))
    # English2Cypher with GPT
    else:
        output, cypher_query = generate_response(user_input)
        # Lưu kết quả truy vấn
        st.session_state.past.append(user_input)
        if output and output != "null":
            st.session_state.generated.append((output, cypher_query))
        else:
            st.session_state.generated.append((["Để biết thêm chi tiết quý khách vui lòng liên hệ theo số hotline: 1900 585850"], ""))
else:
    st.session_state.generated.append((["Vui lòng nhập câu hỏi"], ""))


# Message placeholder: Khung tin nhắn chat
with placeholder.container():
    if st.session_state['generated']:
        message(st.session_state['past'][-1],
                is_user=True, key=str(-1) + '_user')
        for j, text in enumerate(st.session_state['generated'][-1][0]):
            message(text, key=str(-1) + str(j))
    else:
        message("Để biết thông tin chi tiết, vui lòng liên hệ hotline: 1900 58 58 58, quý khách sẽ được nhân viên chăm sóc tư vấn và giải đáp ngay lập tức!")

# Generated Cypher statements: Nơi chứa câu lệnh Cypher được tạo
with another_placeholder.container():
    if st.session_state['generated']:
        cypher_statement = st.session_state['generated'][-1][1]
        if cypher_statement:
            st.text_area("Generated Cypher statement - Khởi tạo câu lệnh truy vấn Cypher thông qua đoạn text mà người dùng nhập",
                         cypher_statement, height=200)
        else:
            st.text_area("Generated Cypher statement - Khởi tạo câu lệnh truy vấn Cypher thông qua đoạn text mà người dùng nhập",
                         "Chúng tôi không thể tìm thấy kết quả trong CSDL", height=200)
    else:
        print("Đã có lỗi xảy ra? Quý khách vui lòng thử lại!")

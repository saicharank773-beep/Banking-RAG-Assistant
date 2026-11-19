
import streamlit as st
from workflow import banking_workflow

st.set_page_config(
    page_title="Banking AI Assistant",
    page_icon="🏦"
)

st.title("🏦 Banking AI Assistant")
st.caption("Banking HR Policy Assistant")
st.write("Ask questions about company HR policies.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("Ask your HR policy question...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching policy documents..."):
            try:
                result = banking_workflow.invoke({
                    "question": question,
                    "context": "",
                    "answer": ""
                })

                answer = result["answer"]
                st.write(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(f"Error: {e}")

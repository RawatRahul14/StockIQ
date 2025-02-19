import streamlit as st
from StockIQ.utils.model import load_llm
from StockIQ.pipeline.agent import create_stock_agent

st.set_page_config(page_title = "StockIQ🤖 - Intelligent Insights for Trading",
                   layout = "wide")
st.title("StockIQ🤖 - Intelligent Insights for Trading")
st.write("Ask any stock-related question, and our AI will provide insights!")

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "agent" not in st.session_state:
    with st.spinner("Loading the AI model..."):
        st.session_state.agent = create_stock_agent(load_llm())

# Display chat history
chat_container = st.container()
with chat_container:
    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(chat["question"])
        with st.chat_message("assistant"):
            st.write(chat["answer"])

# User input field
user_question = st.text_input("Ask a question about a stock...", key = "user_input")

if user_question:
    with st.spinner("Analyzing..."):
        try:
            response = st.session_state.agent.run({"input": user_question})
            st.session_state.chat_history.append({"question": user_question, "answer": response})
            
            # Display the latest chat interaction
            with chat_container:
                with st.chat_message("user"):
                    st.write(user_question)
                with st.chat_message("assistant"):
                    st.write(response)
            
            # Clear input field after submission
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")
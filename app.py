import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


from dotenv import load_dotenv
import os

load_dotenv()

## Langsmith Tracing
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Q&A Chatbot with Groq"



## Prompt Template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user's question as accurately as possible."),
        ("user", "Question: {question}")
    ]
)

def generate_response(question,api_key,llm,temperature,max_tokens):
    model = ChatGroq(model=llm, api_key=api_key, temperature=temperature, max_tokens=max_tokens)
    output_parser = StrOutputParser()
    chain = prompt | model | output_parser
    response = chain.invoke({"question": question})
    return response


## Streamlit App

## title of tha app
st.title("Q&A Chatbot with Groq")

## sidebar for settings
st.sidebar.header("Settings")
api_key=st.sidebar.text_input("Enter your Groq API Key:", type="password")

## Dropdown to select various GROQ models
llm = [
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "openai/gpt-oss-120b"
]
selected_model = st.sidebar.selectbox("Select GROQ Model:", llm)

## Adjust response creativity
temperature = st.sidebar.slider("Response Creativity (Temperature):", 0.0, 1.0, 0.7)

## Adjust response length
max_tokens = st.sidebar.slider("Max Response Length (Tokens):", 50, 1000, 200)

## User input for question
question = st.text_input("Enter your question here:")

if question and api_key:
    with st.spinner("Generating response..."):
        response = generate_response(question, api_key, selected_model, temperature, max_tokens)
    st.subheader("Response:")
    st.write(response)
else:
    st.info("Please enter a question and your Groq API key to get a response.")
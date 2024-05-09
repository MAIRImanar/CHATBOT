import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import streamlit as st
import google.generativeai as genai
from langchain.vectorstores import FAISS 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# read all pdf files and return text
def get_pdf_text(pdf_paths):  # Modify to take a list of PDF paths
    text = ""
    for pdf_path in pdf_paths:
        with open(pdf_path, "rb") as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            for page in pdf_reader.pages:
                text += page.extract_text()
    return text

# split text into chunks
def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000, chunk_overlap=1000)
    chunks = splitter.split_text(text)
    return chunks  # list of strings

# get embeddings for each chunk
def get_vector_store(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001")  # type: ignore
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    User_question: \n{user_question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro",
                                   client=genai,
                                   temperature=0.3,
                                   )
    prompt = PromptTemplate(template=prompt_template,
                            input_variables=["context", "user_question"])
    chain = load_qa_chain(llm=model, chain_type="stuff", prompt=prompt)
    return chain

def clear_chat_history():
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello, I am a bot. How can I help you?"}]

def get_response(user_query):

    template = """
    You are a helpful assistant. Answer the following questions considering the history of the conversation:

    User question: {user_question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        
    chain = prompt | ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.1,
        convert_system_message_to_human=True
    ) | StrOutputParser()
    
    return chain.invoke({
        "user_question": user_query,
    })


def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001")  # type: ignore
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain(
        {"input_documents": docs, "user_question": user_question}, return_only_outputs=True, )
    print(response)
    if response is not None and response['output_text']:
        return response['output_text']
    else:
        # If no answer is found in the provided PDFs, invoke Gemini AI
        return get_response(user_question)

def main():
    st.set_page_config(
        page_title="E16_bot",
        page_icon="🤖",
        layout="wide"
    )
    # Custom HTML for setting background color
    st.markdown(
        """
        <style>
        body {
            background-color: #3498db; /* Blue color */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Sidebar for uploading PDF files
    pdf_paths = ["Banque_AR.pdf", "Banque_AR.pdf"]  # Modify this line with the paths to your PDFs
    raw_text = get_pdf_text(pdf_paths)  # Fetch text directly from the PDF files
    text_chunks = get_text_chunks(raw_text)
    get_vector_store(text_chunks)

    # Main content area for displaying chat messages
    st.title("Chatbot🤖")
    st.write("Welcome to the chat!")
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)
  
    # Chat input
    # Placeholder for chat messages

    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant", "content":"Hello, I am a bot. How can I help you?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Display chat messages and bot response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = user_input(prompt)
                placeholder = st.empty()
                full_response = ''
                for item in response:
                    full_response += item
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)
        if response is not None:
            message = {"role": "assistant", "content": full_response}
            st.session_state.messages.append(message)

if __name__ == "__main__":
    main()

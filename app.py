import streamlit as st 
import tempfile
from streamlit_chat import message
from langchain_community.llms import Ollama
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
from langchain.chains import ConversationalRetrievalChain
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.csv_loader import CSVLoader

# load langchain llama model
# you can load any other llms here.
def load_llm():

    # EXAMPLE: loading locally downloaded model using CTransformers
    # llm = CTransformers(
    #     model = "llama-2-7b-chat.ggmlv3.q8_0.bin",
    #     model_type="llama",
    #     max_new_tokens = 512,
    #     temperature = 0.5
    # )

    # EXAMPLE: loading Ollama model from locally deployed instance
    llm = Ollama(base_url = 'http://localhost:11434', model ='llama2')
    return llm

st.title("Chat with your CSVs")
st.markdown("<h3 style='text-align: center; color: white;'></h3>", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Upload your Data", type="csv")

if uploaded_file:

   #use tempfile because CSVLoader only accepts a file_path
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    # load the csv files
    loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8", csv_args={
                'delimiter': ','})
    data = loader.load()

    # split the document into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap =0)
    all_splits = text_splitter.split_documents(data)

    vectorstore = Chroma.from_documents(documents = all_splits, embedding = GPT4AllEmbeddings())
    ollama = load_llm()
    qachain = RetrievalQA.from_chain_type(ollama, retriever =vectorstore.as_retriever() )
    chain = ConversationalRetrievalChain.from_llm(llm=ollama, retriever=vectorstore.as_retriever() )

    def conversational_chat(query):
            result = chain({"question": query, "chat_history": st.session_state['history']})
            st.session_state['history'].append((query, result["answer"]))
            return result["answer"]

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! Ask me anything about your order!"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey! 👋"]
        
    #container for the chat history
    response_container = st.container()
    #container for the user's text input
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            
            user_input = st.text_input("Query:", placeholder="Talk to your csv data here (:", key='input')
            submit_button = st.form_submit_button(label='Send')
            
        if submit_button and user_input:
            output = conversational_chat(user_input)
            
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")






import streamlit as st
import chromadb
from chromadb.config import Settings
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document
import os
import tempfile
from dotenv import load_dotenv
from typing import List
import uuid

# Load environment variables
load_dotenv()

# Initialize OpenAI API key
api_key = None

# Try to get API key from environment variables first
if "OPENAI_API_KEY" in os.environ:
    api_key = os.environ["OPENAI_API_KEY"]
else:
    # Try Streamlit secrets
    try:
        api_key = st.secrets.get("OPENAI_API_KEY", None)
    except:
        pass

# If still not found, ask user to input it
if not api_key:
    st.sidebar.title("🔑 API Key Required")
    api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password", help="Enter your OpenAI API key to use the app")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        st.sidebar.success("✅ API key saved for this session")
    else:
        st.warning("⚠️ Please enter your OpenAI API key in the sidebar to continue.")
        st.info("💡 You can also set it via:\n- Streamlit Cloud Secrets (for deployed apps)\n- Environment variable: `OPENAI_API_KEY`\n- `.env` file in the project directory")
        st.stop()

# Page configuration
st.set_page_config(
    page_title="PDF Chat Assistant",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pdf_documents" not in st.session_state:
    st.session_state.pdf_documents = {}
if "memory" not in st.session_state:
    st.session_state.memory = None

def process_pdf(file) -> List[Document]:
    """Process PDF file and return chunked documents with page numbers"""
    # Save uploaded file to temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(file.read())
        tmp_path = tmp_file.name
    
    try:
        # Load PDF
        loader = PyPDFLoader(tmp_path)
        pages = loader.load()
        
        # Add metadata with page numbers
        for i, page in enumerate(pages):
            page.metadata['page_number'] = i + 1
            page.metadata['source_file'] = file.name
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        chunks = text_splitter.split_documents(pages)
        
        return chunks
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

def create_vectorstore(documents: List[Document]):
    """Create ChromaDB vectorstore with documents"""
    # Initialize embeddings (will use OPENAI_API_KEY from environment)
    embeddings = OpenAIEmbeddings()
    collection_name = "pdf_chat_collection"
    
    # Create vectorstore
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory="./chroma_db"
    )
    
    return vectorstore

def add_to_vectorstore(vectorstore, documents: List[Document]):
    """Add documents to existing vectorstore"""
    ids = [str(uuid.uuid4()) for _ in documents]
    vectorstore.add_documents(documents=documents, ids=ids)
    return vectorstore

def get_qa_chain(vectorstore):
    """Create a QA chain with memory"""
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    # Initialize or reuse memory
    if st.session_state.memory is None:
        st.session_state.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
    
    # Create retrieval chain
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        memory=st.session_state.memory,
        return_source_documents=True,
        verbose=False
    )
    
    return qa_chain

# Main UI
st.title("📚 PDF Chat Assistant")
st.markdown("Upload PDF files and ask questions about their content!")

# Sidebar for PDF upload
with st.sidebar:
    st.header("📄 Upload PDF Files")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        help="Upload a PDF file to start asking questions"
    )
    
    if uploaded_file is not None:
        if st.button("Process PDF", type="primary"):
            with st.spinner("Processing PDF..."):
                try:
                    # Process PDF
                    chunks = process_pdf(uploaded_file)
                    
                    # Create or update vectorstore
                    if st.session_state.vectorstore is None:
                        st.session_state.vectorstore = create_vectorstore(chunks)
                    else:
                        # Add new documents to existing vectorstore
                        st.session_state.vectorstore = add_to_vectorstore(st.session_state.vectorstore, chunks)
                    
                    # Store document metadata
                    st.session_state.pdf_documents[uploaded_file.name] = {
                        "num_pages": len(set(chunk.metadata.get('page_number', 0) for chunk in chunks)),
                        "num_chunks": len(chunks)
                    }
                    
                    st.success(f"✅ PDF processed successfully! ({len(chunks)} chunks created)")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error processing PDF: {str(e)}")
    
    # Show uploaded documents
    if st.session_state.pdf_documents:
        st.header("📚 Processed Documents")
        for doc_name, doc_info in st.session_state.pdf_documents.items():
            st.text(f"• {doc_name}")
            st.caption(f"  {doc_info['num_chunks']} chunks, {doc_info['num_pages']} pages")
    
    # Clear chat button
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.session_state.memory = None
        st.rerun()

# Chat interface
if st.session_state.vectorstore is None:
    st.info("👈 Please upload and process a PDF file to start chatting!")
else:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sources" in message:
                with st.expander("📄 View Sources"):
                    for source in message["sources"]:
                        st.text(f"Page {source['page']} from {source['file']}")
                        st.caption(source['snippet'][:200] + "...")
    
    # Chat input
    if prompt := st.chat_input("Ask a question about the PDF..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    qa_chain = get_qa_chain(st.session_state.vectorstore)
                    result = qa_chain({"question": prompt})
                    
                    answer = result["answer"]
                    source_documents = result.get("source_documents", [])
                    
                    # Display answer
                    st.markdown(answer)
                    
                    # Extract source information
                    sources = []
                    for doc in source_documents:
                        page_num = doc.metadata.get('page_number', 'Unknown')
                        source_file = doc.metadata.get('source_file', 'Unknown')
                        snippet = doc.page_content[:300]
                        sources.append({
                            "page": page_num,
                            "file": source_file,
                            "snippet": snippet
                        })
                    
                    # Display sources
                    if sources:
                        with st.expander("📄 View Sources"):
                            for source in sources:
                                st.markdown(f"**Page {source['page']}** from `{source['file']}`")
                                st.caption(f'"{source["snippet"]}..."')
                                st.divider()
                    
                    # Add assistant message to chat
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })
                    
                except Exception as e:
                    error_msg = f"Error generating response: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })

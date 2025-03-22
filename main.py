import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, Document
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.response_synthesizers import get_response_synthesizer
import os
import sys
import PyPDF2
import glob
            
openai_key = os.environ.get("OPENAI_API_KEY")

def read_pdf_files(pdf_directory):
    pdf_texts = []
    pdf_files = glob.glob(os.path.join(pdf_directory, "*.pdf"))
    
    for pdf_file in pdf_files:
        try:
            with open(pdf_file, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
                
                file_name = os.path.basename(pdf_file)
                pdf_texts.append({"file_name": file_name, "text": text})
                
                print(f"Successfully read PDF: {file_name}")
        except Exception as e:
            print(f"Error reading PDF {pdf_file}: {str(e)}")
    
    return pdf_texts

def main():
    st.set_page_config(page_title="PDF Reader")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat header
    st.title("PDF reader")
    st.subheader("Your personal assistant")

    # Read PDF files
    pdf_dir = "C:/Users/gupta/OneDrive/Desktop/LLMS/random builds/classment_assignment"
    pdf_texts = read_pdf_files(pdf_dir)
    
    documents = []
    for pdf_text in pdf_texts:
        document = Document(
            text=pdf_text["text"],
            metadata={"filename": pdf_text["file_name"]}
        )
        documents.append(document)
    
    index = VectorStoreIndex.from_documents(documents)
    retriever = index.as_retriever(streaming=True, similarity_top_k=3)
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input and response
    if prompt := st.chat_input("How can I help you?"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        try:
            # Generate response using streaming
            response_synthesizer = get_response_synthesizer(
                response_mode="tree_summarize",
                streaming=True
            )
            query_engine = RetrieverQueryEngine(
                retriever=retriever,
                response_synthesizer=response_synthesizer,
            )
            
            # Stream response
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                full_response = ""
                
                # Get streaming response
                streaming_response = query_engine.query(prompt)
                for chunk in streaming_response.response_gen:
                    if chunk:
                        full_response += chunk
                        response_placeholder.markdown(full_response + "▌")
                
                # Display final response
                response_placeholder.markdown(full_response)
            
            # Add complete response to history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": full_response
            })

        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
                    
if __name__ == "__main__":
    main()

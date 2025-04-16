# Set page layout to wide
st.set_page_config(layout="wide")

st.title("Colpali Based Multimodal RAG App")

# Import necessary libraries
import os
import uuid
import base64
from io import BytesIO
from PIL import Image
import streamlit as st

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Create a directory to save uploaded PDFs
upload_dir = "uploads"
os.makedirs(upload_dir, exist_ok=True)

# Create sidebar for configuration options
with st.sidebar:
    st.header("Configuration Options")
    
    # Dropdown for selecting Colpali model
    colpali_model = st.selectbox(
        "Select Colpali Model",
        options=["vidore/colpali", "vidore/colpali-v1.2", "vidore/colqwen2-v1.0"]
    )
    
    # Dropdown for selecting Multi-Model LLM
    multi_model_llm = st.selectbox(
        "Select Multi-Model LLM",
        options=["gpt-4o", "Qwin", "Llama3.2"]
    )
    
    # File upload button for PDFs directly
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# Main content layout
if uploaded_file is not None:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("### Uploaded PDF file")
        
        # Save the uploaded PDF file locally
        pdf_path = os.path.join(upload_dir, uploaded_file.name)
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File saved: {uploaded_file.name}")

        # Load models
        @st.cache_resource
        def load_models(colpali_model):
            RAG = RAGMultiModalModel.from_pretrained(colpali_model, verbose=10)
            return RAG
        
        RAG = load_models(colpali_model)

        # Create a unique index name for the PDF
        index_name = f"{os.path.basename(pdf_path).replace('.pdf', '')}_{uuid.uuid4().hex}"
        print("Index name", index_name)
        
        st.subheader(f"Processing: {os.path.basename(pdf_path)}")
        with st.spinner(f"Indexing {index_name}..."):
            try:
                @st.cache_data
                def create_rag_index(pdf_path, index_name):
                    RAG.index(
                        input_path=pdf_path,
                        index_name=index_name,
                        store_collection_with_index=True,
                        overwrite=True,  # Ensure any existing index is cleared
                    )
                
                create_rag_index(pdf_path, index_name)
                st.success(f"Successfully indexed {os.path.basename(pdf_path)}")
            
            except ValueError as e:
                st.error(f"ValueError while indexing {os.path.basename(pdf_path)}: {e}")
            except Exception as e:
                st.error(f"Error while indexing {os.path.basename(pdf_path)}: {e}")
    
    with col2:
        # Display chat history
        st.subheader("Chat History")
        chat_container = st.container()
        
        with chat_container:
            for i, chat in enumerate(st.session_state.chat_history):
                # Display user message
                with st.chat_message("user"):
                    st.write(chat["query"])
                
                # Display assistant response
                with st.chat_message("assistant"):
                    st.write(chat["response"])
                    
                    # Show image if available
                    if "image" in chat:
                        with st.expander("View Image Evidence", expanded=False):
                            st.image(chat["image"], caption="Result Image", use_column_width=True)
        
        # Text input for new user query
        text_query = st.chat_input("Ask a question about the PDF...")
        
        if text_query:
            # Show user message immediately
            with st.chat_message("user"):
                st.write(text_query)
            
            # Show typing indicator while processing
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                message_placeholder.info("Searching and generating response...")
                
                with st.spinner("Processing..."):
                    # Search for relevant content
                    results = RAG.search(text_query, k=1, return_base64_results=True)
                    
                    if results and len(results) > 0:
                        # Decode the base64 image
                        image_data = base64.b64decode(results[0].base64)
                        image = Image.open(BytesIO(image_data))
                        
                        # Prepare message for LLM - without chat history context
                        # Only send the current query with the image
                        messages = [
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": text_query},
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/png;base64,{results[0].base64}"
                                        }
                                    },
                                ],
                            }
                        ]
                        
                        # Get response from LLM
                        response = client.chat.completions.create(
                            model=multi_model_llm,
                            messages=messages,
                            max_tokens=300,
                        )
                        
                        output = response.choices[0].message.content
                        
                        # Clear placeholder and display response
                        message_placeholder.empty()
                        st.write(output)
                        
                        # Show the evidence image in an expander
                        with st.expander("View Image Evidence", expanded=False):
                            st.image(image, caption="Result Image", use_column_width=True)
                        
                        # Save to chat history
                        st.session_state.chat_history.append({
                            "query": text_query,
                            "response": output,
                            "image": image
                        })
                    else:
                        # Clear placeholder and display no results message
                        message_placeholder.empty()
                        st.warning("No relevant information found in the PDF for your query.")
                        
                        # Still save to chat history even without results
                        st.session_state.chat_history.append({
                            "query": text_query,
                            "response": "No relevant information found in the PDF for your query."
                        })
else:
    st.info("Upload a PDF file to get started.")

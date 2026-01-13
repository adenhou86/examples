"""
Enhanced Multi-Hop-RAG system following the Multi-Hop-RAG paper methodology.

This implementation provides:
- Structured reasoning traces (Q1, A1, R1, Q2, A2, R2, ...)
- Missing information identification and targeting
- Document metadata tracking and transparency
- Token-efficient truncation and filtering
- Clear separation of reasoning trace and final answer

Key Components:
- Main function: get_multihop_rag_answer()
- Reasoning: _generate_structured_reasoning()
- Sub-question generation: _generate_next_subquestion_from_missing()
- Document processing: _truncate_documents(), _remove_duplicates_with_metadata()
- Final synthesis: _generate_final_answer_structured()

Author: Assistant
Date: 2024

MISSING COMPONENTS IDENTIFIED:
1. Imports (langchain, vector store, embeddings, etc.)
2. _retrieve_documents_simple() function
3. _remove_duplicates_with_metadata() function
4. Vector store initialization
5. LLM initialization
"""

# ============================================================================
# IMPORTS - These need to be added
# ============================================================================
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import hashlib

# LangChain imports (adjust based on your LangChain version)
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS, Chroma  # or your preferred vector store
from langchain_community.embeddings import HuggingFaceEmbeddings  # or OpenAIEmbeddings
from langchain_openai import ChatOpenAI  # or your preferred LLM
# Alternative: from langchain_community.llms import DeepSeek

# Optional: for loading documents
# from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter


# ============================================================================
# GLOBAL VARIABLES - Need to be initialized
# ============================================================================
# These should be initialized before calling get_multihop_rag_answer()

vector_store = None  # Your initialized vector store (FAISS, Chroma, Pinecone, etc.)
embeddings = None    # Your embedding model


# ============================================================================
# MISSING FUNCTION #1: _retrieve_documents_simple
# ============================================================================
def _retrieve_documents_simple(query: str, top_k: int = 3) -> List[Document]:
    """
    Retrieve documents from vector store based on query similarity.
    
    This function performs semantic search against the vector store
    to find the most relevant documents for the given query.
    
    Args:
        query (str): Search query string
        top_k (int): Number of top documents to retrieve
        
    Returns:
        List[Document]: List of retrieved documents with metadata
        
    Note:
        Requires 'vector_store' to be initialized globally or passed as parameter.
    """
    global vector_store
    
    if vector_store is None:
        raise ValueError(
            "Vector store is not initialized. "
            "Please initialize 'vector_store' before calling this function."
        )
    
    try:
        # Perform similarity search
        docs = vector_store.similarity_search(query, k=top_k)
        return docs
    except Exception as e:
        print(f"⚠️ Error retrieving documents: {e}")
        return []


# ============================================================================
# MISSING FUNCTION #2: _remove_duplicates_with_metadata
# ============================================================================
def _remove_duplicates_with_metadata(docs: List[Document]) -> List[Document]:
    """
    Remove duplicate documents while preserving hop metadata.
    
    This function deduplicates retrieved documents based on content hash,
    keeping the first occurrence and preserving its metadata. This prevents
    the same document from appearing multiple times in the final context.
    
    Args:
        docs (List[Document]): List of documents potentially containing duplicates
        
    Returns:
        List[Document]: Deduplicated list of documents
        
    Process:
        1. Generate content hash for each document
        2. Track seen hashes to identify duplicates
        3. Keep first occurrence of each unique document
        4. Preserve original metadata including hop information
    """
    seen_hashes = set()
    unique_docs = []
    
    for doc in docs:
        # Create hash based on content (you could also include metadata)
        content_hash = hashlib.md5(doc.page_content.encode()).hexdigest()
        
        # Alternative: hash based on chunk_id if available
        # chunk_id = doc.metadata.get('chunk_id', '')
        # content_hash = chunk_id if chunk_id else hashlib.md5(doc.page_content.encode()).hexdigest()
        
        if content_hash not in seen_hashes:
            seen_hashes.add(content_hash)
            unique_docs.append(doc)
    
    return unique_docs


# ============================================================================
# INITIALIZATION HELPER FUNCTIONS
# ============================================================================
def initialize_vector_store(
    documents: List[Document] = None,
    persist_directory: str = None,
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    store_type: str = "faiss"
) -> Any:
    """
    Initialize the vector store with documents or load from disk.
    
    Args:
        documents: List of documents to index (if creating new store)
        persist_directory: Path to load/save vector store
        embedding_model: HuggingFace model for embeddings
        store_type: Type of vector store ("faiss" or "chroma")
        
    Returns:
        Initialized vector store
    """
    global vector_store, embeddings
    
    # Initialize embeddings
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
    
    if store_type.lower() == "faiss":
        if persist_directory and documents is None:
            # Load existing FAISS index
            vector_store = FAISS.load_local(
                persist_directory, 
                embeddings,
                allow_dangerous_deserialization=True
            )
        elif documents:
            # Create new FAISS index
            vector_store = FAISS.from_documents(documents, embeddings)
            if persist_directory:
                vector_store.save_local(persist_directory)
    
    elif store_type.lower() == "chroma":
        if persist_directory:
            vector_store = Chroma(
                persist_directory=persist_directory,
                embedding_function=embeddings
            )
        elif documents:
            vector_store = Chroma.from_documents(documents, embeddings)
    
    return vector_store


def initialize_llm(
    model_name: str = "gpt-3.5-turbo",
    api_key: str = None,
    temperature: float = 0.0,
    **kwargs
) -> Any:
    """
    Initialize the LLM for reasoning and answer generation.
    
    Args:
        model_name: Name of the model to use
        api_key: API key (or set via environment variable)
        temperature: Sampling temperature
        **kwargs: Additional model parameters
        
    Returns:
        Initialized LLM instance
    """
    # For OpenAI models
    llm = ChatOpenAI(
        model=model_name,
        api_key=api_key,
        temperature=temperature,
        **kwargs
    )
    
    # Alternative for DeepSeek or other providers:
    # from langchain_community.chat_models import ChatDeepSeek
    # llm = ChatDeepSeek(model=model_name, api_key=api_key, temperature=temperature)
    
    return llm


# ============================================================================
# MAIN FUNCTIONS FROM ORIGINAL CODE
# ============================================================================

def get_multihop_rag_answer(query: str, llm, max_hops=3, docs_per_hop=3, chunk_word_limit=300) -> str:
    """
    Multi-hop retrieval with structured reasoning steps (enhanced MultiHop-RAG).

    This is the main function that orchestrates the entire multi-hop retrieval process.
    It performs iterative retrieval, reasoning, and sub-question generation to comprehensively
    answer complex questions that may require information from multiple sources.

    Args:
        query (str): The original user question to be answered
        llm: DeepSeek LLM instance for reasoning and query generation
        max_hops (int, optional): Maximum number of retrieval hops to perform. Defaults to 3.
            Each hop consists of query -> retrieve -> reason -> next query
        docs_per_hop (int, optional): Number of top documents to retrieve per hop. Defaults to 3.
            Controls retrieval breadth vs. focus
        chunk_word_limit (int, optional): Maximum words per document chunk to prevent prompt bloat.
            Defaults to 300. Helps manage token usage

    Returns:
        str: Comprehensive answer formatted with:
            - Multi-hop reasoning trace (Q1, A1, R1, Q2, A2, R2, ...)
            - Synthesized final answer
            - Document source metadata for transparency

    Process Flow:
        1. For each hop (up to max_hops):
            a. Retrieve documents for current query
            b. Generate structured reasoning (insights, reasoning, missing info)
            c. Generate next sub-question based on missing information
        2. Deduplicate and combine all retrieved documents
        3. Generate final answer using both documents and reasoning trace
        4. Format output with clear section separation

    Example:
        >>> answer = get_multihop_rag_answer(
        ...     "What was Apple's R&D spending in 2023?",
        ...     llm,
        ...     max_hops=2,
        ...     docs_per_hop=5
        ... )
        >>> print(answer)

    Raises:
        ValueError: If llm is None or invalid
        Exception: For retrieval, reasoning, or generation errors
    """

    print("🔎 ENHANCED MULTIHOP-RAG WITH STRUCTURED REASONING")
    print("=" * 60)
    print(f"🧭 Max hops: {max_hops} | Docs per hop: {docs_per_hop} | Word limit: {chunk_word_limit}")

    try:
        # Validate LLM
        if llm is None:
            raise ValueError("LLM is None. Please ensure the LLM is properly initialized.")

        all_retrieved_docs = []
        current_query = query
        reasoning_trace = {
            'hops': [],      # Structured reasoning for each hop
            'summary': ''    # Overall reasoning summary
        }

        # Multi-hop retrieval process with structured reasoning
        for hop in range(max_hops):
            hop_num = hop + 1
            print(f"\n🔁 HOP {hop_num}")
            print("-" * 50)

            # Step 1: Display current query
            if hop == 0:
                print(f"📝 Q{hop_num} (Original): {current_query}")
            else:
                print(f"📝 Q{hop_num} (Sub-question): {current_query}")

            # Step 2: Retrieve documents for current query
            hop_docs = _retrieve_documents_simple(current_query, top_k=docs_per_hop)
            print(f"📄 Retrieved {len(hop_docs)} documents")

            # Step 3: Truncate documents and add metadata
            truncated_docs = _truncate_documents(hop_docs, chunk_word_limit, hop_num)
            all_retrieved_docs.extend(truncated_docs)

            # Step 4: Display retrieved document metadata
            print(f"\n📑 A{hop_num} (Retrieved Documents):")
            for i, doc in enumerate(truncated_docs, 1):
                metadata = doc.metadata
                company = metadata.get('company', 'Unknown').replace(' (1)', '')
                chunk_id = metadata.get('chunk_id', 'Unknown')
                source = metadata.get('source', 'Unknown')
                hop_val = metadata.get('hop', '?')
                print(f"  {i}. {company} | Chunk: {chunk_id} | Source: {source} | Hop: {hop_val}")

            # Step 5: Generate structured reasoning step
            print(f"\n🧠 R{hop_num} (Reasoning):")
            reasoning_step = _generate_structured_reasoning(
                query, current_query, truncated_docs, reasoning_trace, llm, hop_num
            )

            # Store structured reasoning
            hop_reasoning = {
                'hop': hop_num,
                'question': current_query,
                'retrieved_docs': len(truncated_docs),
                'reasoning': reasoning_step['reasoning'],
                'missing_info': reasoning_step['missing_info'],
                'insights': reasoning_step['insights']
            }
            reasoning_trace['hops'].append(hop_reasoning)

            print(f"  Insights: {reasoning_step['insights']}")
            print(f"  Reasoning: {reasoning_step['reasoning']}")
            print(f"  Still Missing: {reasoning_step['missing_info']}")

            # Step 6: Generate next sub-question based on missing info (if not last hop)
            if hop < max_hops - 1 and reasoning_step['missing_info'].lower() not in ['none', 'nothing', 'no missing information']:
                current_query = _generate_next_subquestion_from_missing(
                    query, reasoning_step['missing_info'], llm, hop_num
                )
                print(f"\n➡️ Next sub-question generated from missing info")
            elif hop < max_hops - 1:
                print(f"\n✅ Sufficient information found, but continuing to hop {hop_num + 1} for completeness")
                break

        print(f"\n📊 RETRIEVAL SUMMARY:")
        print(f"Total documents retrieved: {len(all_retrieved_docs)}")

        # Remove duplicates while preserving hop information
        unique_docs = _remove_duplicates_with_metadata(all_retrieved_docs)
        print(f"Unique documents: {len(unique_docs)}")

        # Generate final answer with structured reasoning and metadata
        final_answer = _generate_final_answer_structured(query, unique_docs, reasoning_trace, llm)

        print(f"✅ Enhanced MultiHop-RAG Answer Generated")
        print("=" * 60)

        return final_answer

    except Exception as e:
        error_msg = f"Error in Enhanced MultiHop-RAG: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg


def _generate_structured_reasoning(original_query: str, current_query: str, hop_docs, reasoning_trace, llm, hop_num: int) -> dict:
    """
    Generate structured reasoning with explicit missing information identification.
    
    This function analyzes the documents retrieved in the current hop and generates
    a structured reasoning step that includes insights, reasoning, and identification
    of missing information. This follows the MultiHop-RAG paper's approach of
    explicit reasoning after each retrieval step.
    
    Args:
        original_query (str): The original user question for context
        current_query (str): The current hop's sub-question
        hop_docs (list): List of documents retrieved in this hop
        reasoning_trace (dict): Previous reasoning steps for context
        llm: LLM instance for generating reasoning
        hop_num (int): Current hop number for labeling
    
    Returns:
        dict: Structured reasoning with keys:
            - 'insights': What was learned from the documents
            - 'reasoning': How this helps answer the original question
            - 'missing_info': What information is still needed
    
    Process:
        1. Prepare context from current hop documents (truncated)
        2. Gather previous reasoning steps for continuity
        3. Prompt LLM for structured analysis (insights, reasoning, missing)
        4. Parse and structure the LLM response
        5. Return structured reasoning components
    
    Example Output:
        {
            'insights': 'Found Apple R&D spending of $29.9B in 2023',
            'reasoning': 'This directly answers the spending amount',
            'missing_info': 'Historical comparison would provide context'
        }
    """
    
    # Prepare context from current hop documents
    hop_context = ""
    if hop_docs:
        hop_context = "\n".join([
            f"Doc {i+1}: {doc.page_content[:200]}..."
            for i, doc in enumerate(hop_docs)
        ])
    else:
        hop_context = "No relevant documents found in this hop."
    
    # Prepare previous reasoning context
    previous_insights = []
    if reasoning_trace['hops']:
        for i, hop_data in enumerate(reasoning_trace['hops']):
            previous_insights.append(f"Q{i+1}: {hop_data['question']}")
            previous_insights.append(f"A{i+1}: {hop_data['insights']}")
            previous_insights.append(f"R{i+1}: {hop_data['reasoning']}")
    
    previous_context = "\n".join(previous_insights) if previous_insights else "None (this is the first hop)"
    
    reasoning_prompt = f"""Analyze the retrieved documents and provide structured reasoning for this multi-hop retrieval step.

ORIGINAL QUESTION: {original_query}
CURRENT SUB-QUESTION (Q{hop_num}): {current_query}

PREVIOUS REASONING TRACE:
{previous_context}

RETRIEVED DOCUMENTS (A{hop_num}):
{hop_context}

Provide a structured analysis with three components:

1. INSIGHTS: What key information did you learn from these documents? (1-2 sentences)
2. REASONING: How does this information help answer the original question? (1-2 sentences)
3. MISSING_INFO: What specific information is still missing to fully answer the original question? Be explicit. If nothing is missing, say "No missing information" (1 sentence)

Format your response as:
INSIGHTS: [your insights]
REASONING: [your reasoning]
MISSING_INFO: [what's still missing or "No missing information"]"""
    
    try:
        response = llm.invoke(reasoning_prompt)
        content = response.content.strip()
        
        # Parse structured response
        insights = ""
        reasoning = ""
        missing_info = ""
        
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('INSIGHTS:'):
                current_section = 'insights'
                insights = line.replace('INSIGHTS:', '').strip()
            elif line.startswith('REASONING:'):
                current_section = 'reasoning'
                reasoning = line.replace('REASONING:', '').strip()
            elif line.startswith('MISSING_INFO:'):
                current_section = 'missing_info'
                missing_info = line.replace('MISSING_INFO:', '').strip()
            elif current_section and line:
                if current_section == 'insights':
                    insights += " " + line
                elif current_section == 'reasoning':
                    reasoning += " " + line
                elif current_section == 'missing_info':
                    missing_info += " " + line
        
        return {
            'insights': insights or f"Retrieved {len(hop_docs)} documents from hop {hop_num}",
            'reasoning': reasoning or "Information contributes to understanding the original question",
            'missing_info': missing_info or "Additional context may be helpful"
        }
    
    except Exception as e:
        print(f"⚠️ Error in structured reasoning: {e}")
        return {
            'insights': f"Retrieved {len(hop_docs)} documents",
            'reasoning': "Analysis step encountered an error",
            'missing_info': "Unable to determine missing information"
        }


def _generate_next_subquestion_from_missing(original_query: str, missing_info: str, llm, current_hop: int) -> str:
    """
    Generate next sub-question specifically targeting the identified missing information.

    This function creates a focused sub-question based on the missing information
    identified in the current hop's reasoning step. This ensures that each subsequent
    hop is purposeful and targets specific information gaps.

    Args:
        original_query (str): The original user question for context
        missing_info (str): Specific missing information identified in reasoning
        llm: LLM instance for generating the sub-question
        current_hop (int): Current hop number for context

    Returns:
        str: Generated sub-question targeting the missing information

    Process:
        1. Analyze the missing information gap
        2. Generate a targeted sub-question to fill this gap
        3. Ensure the sub-question is specific and actionable
        4. Return the focused sub-question for next hop

    Example:
        missing_info = "Historical comparison would provide context"
        returns = "Apple R&D spending trends over past 3 years comparison"
    """
    subquestion_prompt = f"""Generate a specific sub-question to find the missing information identified in the reasoning step.

ORIGINAL QUESTION: {original_query}
MISSING INFORMATION: {missing_info}
CURRENT HOP: {current_hop}

Based on the missing information, create a targeted sub-question that will help retrieve documents containing this specific information.

The sub-question should:
1. Directly address the missing information gap
2. Use specific terminology related to the missing information
3. Be concise and focused
4. Be different from previous queries

Provide only the sub-question:"""

    try:
        response = llm.invoke(subquestion_prompt)
        sub_question = response.content.strip().strip('"""').strip("'''")
        return sub_question

    except Exception as e:
        print(f"⚠️ Error generating targeted sub-question: {e}")
        return original_query


def _truncate_documents(docs, word_limit: int, hop_num: int):
    """
    Truncate documents to word limit and add hop metadata for token efficiency.

    This function processes retrieved documents to ensure they don't exceed
    the specified word limit, preventing prompt bloat while preserving
    essential information. It also adds hop tracking metadata.

    Args:
        docs (list): List of document objects to truncate
        word_limit (int): Maximum number of words per document
        hop_num (int): Current hop number to add to metadata

    Returns:
        list: List of truncated documents with hop metadata
    """
    truncated_docs = []
    
    for doc in docs:
        # Truncate content to word limit
        words = doc.page_content.split()
        if len(words) > word_limit:
            truncated_content = " ".join(words[:word_limit]) + "..."
            doc.page_content = truncated_content
        
        # Add hop metadata
        doc.metadata['hop'] = hop_num
        
        truncated_docs.append(doc)
    
    return truncated_docs


def _generate_final_answer_structured(query: str, docs, reasoning_trace, llm) -> str:
    """
    Generate final answer with clear separation of reasoning trace and synthesized answer.
    
    This function creates the final output by combining the multi-hop reasoning trace
    with a synthesized answer based on all retrieved documents. It provides clear
    formatting with distinct sections for transparency and readability.
    
    Args:
        query (str): Original user question
        docs (list): All unique documents retrieved across hops
        reasoning_trace (dict): Complete reasoning trace from all hops
        llm: LLM instance for final answer synthesis
    
    Returns:
        str: Formatted final answer with:
            - Multi-hop reasoning trace section
            - Synthesized answer section
            - Document sources section with metadata
    
    Process:
        1. Format reasoning trace in Q1, A1, R1, Q2, A2, R2 structure
        2. Prepare document context with metadata headers
        3. Generate synthesized answer using trace and documents
        4. Format final output with clear section separation
        5. Add document source summary for transparency
    
    Output Structure:
        🔍 MULTI-HOP REASONING TRACE:
        [Structured reasoning steps]
        
        🎯 SYNTHESIZED ANSWER:
        [Comprehensive answer]
        
        📄 DOCUMENT SOURCES:
        [Source metadata list]
    """
    
    # Prepare structured reasoning trace for display
    reasoning_display = []
    for hop_data in reasoning_trace['hops']:
        hop_num = hop_data['hop']
        reasoning_display.append(f"Q{hop_num}: {hop_data['question']}")
        reasoning_display.append(f"A{hop_num}: Retrieved {hop_data['retrieved_docs']} documents - {hop_data['insights']}")
        reasoning_display.append(f"R{hop_num}: {hop_data['reasoning']}")
        if hop_data['missing_info'].lower() not in ['no missing information', 'none', 'nothing']:
            reasoning_display.append(f"Missing: {hop_data['missing_info']}")
        reasoning_display.append("")  # Empty line for readability
    
    reasoning_context = "\n".join(reasoning_display)
    
    # Prepare document context with metadata
    doc_context_parts = []
    for i, doc in enumerate(docs, 1):
        metadata = doc.metadata
        company = metadata.get('company', 'Unknown').replace(' (1)', '')
        chunk_id = metadata.get('chunk_id', 'Unknown')
        source = metadata.get('source', 'Unknown')
        hop = metadata.get('hop', '?')
        
        doc_header = f"Document {i} [Company: {company}, Chunk: {chunk_id}, Source: {source}, Hop: {hop}]:"
        doc_context_parts.append(f"{doc_header}\n{doc.page_content}")
    
    document_context = "\n\n".join(doc_context_parts)
    
    final_prompt = f"""Provide a comprehensive answer using the multi-hop reasoning trace and retrieved documents.

ORIGINAL QUESTION: {query}

MULTI-HOP REASONING TRACE:
{reasoning_context}

RETRIEVED DOCUMENTS WITH METADATA:
{document_context}

INSTRUCTIONS:
- Provide a clear, comprehensive answer to the original question
- Use information from all hops and reasoning steps
- Include specific details, numbers, and facts from the documents
- Reference the hop number and source when mentioning specific information
- Structure your answer logically, building from the reasoning trace

ANSWER:"""
    
    try:
        response = llm.invoke(final_prompt)
        synthesized_answer = response.content.strip()
        print(f"✅ Final Answer Generated")
        print("=" * 60)
        print(f"🎯 Synthesized Answer: {synthesized_answer}")
        
        # Format final output with clear separation
        final_output = f"""
🔍 MULTI-HOP REASONING TRACE:
{'=' * 40}
{reasoning_context}

🎯 SYNTHESIZED ANSWER:
{'=' * 40}
{synthesized_answer}

📄 DOCUMENT SOURCES:
{'=' * 40}"""
        
        # Add document source summary
        for i, doc in enumerate(docs, 1):
            metadata = doc.metadata
            company = metadata.get('company', 'Unknown').replace(' (1)', '')
            chunk_id = metadata.get('chunk_id', 'Unknown')
            source = metadata.get('source', 'Unknown')
            hop = metadata.get('hop', '?')
            
            final_output += f"\n{i}. {company} - {source} (Chunk: {chunk_id}, Hop: {hop})"
        
        return final_output
        
    except Exception as e:
        print(f"❌ Error generating final answer: {e}")
        return f"Error generating answer: {str(e)}"


# ============================================================================
# EXAMPLE USAGE
# ============================================================================
if __name__ == "__main__":
    """
    Example usage of the Multi-Hop RAG system.
    
    Before running:
    1. Install required packages:
       pip install langchain langchain-community langchain-openai faiss-cpu sentence-transformers
       
    2. Set your API key:
       export OPENAI_API_KEY="your-api-key"
       
    3. Prepare your documents and create a vector store
    """
    
    import os
    
    # Example: Initialize components
    print("=" * 60)
    print("MULTI-HOP RAG SYSTEM - EXAMPLE USAGE")
    print("=" * 60)
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️ Warning: OPENAI_API_KEY not set. Please set it before running.")
        print("   export OPENAI_API_KEY='your-api-key'")
    
    # Example initialization (uncomment and modify as needed):
    """
    # 1. Load and prepare documents
    from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    
    loader = DirectoryLoader("./documents", glob="**/*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(documents)
    
    # 2. Initialize vector store
    vector_store = initialize_vector_store(
        documents=splits,
        persist_directory="./vector_store",
        embedding_model="sentence-transformers/all-MiniLM-L6-v2",
        store_type="faiss"
    )
    
    # 3. Initialize LLM
    llm = initialize_llm(
        model_name="gpt-3.5-turbo",
        temperature=0.0
    )
    
    # 4. Run Multi-Hop RAG
    query = "What was Apple's R&D spending in 2023 and how does it compare to previous years?"
    
    answer = get_multihop_rag_answer(
        query=query,
        llm=llm,
        max_hops=3,
        docs_per_hop=5,
        chunk_word_limit=300
    )
    
    print(answer)
    """
    
    print("\n📖 To use this system:")
    print("1. Initialize your vector store with documents")
    print("2. Initialize your LLM (OpenAI, DeepSeek, etc.)")
    print("3. Call get_multihop_rag_answer() with your query")
    print("\nSee the commented example code above for details.")

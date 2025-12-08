from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
from dotenv import load_dotenv

# LangChain libraries
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

app = Flask(__name__)
CORS(app)

# --- Knowledge Base Settings ---
vectorstore = None
DB_FAISS_PATH = 'vectorstore/db_faiss' # Embeddings Save folder

def initialize_knowledge_base():
    global vectorstore
    
    # HuggingFace Embeddings Model
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 1. Check if previously saved Embeddings exist
    if os.path.exists(DB_FAISS_PATH):
        print("🔄 Using previously created Embeddings (Cache)...")
        try:
            # If available, load directly (takes seconds)
            vectorstore = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
            print("✅ Knowledge Base Loaded from Cache!")
            return
        except Exception as e:
            print(f"⚠️ Cache loading error: {e}. Rebuilding...")

    # 2. new pdf embeddings creating
    print("🔄 Reading PDFs and creating embeddings...")
    
    pdf_paths = [
        "data/Maternal & Newborn Strat Plan .pdf", 
        "data/maternal_care_healthcare_workers.pdf"
    ] 
    
    all_docs = []
    for pdf_path in pdf_paths:
        if os.path.exists(pdf_path):
            print(f"   📄 Loading: {pdf_path}")
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()
            all_docs.extend(docs)
        else:
            print(f"⚠️ PDF not found: {pdf_path}")

    if all_docs:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        splits = text_splitter.split_documents(all_docs)
        
        # Vector Store development
        vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
        
        # 3. save into local directory for future use
        vectorstore.save_local(DB_FAISS_PATH)
        print("✅ Knowledge Base Created & Saved Locally!")
    else:
        print("⚠️ PDF නොමැත.")

# Start by initializing the knowledge base
initialize_knowledge_base()

# --- Chat Function ---
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_question = data.get('question', '')
    image_base64 = data.get('image', None)

   #large language model for generating answers
   
    llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0.3)
    
    system_instruction = (
        "ඔබ ශ්‍රී ලංකාවේ මාතෘ සහ ළදරු සෞඛ්‍ය පිළිබඳ සහායක AI නිලධාරියෙකි. "
        "පිළිතුරු සිංහලෙන් ලබා දෙන්න. මෙය වෛද්‍ය උපදෙසක් නොවන බව කරුණාවෙන් සලකන්න."
    )

    context_text = ""
    if vectorstore:
        try:
            retriever = vectorstore.as_retriever()
            relevant_docs = retriever.invoke(user_question)
            context_text = "\n\n".join([d.page_content for d in relevant_docs])
        except Exception as e:
            print(f"Retrieval Error: {e}")

    messages = [SystemMessage(content=system_instruction)]
    
    if image_base64:
        content = [
            {"type": "text", "text": f"Context: {context_text}\n\nQuestion: {user_question}"},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
        ]
        messages.append(HumanMessage(content=content))
    else:
        messages.append(HumanMessage(content=f"Context: {context_text}\n\nQuestion: {user_question}"))

    try:
        response = llm.invoke(messages)
        return jsonify({"answer": response.content})
    except Exception as e:
        return jsonify({"answer": "සමාවන්න, දෝෂයක් ඇති විය.", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
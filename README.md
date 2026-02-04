# Maternal & Newborn Health Chatbot Assistant (Sri Lanka)

This project is an AI-powered chatbot designed to assist with maternal and newborn health queries in Sri Lanka. It utilizes **Retrieval-Augmented Generation (RAG)** to provide accurate, context-aware responses in **Sinhala**, based on provided medical documents and strategic plans.

## 🚀 Features

- **Specialized Knowledge Base**: Built on official documents like "Maternal & Newborn Strat Plan" and healthcare worker guidelines.
- **Sinhala Language Support**: tailored to respond in Sinhala, acting as a helpful AI health officer.
- **Multimodal Capabilities**: Capable of processing both text questions and images to provide relevant advice.
- **RAG Architecture**: Uses FAISS vector store and HuggingFace embeddings to retrieve relevant context before generating answers with Google Gemini.

## 🛠️ Technology Stack

- **Python** (Backend Logic)
- **Flask** (Web Server)
- **LangChain** (LLM Framework)
- **Google Gemini** (Generative AI Model)
- **FAISS** (Vector Database)
- **HuggingFace** (Embeddings)

## 📂 Project Structure

```
chatbot/
├── data/                  # Source PDF documents for the knowledge base
├── vectorstore/           # Persisted FAISS vector index
├── server.py              # Main Flask application entry point
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (API Keys)
└── README.md              # Project documentation
```

## ⚙️ Setup & Installation

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd chatbot
    ```

2.  **Create a Virtual Environment (Recommended)**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    Note: Ensure you have C++ build tools installed if required by FAISS.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables**
    Create a `.env` file in the root directory and add your Google API Key:
    ```env
    GOOGLE_API_KEY=your_google_api_key_here
    ```

5.  **Prepare Data**
    Ensure your PDF documents are placed in the `data/` directory. The system looks for:
    - `Maternal & Newborn Strat Plan .pdf`
    - `maternal_care_healthcare_workers.pdf`

## 🏃‍♂️ Usage

1.  **Start the Server**
    ```bash
    python server.py
    ```
    *On the first run, the system will process the PDFs in the `data/` folder to build the vector index. This may take a few moments.*

2.  **API Endpoint**
     The server runs on `http://localhost:3000`.

    **POST** `/chat`
    
    **Request Body (JSON):**
    ```json
    {
      "question": "මාතෘ සෞඛ්‍ය යනු කුමක්ද?",
      "image": "(Optional) Base64 encoded image string"
    }
    ```

    **Response (JSON):**
    ```json
    {
      "answer": "Generated answer in Sinhala..."
    }
    ```

## ⚠️ Notes

- The system is configured to **only** answer questions related to maternal and child health.
- Responses are generated using `gemini-flash-latest`.
- This tool is for informational purposes and does not replace professional medical advice.

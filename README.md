# PDF Chat Assistant

A Streamlit application that allows you to upload PDF files, process them using LangChain and ChromaDB, and chat with them using OpenAI's GPT models. The app provides source citations showing which page each answer came from.

## Features

- 📄 **PDF Upload**: Upload and process PDF files
- 🔍 **Document Chunking**: Automatically splits PDFs into manageable chunks
- 💾 **Vector Storage**: Stores embeddings in ChromaDB for efficient retrieval
- 💬 **Chat Interface**: Interactive chat interface to ask questions about your PDFs
- 📑 **Source Citation**: Shows which page and section each answer came from
- 🧠 **Memory**: Maintains conversation context across multiple questions

## Requirements

- Python 3.11
- OpenAI API key

## Installation

1. Clone this repository or download the files

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:

Create a `.env` file in the project directory:
```
OPENAI_API_KEY=your_openai_api_key_here
```

Or set it as an environment variable:
```bash
# On Windows (PowerShell)
$env:OPENAI_API_KEY="your_openai_api_key_here"

# On Linux/Mac
export OPENAI_API_KEY="your_openai_api_key_here"
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the URL shown (typically `http://localhost:8501`)

3. Upload a PDF file using the sidebar

4. Click "Process PDF" to process the document

5. Start asking questions in the chat interface!

## How It Works

1. **PDF Processing**: When you upload a PDF, it's loaded and split into chunks using LangChain's `RecursiveCharacterTextSplitter`
2. **Embedding Generation**: Each chunk is embedded using OpenAI's embeddings model
3. **Vector Storage**: Embeddings are stored in ChromaDB for fast similarity search
4. **Question Answering**: When you ask a question:
   - The question is embedded and used to find the most relevant chunks
   - The relevant chunks are passed to GPT-3.5-turbo along with the question
   - The model generates an answer based on the retrieved context
   - Source information (page numbers and snippets) is extracted and displayed

## Project Structure

```
.
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── .env               # Environment variables (create this)
└── chroma_db/         # ChromaDB database (created automatically)
```

## Notes

- The app uses GPT-3.5-turbo for chat. You can modify the model in `app.py` if needed
- ChromaDB data is persisted in the `chroma_db/` directory
- Each PDF processing creates chunks that are stored and can be queried
- The chat maintains context within a session

## Troubleshooting

- **OpenAI API Key Error**: Make sure you've set the `OPENAI_API_KEY` in your `.env` file or environment variables
- **PDF Processing Error**: Ensure the PDF file is not corrupted or password-protected
- **Memory Issues**: For very large PDFs, you may need to adjust the chunk size in `app.py`

## Deploying to GitHub

See [DEPLOY.md](DEPLOY.md) for detailed instructions on how to deploy this project to GitHub.

Quick steps:
1. Install Git from https://git-scm.com/downloads
2. Initialize repository: `git init`
3. Add files: `git add .`
4. Commit: `git commit -m "Initial commit"`
5. Create repository on GitHub
6. Push: `git push -u origin main`

**Important**: Never commit your `.env` file with your API key! The `.gitignore` file is already configured to exclude it.

## License

MIT License

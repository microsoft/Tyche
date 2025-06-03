# Multi-Agent AI Chat Application

This project is a full-stack chat application using Azure OpenAI and Azure AI Search, built with Semantic Kernel. It features a FastAPI backend and a React frontend, designed for multi-agent extensibility.

## Features
- **Multi-agent ready** backend using Semantic Kernel
- **Azure OpenAI** for chat completions
- **Azure AI Search** for memory/context
- **FastAPI** backend (Python)
- **React** frontend (JavaScript)
- **Modern chat UI**
- **Secure configuration** via environment variables

---

## Folder Structure
```
root/
├── api/         # FastAPI backend (Python)
│   └── main.py
├── app/         # React frontend (JavaScript)
│   ├── package.json
│   └── src/
│       ├── App.jsx
│       ├── App.css
│       ├── index.js
│       └── setupProxy.js
├── requirements.txt
└── README.md
```

---

## Backend Setup (FastAPI)
1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
2. **Set environment variables:**
   - `AZURE_OPENAI_ENDPOINT`
   - `AZURE_OPENAI_KEY`
   - `AZURE_OPENAI_DEPLOYMENT`
   - `AZURE_SEARCH_ENDPOINT`
   - `AZURE_SEARCH_KEY`
   - `AZURE_SEARCH_INDEX`

   You can use a `.env` file or set them in your shell.

3. **Run the API server:**
   ```sh
   uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
   ```

---

## Frontend Setup (React)
1. **Install dependencies:**
   ```sh
   cd app
   npm install
   ```
2. **Start the React app:**
   ```sh
   npm start
   ```
   The app will run at [http://localhost:3000](http://localhost:3000) and proxy API requests to FastAPI.

---

## Usage
- Open [http://localhost:3000](http://localhost:3000) in your browser.
- Chat with the AI agent. The backend is ready for multi-agent extension.

---

## Security & Best Practices
- **Never hardcode secrets.** Use environment variables or Azure Key Vault.
- **Use managed identity** for production deployments.
- **Error handling and logging** are included in the backend.

---

## Extending to Multi-Agent
- Add more agents in `api/main.py` and route messages as needed.
- Use Semantic Kernel’s multi-agent orchestration features.

---

## References
- [Semantic Kernel](https://github.com/microsoft/semantic-kernel)
- [Azure OpenAI Service](https://learn.microsoft.com/azure/ai-services/openai/)
- [Azure Cognitive Search](https://learn.microsoft.com/azure/search/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)

---

## License
MIT

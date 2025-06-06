# Tyche - AI-Powered Customer Action Intelligence Platform

Tyche is an advanced multi-agent AI chat application designed for customer relationship management and next best action (NBA) recommendations. Built with Azure OpenAI and Semantic Kernel, it provides intelligent insights for credit management, order velocity optimization, and customer account analysis.

## 🎯 Purpose

Tyche helps business analysts and customer service teams by:
- **Analyzing customer accounts** and providing actionable recommendations
- **Improving order velocity** through intelligent hold management
- **Credit limit optimization** based on account history and risk assessment
- **Invoice aging analysis** for collections and credit teams
- **Account ownership tracking** for relationship management

## ✨ Features

### Core Capabilities
- **Multi-Agent Architecture** using Semantic Kernel with specialized agents
- **Azure OpenAI Integration** for advanced natural language processing
- **Azure AI Search** for knowledge base and context retrieval
- **Intelligent Message Formatting** with automatic content structure recognition
- **Modern Responsive UI** with professional chat interface
- **Plugin-Based Extensions** for modular functionality

### AI Agents & Plugins
- **ActionReview Agent**: Determines next best actions for customers
- **Threshold Plugin**: Analyzes account thresholds and limits
- **Account Owner Plugin**: Manages customer-employee relationships
- **Improve Order Velocity Plugin**: Optimizes order processing workflows
- **Credit Limit Plugin**: Handles credit assessments and adjustments
- **Invoice Aging Plugin**: Analyzes payment patterns and collections

### UI/UX Features
- **Smart Text Formatting**: Automatically formats bullet points, numbered lists, and headers
- **Agent Identification**: Clear display of which AI agent provided each response
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Professional Styling**: Modern chat bubbles with proper visual hierarchy
- **Real-time Updates**: Live chat interface with typing indicators

---

## 📁 Project Structure

```
Tyche/
├── 📁 api/                           # FastAPI Backend (Python)
│   ├── main.py                       # FastAPI application entry point
│   ├── sk_agent.py                   # Semantic Kernel agent orchestration
│   └── 📁 plugins/                   # AI Agent Plugins
│       ├── account_owner_plugin.py   # Customer-employee relationship management
│       ├── base_vector_search_plugin.py  # Base class for search functionality
│       ├── improve_order_velocity_plugin.py  # Order processing optimization
│       ├── increase_credit_limit_plugin.py   # Credit limit adjustments
│       ├── invoice_aging_plugin.py   # Payment analysis and collections
│       └── threshold_plugin.py       # Account threshold analysis
├── 📁 app/                           # React Frontend (JavaScript)
│   ├── package.json                  # Node.js dependencies and scripts
│   ├── public/
│   │   └── index.html                # HTML template
│   └── src/
│       ├── App.jsx                   # Main React component with chat UI
│       ├── App.css                   # Modern styling and responsive design
│       ├── index.js                  # React application entry point
│       ├── setupProxy.js             # Development proxy configuration
│       └── testData.js               # Sample data for testing
├── 📄 requirements.txt               # Python dependencies
├── 📄 sample.env                     # Environment variables template
├── 📄 test.http                      # API endpoint testing
├── 📄 SECURITY.md                    # Security guidelines and best practices
├── 📄 LICENSE                        # Project license
└── 📄 README.md                      # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ with pip
- Node.js 16+ with npm
- Azure OpenAI account with deployed models
- Azure AI Search service (optional, for enhanced context)

### 1. Backend Setup (FastAPI)

1. **Clone and navigate to the project:**
   ```bash
   git clone <repository-url>
   cd Tyche
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Copy `sample.env` to `.env` and update with your Azure credentials:
   ```env
   AZURE_OPENAI_ENDPOINT=https://your-openai-resource.openai.azure.com/
   AZURE_OPENAI_KEY=your-openai-key
   AZURE_OPENAI_DEPLOYMENT=your-deployment-name
   AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
   AZURE_SEARCH_KEY=your-search-key
   ```

5. **Start the API server:**
   ```bash
   uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
   ```
   The API will be available at http://localhost:8000

### 2. Frontend Setup (React)

1. **Navigate to the app directory:**
   ```bash
   cd app
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the React development server:**
   ```bash
   npm start
   ```
   The application will open at http://localhost:3000

### 3. Using the Application

1. Open your browser to http://localhost:3000
2. Start chatting with the AI agents
3. Ask questions like:
   - "What is the next best action for customer ABC123?"
   - "Who is the account owner for this customer?"
   - "How can we improve order velocity for account XYZ?"
   - "What are the current credit thresholds?"

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

---

## 🔧 Development

### API Endpoints

- `GET /health` - Health check endpoint
- `POST /chat` - Main chat endpoint
  ```json
  {
    "user": "string",
    "message": "string"
  }
  ```

### Adding New Plugins

1. Create a new plugin file in `api/plugins/`
2. Inherit from `BaseVectorSearchPlugin` (if search functionality needed)
3. Implement required methods with `@kernel_function` decorator
4. Register the plugin in `sk_agent.py`

Example plugin structure:
```python
from semantic_kernel import kernel_function
from .base_vector_search_plugin import BaseVectorSearchPlugin

class YourNewPlugin(BaseVectorSearchPlugin):
    @kernel_function(name="your_function", description="Function description")
    async def your_function(self, query: str) -> str:
        # Your implementation here
        return result
```

### Frontend Customization

The React frontend uses a smart formatting system that automatically recognizes:
- **Headers**: Lines ending with colons or in ALL CAPS
- **Bullet Points**: Lines starting with `-`
- **Numbered Lists**: Lines starting with `1.`, `2.`, etc.
- **Sub-items**: Lettered points (`a.`, `b.`) and roman numerals (`i.`, `ii.`)
- **Emphasis**: Quoted text and parenthetical content

### Testing

Test the API directly using the provided `test.http` file with your favorite HTTP client.

---

## 🏗️ Architecture

### Multi-Agent System
- **Semantic Kernel**: Orchestrates multiple AI agents
- **Concurrent Orchestration**: Handles parallel agent execution
- **Plugin-Based**: Modular design for easy extension

### Backend Stack
- **FastAPI**: High-performance async Python web framework
- **Semantic Kernel**: Microsoft's AI orchestration framework
- **Azure OpenAI**: GPT models for natural language processing
- **Azure AI Search**: Vector search and knowledge retrieval

### Frontend Stack
- **React 18**: Modern frontend library with hooks
- **Axios**: HTTP client for API communication
- **CSS3**: Custom styling with modern design principles
- **Responsive Design**: Mobile-first approach

---

## 🔒 Enhanced Security & Best Practices

### Environment Security
- **Never commit secrets** to version control
- **Use environment variables** for all sensitive configuration
- **Implement managed identity** for production Azure deployments
- **Regular key rotation** for Azure services

### Code Quality
- **Error handling** implemented throughout the application
- **Logging** configured for debugging and monitoring
- **Input validation** on all API endpoints
- **CORS configuration** for frontend-backend communication

### Production Considerations
- Use Azure Key Vault for secret management
- Implement authentication and authorization
- Set up monitoring and alerting
- Configure proper HTTPS certificates
- Implement rate limiting for API endpoints

---

### Local Development
Use the Quick Start guide above for local development setup.

---


## 📚 Enhanced References & Documentation

- [Semantic Kernel Documentation](https://github.com/microsoft/semantic-kernel)
- [Azure OpenAI Service](https://learn.microsoft.com/azure/ai-services/openai/)
- [Azure AI Search](https://learn.microsoft.com/azure/search/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Azure Developer CLI](https://learn.microsoft.com/azure/developer/azure-developer-cli/)

---


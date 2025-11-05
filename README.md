# Wardrobe AI

An intelligent digital wardrobe management system powered by multi-agent AI, featuring semantic search, conversational outfit suggestions, and virtual try-on capabilities.

## Overview

Wardrobe AI helps you:
- 📸 **Digitize your wardrobe** - Upload photos of your clothing items
- 🔍 **Search semantically** - Find items using natural language
- 💡 **Get AI suggestions** - Receive personalized outfit recommendations
- 👔 **Virtual try-on** - See how clothes look on you before wearing them
- 💬 **Chat with stylist** - Get fashion advice from an AI assistant

## Project Structure

```
ai-wardrobe/
├── backend/              # Flask API server
│   ├── app/             # Application code
│   │   ├── controllers/ # Route handlers
│   │   ├── models/      # Data models
│   │   ├── services/    # Business logic (LLM, ChromaDB, embeddings)
│   │   └── utils/       # Helper functions
│   ├── config/          # Configuration
│   └── run.py           # Entry point
├── frontend/            # React + Vite frontend
│   ├── src/
│   │   ├── components/  # Reusable UI components
│   │   ├── pages/       # Page components
│   │   └── services/    # API client
│   └── package.json
└── colab/              # Jupyter notebooks for ML (TODO)
```

## Tech Stack

### Backend
- **Framework**: Flask 3.0 (MVC architecture)
- **LLM**: OpenRouter API (Llama 3.1 70B)
- **Vector DB**: ChromaDB
- **Embeddings**: Sentence Transformers (CLIP)
- **Image Processing**: OpenCV, Pillow

### Frontend
- **Framework**: React 18 + Vite
- **Styling**: TailwindCSS
- **Routing**: React Router
- **HTTP Client**: Axios
- **Icons**: Lucide React

### ML/Vision (Coming Soon)
- OOTDiffusion (virtual try-on)
- Google Colab + ngrok

## Quick Start

### Backend Setup

1. **Navigate to backend**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENROUTER_API_KEY
   ```

5. **Run server**
   ```bash
   python run.py
   ```

   Server will start at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment** (optional)
   ```bash
   cp .env.example .env
   # Edit if backend URL is different
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```

   App will start at `http://localhost:3000`

### Getting API Keys

**OpenRouter** (for LLM):
1. Visit [openrouter.ai](https://openrouter.ai/)
2. Sign up and create an API key
3. Add to `.env`: `OPENROUTER_API_KEY=your_key_here`

## Features

### ✅ Backend (Complete)

- **Garment Management**
  - Upload clothing items with automatic metadata extraction
  - Auto-detect dominant colors
  - LLM-powered garment analysis
  - CRUD operations for garments

- **Semantic Search**
  - CLIP-based multimodal embeddings
  - Text and image search
  - RAG-powered search with ChromaDB
  - Similarity scoring

- **Outfit Suggestions**
  - AI-powered outfit combinations
  - Context-aware suggestions (weather, occasion)
  - Personalized recommendations
  - Outfit creation and management

- **Fashion Chat Assistant**
  - Conversational AI stylist
  - Fashion advice and tips
  - Context-aware responses
  - Conversation history

### ✅ Frontend (Complete)

- **Responsive UI**
  - Modern React interface with TailwindCSS
  - Mobile-friendly responsive design
  - Beautiful component library

- **All Core Pages**
  - Home dashboard with statistics
  - Upload interface with drag & drop
  - Wardrobe gallery with filters
  - AI outfit suggestions page
  - Interactive chat interface
  - Virtual try-on interface

- **User Experience**
  - Real-time search
  - Loading states
  - Error handling
  - Intuitive navigation

### 🚧 Coming Soon

- **Virtual Try-On**
  - OOTDiffusion Colab setup
  - Real-time garment visualization

- **Enhanced Features**
  - User authentication
  - Wardrobe analytics
  - Style profiles
  - Social sharing
  - Mobile app

## API Documentation

See [backend/API_EXAMPLES.md](backend/API_EXAMPLES.md) for detailed API usage examples.

### Quick Examples

**Upload a garment:**
```bash
curl -X POST http://localhost:5000/api/garments/ \
  -F "image=@shirt.jpg" \
  -F "name=Blue Shirt" \
  -F "category=top"
```

**Get outfit suggestions:**
```bash
curl -X POST http://localhost:5000/api/outfits/suggest \
  -H "Content-Type: application/json" \
  -d '{"query": "casual summer outfit", "user_id": "user123"}'
```

**Chat with assistant:**
```bash
curl -X POST http://localhost:5000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "What should I wear to a wedding?", "user_id": "user123"}'
```

## Architecture

### Multi-Agent System

```
User Query
    ↓
┌─────────────────┐
│  Flask Router   │
└────────┬────────┘
         ↓
    ┌────┴────┐
    │ LLM     │ → OpenRouter API
    │ Agent   │
    └────┬────┘
         ↓
    ┌────┴────┐
    │ RAG     │ → ChromaDB + CLIP
    │ Agent   │
    └────┬────┘
         ↓
    ┌────┴────┐
    │ Vision  │ → OOTDiffusion (Colab)
    │ Agent   │
    └─────────┘
```

### Data Flow

1. **Upload Phase**
   - User uploads garment image
   - Image processed (resize, color detection)
   - LLM analyzes and extracts metadata
   - CLIP generates multimodal embedding
   - Stored in ChromaDB

2. **Query Phase**
   - User asks for outfit suggestions
   - Query embedded using CLIP
   - Semantic search in ChromaDB
   - LLM combines results into recommendations

3. **Try-On Phase**
   - User selects garment + person photo
   - Sent to Colab API (OOTDiffusion)
   - Generated image returned
   - Stored and displayed

## Development

### Backend Structure

- **Models**: Data structures (Garment, Outfit, User)
- **Services**: Business logic (LLM, ChromaDB, embeddings)
- **Controllers**: API route handlers
- **Utils**: Helper functions (validation, image processing)

### Adding New Features

1. Create model in `app/models/`
2. Add service in `app/services/`
3. Create controller in `app/controllers/`
4. Register blueprint in `app/__init__.py`

### Testing

```bash
cd backend
pytest tests/
```

## Deployment

### Docker (Coming Soon)

```bash
docker-compose up
```

### Manual Deployment

1. Set `FLASK_ENV=production`
2. Use production WSGI server:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app('production')"
   ```

## Roadmap

- [x] Backend API with Flask
- [x] LLM integration (OpenRouter)
- [x] Vector database (ChromaDB)
- [x] Semantic search (CLIP)
- [x] Outfit suggestions
- [x] Chat assistant
- [x] Frontend React app
- [ ] Virtual try-on API (Colab)
- [ ] User authentication
- [ ] Mobile app
- [ ] Social features
- [ ] Wardrobe analytics

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests
4. Submit a pull request

## License

MIT License

## Support

- **Documentation**:
  - Backend: See `backend/README.md` and `backend/API_EXAMPLES.md`
  - Frontend: See `frontend/README.md`
  - Architecture: See `STRUCTURE.md`
- **Issues**: Open an issue on GitHub
- **Discussions**: Start a discussion for questions

---

**Built with ❤️ using React, Flask, and AI**

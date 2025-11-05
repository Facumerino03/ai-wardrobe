# Wardrobe AI - Project Structure

Complete file structure and organization of the Wardrobe AI project.

## Directory Tree

```
ai-wardrobe/
├── README.md                    # Main project documentation
├── STRUCTURE.md                 # This file
│
├── backend/                     # Flask Backend API
│   ├── README.md               # Backend documentation
│   ├── API_EXAMPLES.md         # Detailed API usage examples
│   ├── requirements.txt        # Python dependencies
│   ├── run.py                  # Main entry point
│   ├── test_basic.py           # Setup verification script
│   ├── setup.sh                # Unix setup script
│   ├── setup.bat               # Windows setup script
│   ├── .env.example            # Environment variables template
│   ├── .gitignore              # Git ignore rules
│   │
│   ├── config/                 # Configuration
│   │   ├── __init__.py
│   │   └── config.py           # Flask config classes
│   │
│   ├── app/                    # Application code
│   │   ├── __init__.py         # Flask app factory
│   │   │
│   │   ├── models/             # Data models
│   │   │   ├── __init__.py
│   │   │   ├── garment.py      # Garment model
│   │   │   ├── outfit.py       # Outfit model
│   │   │   └── user.py         # User model
│   │   │
│   │   ├── controllers/        # API route handlers
│   │   │   ├── __init__.py
│   │   │   ├── garment_controller.py   # Garment CRUD + search
│   │   │   ├── outfit_controller.py    # Outfit management + suggestions
│   │   │   ├── chat_controller.py      # Fashion chat assistant
│   │   │   └── tryon_controller.py     # Virtual try-on
│   │   │
│   │   ├── services/           # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── embeddings_service.py   # CLIP embeddings
│   │   │   ├── chroma_service.py       # ChromaDB operations
│   │   │   ├── llm_service.py          # OpenRouter LLM
│   │   │   └── tryon_service.py        # Virtual try-on API
│   │   │
│   │   ├── utils/              # Helper functions
│   │   │   ├── __init__.py
│   │   │   ├── validators.py           # Input validation
│   │   │   └── image_processing.py     # Image utilities
│   │   │
│   │   └── static/             # Static files
│   │       ├── uploads/        # Uploaded garment images
│   │       └── generated/      # Generated try-on images
│   │
│   ├── data/                   # Persistent data
│   │   └── chroma_db/          # ChromaDB storage
│   │
│   └── tests/                  # Unit tests
│
├── frontend/                   # React Frontend (TODO)
│   ├── package.json
│   ├── vite.config.js
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.jsx
│   └── public/
│
└── colab/                      # Jupyter Notebooks (TODO)
    ├── ootdiffusion_setup.ipynb
    └── virtual_tryon_api.ipynb
```

## Backend Architecture

### MVC Pattern

```
Request
   ↓
Controller (routes)
   ↓
Service (business logic)
   ↓
Model (data structure)
   ↓
Response
```

### Service Layer

The service layer handles all business logic:

- **EmbeddingsService**: Generates CLIP embeddings for text and images
- **ChromaService**: Manages vector database operations (CRUD, search)
- **LLMService**: Interacts with OpenRouter for AI responses
- **TryOnService**: Communicates with Colab API for virtual try-on

### Data Flow

#### Garment Upload Flow
```
User uploads image
    ↓
garment_controller.py
    ↓
├─→ image_processing.py (resize, color detection)
├─→ llm_service.py (metadata extraction)
├─→ embeddings_service.py (generate embedding)
└─→ chroma_service.py (store in DB)
    ↓
Return garment data
```

#### Outfit Suggestion Flow
```
User asks for outfit
    ↓
outfit_controller.py
    ↓
├─→ chroma_service.py (get user's wardrobe)
└─→ llm_service.py (generate suggestions)
    ↓
Return outfit combinations
```

#### Semantic Search Flow
```
User searches "blue formal shirt"
    ↓
garment_controller.py
    ↓
├─→ embeddings_service.py (embed query)
└─→ chroma_service.py (similarity search)
    ↓
Return matching garments
```

## File Responsibilities

### Models (`app/models/`)

| File | Purpose |
|------|---------|
| `garment.py` | Defines Garment dataclass, categories, styles, seasons |
| `outfit.py` | Defines Outfit dataclass, occasions |
| `user.py` | Defines User dataclass, preferences |

### Controllers (`app/controllers/`)

| File | Endpoints | Purpose |
|------|-----------|---------|
| `garment_controller.py` | `/api/garments/*` | Garment CRUD, upload, search |
| `outfit_controller.py` | `/api/outfits/*` | Outfit management, AI suggestions |
| `chat_controller.py` | `/api/chat/*` | Fashion assistant chat |
| `tryon_controller.py` | `/api/tryon/*` | Virtual try-on generation |

### Services (`app/services/`)

| File | Purpose |
|------|---------|
| `embeddings_service.py` | Generate CLIP embeddings for text/images |
| `chroma_service.py` | ChromaDB operations (add, search, update, delete) |
| `llm_service.py` | OpenRouter LLM interactions (analyze, suggest, chat) |
| `tryon_service.py` | Colab API communication for virtual try-on |

### Utils (`app/utils/`)

| File | Purpose |
|------|---------|
| `validators.py` | Input validation (files, data) |
| `image_processing.py` | Image utilities (resize, color detection, etc.) |

## Configuration

### Environment Variables

Defined in `.env`:

```env
# OpenRouter API
OPENROUTER_API_KEY=          # LLM API key
OPENROUTER_MODEL=            # Model to use

# Flask
FLASK_ENV=                   # development/production
FLASK_DEBUG=                 # True/False
SECRET_KEY=                  # Flask secret

# ChromaDB
CHROMA_PERSIST_DIRECTORY=    # Storage path

# Colab (Virtual Try-On)
COLAB_API_URL=               # Ngrok URL

# Uploads
MAX_CONTENT_LENGTH=          # Max file size
ALLOWED_EXTENSIONS=          # File types

# Embeddings
EMBEDDINGS_MODEL=            # Sentence Transformers model
```

### Configuration Classes

In `config/config.py`:

- `Config`: Base configuration
- `DevelopmentConfig`: Development settings
- `ProductionConfig`: Production settings
- `TestingConfig`: Testing settings

## Dependencies

### Core Libraries

- **flask**: Web framework
- **flask-cors**: CORS support
- **chromadb**: Vector database
- **sentence-transformers**: Embeddings
- **openai**: OpenRouter API client
- **opencv-python**: Image processing
- **pillow**: Image manipulation

### Full List

See `backend/requirements.txt` for complete dependencies.

## API Routes

### Garments
- `POST /api/garments/` - Create
- `GET /api/garments/` - List all
- `GET /api/garments/<id>` - Get one
- `PUT /api/garments/<id>` - Update
- `DELETE /api/garments/<id>` - Delete
- `POST /api/garments/search` - Search
- `GET /api/garments/images/<file>` - Serve image

### Outfits
- `POST /api/outfits/` - Create
- `GET /api/outfits/` - List all
- `GET /api/outfits/<id>` - Get one
- `PUT /api/outfits/<id>` - Update
- `DELETE /api/outfits/<id>` - Delete
- `POST /api/outfits/suggest` - AI suggestions
- `POST /api/outfits/<id>/rate` - Rate outfit

### Chat
- `POST /api/chat/message` - Send message
- `GET /api/chat/history/<session>` - Get history
- `DELETE /api/chat/clear/<session>` - Clear history

### Virtual Try-On
- `POST /api/tryon/generate` - Generate image
- `GET /api/tryon/health` - Check API status
- `GET /api/tryon/images/<file>` - Serve image

### System
- `GET /` - API info
- `GET /health` - Health check

## Database Schema

### ChromaDB Collections

**wardrobe_items** collection:
```
{
  "id": "uuid",
  "embedding": [float array],
  "metadata": {
    "name": str,
    "category": str,
    "color": str,
    "style": str,
    "season": str (comma-separated),
    "tags": str (comma-separated),
    "user_id": str,
    "image_path": str,
    "data": str (JSON)
  },
  "document": str (text description)
}
```

### In-Memory Storage

Outfits and chat conversations are currently stored in-memory dictionaries. In production, these should be moved to a persistent database (PostgreSQL, MongoDB, etc.).

## Testing

### Test Files

- `test_basic.py`: Setup verification
- `tests/`: Unit tests (to be added)

### Running Tests

```bash
# Verify setup
python test_basic.py

# Run unit tests
pytest tests/
```

## Development Workflow

1. **Setup**: Run `setup.sh` (Unix) or `setup.bat` (Windows)
2. **Configure**: Edit `.env` with API keys
3. **Develop**: Make changes in `app/`
4. **Test**: Run `test_basic.py` or `pytest`
5. **Run**: Execute `python run.py`

## Deployment

### Development
```bash
python run.py
```

### Production
```bash
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app('production')"
```

### Docker (Coming Soon)
```bash
docker-compose up
```

## Future Additions

- [ ] Frontend React application
- [ ] Colab notebooks for virtual try-on
- [ ] User authentication system
- [ ] PostgreSQL for persistent storage
- [ ] Redis for caching
- [ ] Celery for background tasks
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Monitoring and logging

---

For more details, see:
- [Backend README](backend/README.md)
- [API Examples](backend/API_EXAMPLES.md)
- [Main README](README.md)

# Wardrobe AI Backend

Backend API for the Wardrobe AI project - an intelligent digital wardrobe management system with multi-agent capabilities, semantic search, and virtual try-on.

## Features

- **Garment Management**: Upload, organize, and manage clothing items
- **Semantic Search**: RAG-powered search using ChromaDB and CLIP embeddings
- **AI Fashion Assistant**: Conversational agent for outfit suggestions and styling advice
- **Outfit Suggestions**: LLM-powered outfit combinations based on user preferences
- **Virtual Try-On**: Integration with OOTDiffusion (via Colab API)
- **Image Processing**: Automatic color detection, resizing, and optimization

## Tech Stack

- **Framework**: Flask 3.0 (MVC architecture)
- **LLM**: OpenRouter API (using Llama 3.1 70B)
- **Vector Database**: ChromaDB
- **Embeddings**: Sentence Transformers (CLIP-ViT-B-32)
- **Image Processing**: OpenCV, Pillow
- **Virtual Try-On**: OOTDiffusion (external Colab API)

## Project Structure

```
backend/
├── app/
│   ├── controllers/          # Route handlers
│   │   ├── garment_controller.py
│   │   ├── outfit_controller.py
│   │   ├── chat_controller.py
│   │   └── tryon_controller.py
│   ├── models/              # Data models
│   │   ├── garment.py
│   │   ├── outfit.py
│   │   └── user.py
│   ├── services/            # Business logic
│   │   ├── chroma_service.py
│   │   ├── embeddings_service.py
│   │   ├── llm_service.py
│   │   └── tryon_service.py
│   ├── utils/               # Helper functions
│   │   ├── validators.py
│   │   └── image_processing.py
│   └── static/              # Uploaded/generated files
│       ├── uploads/
│       └── generated/
├── config/                  # Configuration
│   └── config.py
├── tests/                   # Unit tests
├── requirements.txt         # Python dependencies
├── run.py                  # Main entry point
└── .env.example            # Environment variables template
```

## Installation

### Prerequisites

- Python 3.11+
- pip or conda
- Virtual environment (recommended)

### Setup Steps

1. **Clone the repository**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your credentials:
   ```env
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   OPENROUTER_MODEL=meta-llama/llama-3.1-70b-instruct
   COLAB_API_URL=your_ngrok_url_here  # Optional for virtual try-on
   ```

5. **Initialize directories**
   ```bash
   mkdir -p data/chroma_db
   mkdir -p app/static/uploads
   mkdir -p app/static/generated
   ```

## Running the Server

### Development Mode

```bash
python run.py
```

The server will start at `http://localhost:5000`

### Production Mode

```bash
export FLASK_ENV=production
export FLASK_DEBUG=False
python run.py
```

Or use a production WSGI server:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app('production')"
```

## API Endpoints

### Garments

- `POST /api/garments/` - Upload new garment
- `GET /api/garments/` - Get all garments
- `GET /api/garments/<id>` - Get specific garment
- `PUT /api/garments/<id>` - Update garment
- `DELETE /api/garments/<id>` - Delete garment
- `POST /api/garments/search` - Search garments (semantic)
- `GET /api/garments/images/<filename>` - Serve garment images

### Outfits

- `POST /api/outfits/` - Create outfit
- `GET /api/outfits/` - Get all outfits
- `GET /api/outfits/<id>` - Get specific outfit
- `PUT /api/outfits/<id>` - Update outfit
- `DELETE /api/outfits/<id>` - Delete outfit
- `POST /api/outfits/suggest` - Get AI outfit suggestions
- `POST /api/outfits/<id>/rate` - Rate outfit (1-5 stars)

### Chat

- `POST /api/chat/message` - Send message to fashion assistant
- `GET /api/chat/history/<session_id>` - Get conversation history
- `DELETE /api/chat/clear/<session_id>` - Clear conversation

### Virtual Try-On

- `POST /api/tryon/generate` - Generate virtual try-on image
- `GET /api/tryon/health` - Check Colab API health
- `GET /api/tryon/images/<filename>` - Serve generated images

## Usage Examples

### 1. Upload a Garment

```bash
curl -X POST http://localhost:5000/api/garments/ \
  -F "image=@shirt.jpg" \
  -F "name=Blue Denim Shirt" \
  -F "category=top" \
  -F "color=blue" \
  -F "style=casual" \
  -F "season=spring,fall" \
  -F "user_id=user123"
```

### 2. Search for Garments

```bash
curl -X POST http://localhost:5000/api/garments/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "casual blue shirt for spring",
    "user_id": "user123",
    "n_results": 5
  }'
```

### 3. Get Outfit Suggestions

```bash
curl -X POST http://localhost:5000/api/outfits/suggest \
  -H "Content-Type: application/json" \
  -d '{
    "query": "casual weekend outfit for spring",
    "user_id": "user123",
    "context": {
      "weather": "sunny",
      "temperature": 22
    }
  }'
```

### 4. Chat with Fashion Assistant

```bash
curl -X POST http://localhost:5000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What should I wear to a business casual meeting?",
    "user_id": "user123",
    "session_id": "session1"
  }'
```

### 5. Generate Virtual Try-On

```bash
curl -X POST http://localhost:5000/api/tryon/generate \
  -F "person_image=@person.jpg" \
  -F "garment_id=<garment_uuid>"
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` | OpenRouter API key | Required |
| `OPENROUTER_MODEL` | LLM model to use | `meta-llama/llama-3.1-70b-instruct` |
| `FLASK_ENV` | Environment (development/production) | `development` |
| `FLASK_DEBUG` | Enable debug mode | `True` |
| `CHROMA_PERSIST_DIRECTORY` | ChromaDB storage path | `./data/chroma_db` |
| `COLAB_API_URL` | Colab API URL for virtual try-on | Optional |
| `EMBEDDINGS_MODEL` | Sentence Transformer model | `sentence-transformers/clip-ViT-B-32` |

## Getting OpenRouter API Key

1. Go to [OpenRouter.ai](https://openrouter.ai/)
2. Sign up or log in
3. Navigate to API Keys section
4. Generate a new API key
5. Add credits to your account (optional, some models are free)

## Virtual Try-On Setup (Optional)

The virtual try-on feature requires a separate Colab API running OOTDiffusion. Instructions for setting up the Colab notebook will be provided separately.

## Development

### Adding New Endpoints

1. Create controller in `app/controllers/`
2. Register blueprint in `app/__init__.py`
3. Add tests in `tests/`

### Running Tests

```bash
pytest tests/
```

## Troubleshooting

### ChromaDB Connection Issues

- Ensure `data/chroma_db` directory exists
- Check file permissions
- Delete `data/chroma_db` and restart to reinitialize

### Model Loading Errors

- Verify Python version (3.11+)
- Check available disk space (models can be large)
- Ensure stable internet connection for first-time download

### API Rate Limits

- Monitor OpenRouter usage at their dashboard
- Consider implementing request caching
- Use lighter models for development

## Contributing

Contributions are welcome! Please follow:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review API endpoint examples

---

**Built with ❤️ for the Wardrobe AI project**

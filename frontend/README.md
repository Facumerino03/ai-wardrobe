# Wardrobe AI Frontend

Modern React frontend for Wardrobe AI - your intelligent digital wardrobe management system.

## Features

- 📸 **Upload Interface** - Intuitive garment upload with drag & drop
- 👔 **Wardrobe Gallery** - Beautiful grid view with semantic search
- 💡 **AI Outfit Suggestions** - Get personalized outfit recommendations
- 💬 **Chat Assistant** - Interactive fashion stylist chatbot
- 🖼️ **Virtual Try-On** - See how clothes look on you
- 📱 **Responsive Design** - Works on all devices

## Tech Stack

- **React 18** - Modern React with hooks
- **Vite** - Lightning-fast build tool
- **React Router** - Client-side routing
- **TailwindCSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls
- **Lucide React** - Beautiful icon library

## Prerequisites

- Node.js 16+ and npm/yarn
- Backend API running on http://localhost:5000

## Installation

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` if your backend runs on a different URL:
```env
VITE_API_URL=http://localhost:5000
```

### 3. Start Development Server

```bash
npm run dev
```

The app will open at http://localhost:3000

## Available Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint
```

## Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── Layout.jsx       # Main layout with navigation
│   │   ├── Loading.jsx      # Loading spinner
│   │   └── GarmentCard.jsx  # Garment display card
│   │
│   ├── pages/               # Page components
│   │   ├── Home.jsx         # Dashboard
│   │   ├── UploadGarment.jsx     # Upload interface
│   │   ├── Wardrobe.jsx          # Wardrobe gallery
│   │   ├── OutfitSuggestions.jsx # AI outfit suggestions
│   │   ├── Chat.jsx              # Fashion chat
│   │   └── VirtualTryOn.jsx      # Try-on interface
│   │
│   ├── services/            # API services
│   │   └── api.js           # Axios API client
│   │
│   ├── App.jsx              # Main app with routing
│   ├── main.jsx             # App entry point
│   └── index.css            # Global styles + Tailwind
│
├── public/                  # Static assets
├── index.html              # HTML template
├── package.json            # Dependencies
├── vite.config.js          # Vite configuration
├── tailwind.config.js      # Tailwind configuration
└── postcss.config.js       # PostCSS configuration
```

## Usage Guide

### 1. Upload Garments

1. Navigate to **Upload** page
2. Drag & drop or select an image
3. Fill in garment details (AI will auto-complete if left empty)
4. Click **Upload Garment**

The AI will automatically:
- Detect dominant colors
- Generate descriptions
- Suggest styles and occasions
- Create embeddings for search

### 2. Browse Wardrobe

1. Go to **Wardrobe** page
2. Use semantic search: "blue formal shirt for summer"
3. Filter by category
4. Click garments to view details

### 3. Get Outfit Suggestions

1. Navigate to **Outfits** page
2. Describe what you need: "casual brunch outfit"
3. Optional: Add context (weather, occasion)
4. Get AI-powered suggestions with styling tips

### 4. Chat with Fashion Assistant

1. Go to **Chat** page
2. Ask fashion questions or request advice
3. Get personalized styling recommendations
4. Conversation history is saved

### 5. Virtual Try-On (Requires Colab Setup)

1. Navigate to **Try-On** page
2. Upload a photo of yourself
3. Select a garment from your wardrobe
4. Generate virtual try-on image

## API Integration

The frontend connects to the Flask backend API. All API calls are in `src/services/api.js`:

```javascript
// Example: Upload garment
import { garmentAPI } from './services/api';

const formData = new FormData();
formData.append('image', file);
formData.append('name', 'Blue Shirt');
formData.append('category', 'top');

const result = await garmentAPI.upload(formData);
```

Available API modules:
- `garmentAPI` - Garment CRUD and search
- `outfitAPI` - Outfit management and suggestions
- `chatAPI` - Fashion chat assistant
- `tryonAPI` - Virtual try-on

## Customization

### Changing Colors

Edit `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        // Your custom color palette
      },
    },
  },
}
```

### Adding New Pages

1. Create component in `src/pages/`
2. Add route in `src/App.jsx`
3. Add navigation link in `src/components/Layout.jsx`

### Modifying API Base URL

Edit `src/services/api.js`:

```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';
```

## Building for Production

```bash
npm run build
```

This creates an optimized build in `dist/` folder.

### Deployment Options

**Static Hosting (Vercel, Netlify):**
```bash
npm run build
# Deploy dist/ folder
```

**With Docker:**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
RUN npm install -g serve
CMD ["serve", "-s", "dist", "-l", "3000"]
```

**Environment Variables for Production:**
```env
VITE_API_URL=https://your-backend-api.com
```

## Troubleshooting

### API Connection Errors

- Ensure backend is running on http://localhost:5000
- Check CORS settings in backend
- Verify `VITE_API_URL` in `.env`

### Images Not Loading

- Check backend static file serving
- Verify image paths in API responses
- Ensure backend `/api/garments/images/` endpoint works

### Build Errors

- Clear node_modules: `rm -rf node_modules && npm install`
- Clear Vite cache: `rm -rf node_modules/.vite`
- Update dependencies: `npm update`

## Development Tips

### Hot Reload

Vite provides instant hot module replacement (HMR). Changes appear immediately without full page reload.

### Component Development

Use React DevTools browser extension to inspect components and state.

### API Testing

Test API endpoints with the browser console:

```javascript
// In browser console
const api = await import('./src/services/api.js');
const garments = await api.garmentAPI.getAll();
console.log(garments);
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open pull request

## License

MIT License

## Support

- Check [main README](../README.md) for project overview
- See [backend README](../backend/README.md) for API documentation
- Open issues on GitHub

---

**Built with ❤️ using React + Vite + TailwindCSS**

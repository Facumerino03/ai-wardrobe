import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import UploadGarment from './pages/UploadGarment';
import Wardrobe from './pages/Wardrobe';
import OutfitSuggestions from './pages/OutfitSuggestions';
import Chat from './pages/Chat';
import VirtualTryOn from './pages/VirtualTryOn';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/upload" element={<UploadGarment />} />
          <Route path="/wardrobe" element={<Wardrobe />} />
          <Route path="/outfits" element={<OutfitSuggestions />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/tryon" element={<VirtualTryOn />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;

import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Upload, Shirt, Sparkles, MessageCircle, TrendingUp, Package } from 'lucide-react';
import { garmentAPI, outfitAPI } from '../services/api';
import Loading from '../components/Loading';

const Home = () => {
  const [stats, setStats] = useState({
    totalGarments: 0,
    totalOutfits: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const [garmentsData, outfitsData] = await Promise.all([
        garmentAPI.getAll(),
        outfitAPI.getAll(),
      ]);

      setStats({
        totalGarments: garmentsData.count || 0,
        totalOutfits: outfitsData.count || 0,
      });
    } catch (error) {
      console.error('Error loading stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const features = [
    {
      icon: Upload,
      title: 'Upload Garments',
      description: 'Add your clothing items with AI-powered analysis',
      link: '/upload',
      color: 'bg-blue-100 text-blue-600',
    },
    {
      icon: Shirt,
      title: 'Browse Wardrobe',
      description: 'Explore your digital closet with smart search',
      link: '/wardrobe',
      color: 'bg-purple-100 text-purple-600',
    },
    {
      icon: Sparkles,
      title: 'Get Outfit Ideas',
      description: 'AI-powered outfit suggestions for any occasion',
      link: '/outfits',
      color: 'bg-pink-100 text-pink-600',
    },
    {
      icon: MessageCircle,
      title: 'Fashion Assistant',
      description: 'Chat with your personal AI stylist',
      link: '/chat',
      color: 'bg-green-100 text-green-600',
    },
  ];

  if (loading) {
    return <Loading message="Loading your wardrobe..." />;
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Welcome to Wardrobe AI
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Your intelligent digital closet powered by AI. Organize, style, and discover new outfit combinations effortlessly.
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card text-center">
          <div className="flex justify-center mb-3">
            <Package className="w-12 h-12 text-primary-600" />
          </div>
          <h3 className="text-3xl font-bold text-gray-900">{stats.totalGarments}</h3>
          <p className="text-gray-600">Garments</p>
        </div>

        <div className="card text-center">
          <div className="flex justify-center mb-3">
            <Sparkles className="w-12 h-12 text-primary-600" />
          </div>
          <h3 className="text-3xl font-bold text-gray-900">{stats.totalOutfits}</h3>
          <p className="text-gray-600">Outfits Created</p>
        </div>

        <div className="card text-center">
          <div className="flex justify-center mb-3">
            <TrendingUp className="w-12 h-12 text-primary-600" />
          </div>
          <h3 className="text-3xl font-bold text-gray-900">AI Powered</h3>
          <p className="text-gray-600">Smart Suggestions</p>
        </div>
      </div>

      {/* Features */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-6">What would you like to do?</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => (
            <Link
              key={index}
              to={feature.link}
              className="card hover:shadow-lg transition-all group"
            >
              <div className={`w-12 h-12 ${feature.color} rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                <feature.icon className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600 text-sm">
                {feature.description}
              </p>
            </Link>
          ))}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card bg-gradient-to-r from-primary-500 to-primary-600 text-white">
        <div className="flex flex-col md:flex-row items-center justify-between">
          <div className="mb-4 md:mb-0">
            <h3 className="text-2xl font-bold mb-2">Ready to get started?</h3>
            <p className="opacity-90">
              Upload your first garment or chat with our AI fashion assistant!
            </p>
          </div>
          <div className="flex gap-3">
            <Link
              to="/upload"
              className="btn bg-white text-primary-600 hover:bg-gray-100"
            >
              Upload Garment
            </Link>
            <Link
              to="/chat"
              className="btn border-2 border-white text-white hover:bg-white hover:text-primary-600"
            >
              Chat Now
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;

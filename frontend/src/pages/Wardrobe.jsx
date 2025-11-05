import { useState, useEffect } from 'react';
import { Search, Filter, Plus } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { garmentAPI } from '../services/api';
import GarmentCard from '../components/GarmentCard';
import Loading from '../components/Loading';

const Wardrobe = () => {
  const navigate = useNavigate();
  const [garments, setGarments] = useState([]);
  const [filteredGarments, setFilteredGarments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterCategory, setFilterCategory] = useState('all');
  const [searching, setSearching] = useState(false);

  const categories = ['all', 'top', 'bottom', 'dress', 'outerwear', 'shoes', 'accessory', 'underwear', 'activewear'];

  useEffect(() => {
    loadGarments();
  }, []);

  useEffect(() => {
    filterGarments();
  }, [garments, filterCategory]);

  const loadGarments = async () => {
    try {
      const response = await garmentAPI.getAll();
      setGarments(response.garments || []);
      setFilteredGarments(response.garments || []);
    } catch (error) {
      console.error('Error loading garments:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterGarments = () => {
    if (filterCategory === 'all') {
      setFilteredGarments(garments);
    } else {
      setFilteredGarments(garments.filter(g => g.category === filterCategory));
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      filterGarments();
      return;
    }

    setSearching(true);
    try {
      const response = await garmentAPI.search(searchQuery);
      setFilteredGarments(response.results || []);
    } catch (error) {
      console.error('Error searching:', error);
    } finally {
      setSearching(false);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this garment?')) return;

    try {
      await garmentAPI.delete(id);
      setGarments(prev => prev.filter(g => g.id !== id));
    } catch (error) {
      console.error('Error deleting garment:', error);
      alert('Failed to delete garment');
    }
  };

  if (loading) {
    return <Loading message="Loading your wardrobe..." />;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">My Wardrobe</h1>
          <p className="text-gray-600 mt-1">{filteredGarments.length} items</p>
        </div>
        <button
          onClick={() => navigate('/upload')}
          className="btn btn-primary"
        >
          <Plus className="w-5 h-5 mr-2 inline" />
          Add Garment
        </button>
      </div>

      {/* Search and Filters */}
      <div className="card">
        <div className="flex flex-col md:flex-row gap-4">
          {/* Search */}
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search your wardrobe (e.g., 'blue formal shirt', 'summer dress')..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                className="input pl-10"
              />
            </div>
          </div>

          {/* Category Filter */}
          <div className="flex items-center gap-2">
            <Filter className="w-5 h-5 text-gray-400" />
            <select
              value={filterCategory}
              onChange={(e) => setFilterCategory(e.target.value)}
              className="input w-auto"
            >
              {categories.map(cat => (
                <option key={cat} value={cat}>
                  {cat === 'all' ? 'All Categories' : cat.charAt(0).toUpperCase() + cat.slice(1)}
                </option>
              ))}
            </select>
          </div>

          {/* Search Button */}
          <button
            onClick={handleSearch}
            disabled={searching}
            className="btn btn-primary"
          >
            {searching ? 'Searching...' : 'Search'}
          </button>
        </div>
      </div>

      {/* Garments Grid */}
      {filteredGarments.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <Search className="w-16 h-16 mx-auto" />
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            {garments.length === 0 ? 'No garments yet' : 'No matching items'}
          </h3>
          <p className="text-gray-600 mb-4">
            {garments.length === 0
              ? 'Start building your digital wardrobe by uploading your first garment'
              : 'Try adjusting your search or filters'}
          </p>
          {garments.length === 0 && (
            <button
              onClick={() => navigate('/upload')}
              className="btn btn-primary"
            >
              Upload Your First Garment
            </button>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredGarments.map(garment => (
            <GarmentCard
              key={garment.id}
              garment={garment}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default Wardrobe;

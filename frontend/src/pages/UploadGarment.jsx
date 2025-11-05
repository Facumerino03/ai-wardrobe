import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, CheckCircle, AlertCircle } from 'lucide-react';
import { garmentAPI } from '../services/api';

const UploadGarment = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    category: 'top',
    color: '',
    style: '',
    season: [],
    description: '',
    tags: '',
  });
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);

  const categories = ['top', 'bottom', 'dress', 'outerwear', 'shoes', 'accessory', 'underwear', 'activewear'];
  const styles = ['casual', 'formal', 'business', 'sporty', 'streetwear', 'bohemian', 'vintage', 'minimalist'];
  const seasons = ['spring', 'summer', 'fall', 'winter'];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSeasonChange = (season) => {
    setFormData(prev => ({
      ...prev,
      season: prev.season.includes(season)
        ? prev.season.filter(s => s !== season)
        : [...prev.season, season]
    }));
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      if (!image) {
        throw new Error('Please select an image');
      }

      const submitData = new FormData();
      submitData.append('image', image);
      submitData.append('name', formData.name);
      submitData.append('category', formData.category);
      submitData.append('color', formData.color);
      submitData.append('style', formData.style);
      submitData.append('season', formData.season.join(','));
      submitData.append('description', formData.description);
      submitData.append('tags', formData.tags);
      submitData.append('user_id', 'default_user');

      await garmentAPI.upload(submitData);

      setSuccess(true);
      setTimeout(() => {
        navigate('/wardrobe');
      }, 2000);

    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Failed to upload garment');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Upload New Garment</h1>

      {success && (
        <div className="mb-6 p-4 bg-green-100 border border-green-400 text-green-700 rounded-lg flex items-center">
          <CheckCircle className="w-5 h-5 mr-2" />
          Garment uploaded successfully! Redirecting to wardrobe...
        </div>
      )}

      {error && (
        <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg flex items-center">
          <AlertCircle className="w-5 h-5 mr-2" />
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Image Upload */}
          <div className="md:col-span-2">
            <label className="label">Garment Image *</label>
            <div className="mt-2 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-lg hover:border-primary-500 transition-colors">
              <div className="space-y-1 text-center">
                {preview ? (
                  <div className="mb-4">
                    <img src={preview} alt="Preview" className="mx-auto h-64 w-auto rounded-lg" />
                  </div>
                ) : (
                  <Upload className="mx-auto h-12 w-12 text-gray-400" />
                )}
                <div className="flex text-sm text-gray-600">
                  <label htmlFor="file-upload" className="relative cursor-pointer bg-white rounded-md font-medium text-primary-600 hover:text-primary-500">
                    <span>Upload a file</span>
                    <input
                      id="file-upload"
                      name="file-upload"
                      type="file"
                      className="sr-only"
                      accept="image/*"
                      onChange={handleImageChange}
                      required
                    />
                  </label>
                  <p className="pl-1">or drag and drop</p>
                </div>
                <p className="text-xs text-gray-500">PNG, JPG, WEBP up to 16MB</p>
              </div>
            </div>
          </div>

          {/* Name */}
          <div>
            <label htmlFor="name" className="label">Garment Name *</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              className="input"
              required
              placeholder="e.g., Blue Denim Shirt"
            />
          </div>

          {/* Category */}
          <div>
            <label htmlFor="category" className="label">Category *</label>
            <select
              id="category"
              name="category"
              value={formData.category}
              onChange={handleInputChange}
              className="input"
              required
            >
              {categories.map(cat => (
                <option key={cat} value={cat}>{cat.charAt(0).toUpperCase() + cat.slice(1)}</option>
              ))}
            </select>
          </div>

          {/* Color */}
          <div>
            <label htmlFor="color" className="label">Color</label>
            <input
              type="text"
              id="color"
              name="color"
              value={formData.color}
              onChange={handleInputChange}
              className="input"
              placeholder="e.g., Blue (AI will auto-detect if left empty)"
            />
          </div>

          {/* Style */}
          <div>
            <label htmlFor="style" className="label">Style</label>
            <select
              id="style"
              name="style"
              value={formData.style}
              onChange={handleInputChange}
              className="input"
            >
              <option value="">Select style...</option>
              {styles.map(style => (
                <option key={style} value={style}>{style.charAt(0).toUpperCase() + style.slice(1)}</option>
              ))}
            </select>
          </div>

          {/* Season */}
          <div className="md:col-span-2">
            <label className="label">Seasons</label>
            <div className="flex gap-3 mt-2">
              {seasons.map(season => (
                <label key={season} className="flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.season.includes(season)}
                    onChange={() => handleSeasonChange(season)}
                    className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">{season.charAt(0).toUpperCase() + season.slice(1)}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Description */}
          <div className="md:col-span-2">
            <label htmlFor="description" className="label">Description</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              rows={3}
              className="input"
              placeholder="Optional description (AI will generate if left empty)"
            />
          </div>

          {/* Tags */}
          <div className="md:col-span-2">
            <label htmlFor="tags" className="label">Tags</label>
            <input
              type="text"
              id="tags"
              name="tags"
              value={formData.tags}
              onChange={handleInputChange}
              className="input"
              placeholder="e.g., work, weekend, summer (comma-separated)"
            />
          </div>
        </div>

        {/* Submit Button */}
        <div className="flex gap-4">
          <button
            type="submit"
            disabled={loading}
            className="flex-1 btn btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Uploading...' : 'Upload Garment'}
          </button>
          <button
            type="button"
            onClick={() => navigate('/wardrobe')}
            className="btn btn-secondary"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default UploadGarment;

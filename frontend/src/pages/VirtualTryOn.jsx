import { useState, useEffect } from 'react';
import { Upload, Image as ImageIcon, AlertCircle, CheckCircle } from 'lucide-react';
import { tryonAPI, garmentAPI } from '../services/api';
import GarmentCard from '../components/GarmentCard';
import Loading from '../components/Loading';

const VirtualTryOn = () => {
  const [garments, setGarments] = useState([]);
  const [selectedGarment, setSelectedGarment] = useState(null);
  const [personImage, setPersonImage] = useState(null);
  const [personPreview, setPersonPreview] = useState(null);
  const [generatedImage, setGeneratedImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingGarments, setLoadingGarments] = useState(true);
  const [error, setError] = useState(null);
  const [apiAvailable, setApiAvailable] = useState(null);

  useEffect(() => {
    loadGarments();
    checkApiHealth();
  }, []);

  const loadGarments = async () => {
    try {
      const response = await garmentAPI.getAll();
      setGarments(response.garments || []);
    } catch (error) {
      console.error('Error loading garments:', error);
    } finally {
      setLoadingGarments(false);
    }
  };

  const checkApiHealth = async () => {
    try {
      const response = await tryonAPI.checkHealth();
      setApiAvailable(response.available);
    } catch (error) {
      setApiAvailable(false);
    }
  };

  const handlePersonImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setPersonImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPersonPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleGenerate = async () => {
    if (!personImage || !selectedGarment) {
      setError('Please select both a person image and a garment');
      return;
    }

    setLoading(true);
    setError(null);
    setGeneratedImage(null);

    try {
      const formData = new FormData();
      formData.append('person_image', personImage);
      formData.append('garment_id', selectedGarment.id);

      const response = await tryonAPI.generate(formData);

      if (response.success) {
        setGeneratedImage(response.image_url);
      } else {
        throw new Error(response.error || 'Failed to generate try-on image');
      }
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Failed to generate virtual try-on');
    } finally {
      setLoading(false);
    }
  };

  if (loadingGarments) {
    return <Loading message="Loading wardrobe..." />;
  }

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Virtual Try-On
        </h1>
        <p className="text-gray-600">
          See how garments look on you before wearing them
        </p>
      </div>

      {/* API Status Warning */}
      {apiAvailable === false && (
        <div className="card bg-yellow-50 border border-yellow-200">
          <div className="flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-yellow-600 mt-0.5" />
            <div>
              <h3 className="font-semibold text-yellow-900 mb-1">
                Virtual Try-On API Not Available
              </h3>
              <p className="text-yellow-800 text-sm">
                The Colab API for virtual try-on is not currently running. Please set up the OOTDiffusion notebook and configure the COLAB_API_URL in your backend .env file.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Upload Person Image */}
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-4">
            Step 1: Upload Your Photo
          </h2>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Your Photo
            </label>
            <div className="mt-2 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-lg hover:border-primary-500 transition-colors">
              <div className="space-y-1 text-center">
                {personPreview ? (
                  <div className="mb-4">
                    <img src={personPreview} alt="Preview" className="mx-auto h-64 w-auto rounded-lg" />
                  </div>
                ) : (
                  <Upload className="mx-auto h-12 w-12 text-gray-400" />
                )}
                <div className="flex text-sm text-gray-600">
                  <label htmlFor="person-upload" className="relative cursor-pointer bg-white rounded-md font-medium text-primary-600 hover:text-primary-500">
                    <span>Upload a photo</span>
                    <input
                      id="person-upload"
                      type="file"
                      className="sr-only"
                      accept="image/*"
                      onChange={handlePersonImageChange}
                    />
                  </label>
                  <p className="pl-1">or drag and drop</p>
                </div>
                <p className="text-xs text-gray-500">
                  Full body photo recommended for best results
                </p>
              </div>
            </div>
          </div>

          <h2 className="text-xl font-bold text-gray-900 mb-4 mt-6">
            Step 2: Select a Garment
          </h2>

          {garments.length === 0 ? (
            <div className="text-center py-8 text-gray-600">
              <ImageIcon className="w-12 h-12 mx-auto text-gray-300 mb-2" />
              <p>No garments in your wardrobe yet.</p>
              <p className="text-sm">Upload some items first!</p>
            </div>
          ) : (
            <div className="grid grid-cols-2 gap-3 max-h-96 overflow-y-auto">
              {garments.map(garment => (
                <div key={garment.id} onClick={() => setSelectedGarment(garment)}>
                  <GarmentCard
                    garment={garment}
                    isSelected={selectedGarment?.id === garment.id}
                    onSelect={() => {}}
                  />
                </div>
              ))}
            </div>
          )}

          {selectedGarment && (
            <div className="mt-4 p-3 bg-primary-50 border border-primary-200 rounded-lg">
              <p className="text-sm font-medium text-primary-900">
                Selected: {selectedGarment.name}
              </p>
            </div>
          )}

          <button
            onClick={handleGenerate}
            disabled={loading || !personImage || !selectedGarment || apiAvailable === false}
            className="w-full btn btn-primary mt-4 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Generating...' : 'Generate Try-On'}
          </button>
        </div>

        {/* Right: Result */}
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-4">
            Result
          </h2>

          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-2">
              <AlertCircle className="w-5 h-5 text-red-600 mt-0.5" />
              <p className="text-red-700 text-sm">{error}</p>
            </div>
          )}

          {loading ? (
            <div className="flex flex-col items-center justify-center py-12">
              <Loading message="Generating virtual try-on..." />
              <p className="text-sm text-gray-600 mt-4">
                This may take a minute...
              </p>
            </div>
          ) : generatedImage ? (
            <div>
              <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg flex items-center gap-2">
                <CheckCircle className="w-5 h-5 text-green-600" />
                <p className="text-green-700 text-sm">Try-on generated successfully!</p>
              </div>
              <img
                src={`http://localhost:5000${generatedImage}`}
                alt="Virtual Try-On Result"
                className="w-full rounded-lg shadow-lg"
              />
              <div className="mt-4 flex gap-2">
                <a
                  href={`http://localhost:5000${generatedImage}`}
                  download
                  className="flex-1 btn btn-primary"
                >
                  Download Image
                </a>
                <button
                  onClick={() => {
                    setGeneratedImage(null);
                    setPersonImage(null);
                    setPersonPreview(null);
                    setSelectedGarment(null);
                  }}
                  className="flex-1 btn btn-secondary"
                >
                  Try Another
                </button>
              </div>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-12 text-gray-400">
              <ImageIcon className="w-16 h-16 mb-4" />
              <p className="text-gray-600">
                Your generated try-on image will appear here
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Instructions */}
      <div className="card bg-blue-50 border border-blue-200">
        <h3 className="font-semibold text-blue-900 mb-2">Tips for Best Results:</h3>
        <ul className="list-disc list-inside space-y-1 text-blue-800 text-sm">
          <li>Use a clear, full-body photo with good lighting</li>
          <li>Stand in a neutral pose facing the camera</li>
          <li>Wear form-fitting clothes for more accurate results</li>
          <li>Plain background works best</li>
          <li>Make sure the Colab API is running (see backend README)</li>
        </ul>
      </div>
    </div>
  );
};

export default VirtualTryOn;

import { useState } from 'react';
import { Sparkles, Sun, Cloud, Snowflake, Briefcase, PartyPopper } from 'lucide-react';
import { outfitAPI, garmentAPI } from '../services/api';
import Loading from '../components/Loading';

const OutfitSuggestions = () => {
  const [query, setQuery] = useState('');
  const [context, setContext] = useState({
    weather: '',
    occasion: '',
    formality: '',
  });
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const quickPrompts = [
    { icon: Sun, text: 'Casual summer outfit', weather: 'sunny', occasion: 'casual' },
    { icon: Briefcase, text: 'Business meeting attire', occasion: 'business', formality: 'formal' },
    { icon: PartyPopper, text: 'Party outfit for tonight', occasion: 'party', formality: 'casual' },
    { icon: Snowflake, text: 'Cozy winter look', weather: 'cold', occasion: 'casual' },
  ];

  const handleQuickPrompt = (prompt) => {
    setQuery(prompt.text);
    setContext({
      weather: prompt.weather || '',
      occasion: prompt.occasion || '',
      formality: prompt.formality || '',
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setSuggestions([]);

    try {
      const response = await outfitAPI.suggest(query, 'default_user', context);

      if (!response.success) {
        throw new Error(response.error || 'Failed to get suggestions');
      }

      setSuggestions(response.suggestions || []);
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Failed to get outfit suggestions');
    } finally {
      setLoading(false);
    }
  };

  const getGarmentImageUrl = (path) => {
    if (!path) return 'https://via.placeholder.com/150';

    // Handle both Windows and Unix paths
    const normalizedPath = path.replace(/\\/g, '/');
    const filename = normalizedPath.split('/').pop();

    return `http://localhost:5000/api/garments/images/${filename}`;
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          AI Outfit Suggestions
        </h1>
        <p className="text-gray-600">
          Tell me what you need, and I'll create perfect outfit combinations from your wardrobe
        </p>
      </div>

      {/* Quick Prompts */}
      <div className="card">
        <h3 className="text-sm font-medium text-gray-700 mb-3">Quick suggestions:</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {quickPrompts.map((prompt, index) => (
            <button
              key={index}
              onClick={() => handleQuickPrompt(prompt)}
              className="p-3 border-2 border-gray-200 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-all text-left"
            >
              <prompt.icon className="w-5 h-5 text-primary-600 mb-1" />
              <p className="text-sm font-medium text-gray-900">{prompt.text}</p>
            </button>
          ))}
        </div>
      </div>

      {/* Search Form */}
      <div className="card">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="query" className="label">What do you need?</label>
            <textarea
              id="query"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="input"
              rows={3}
              placeholder="e.g., 'I need a professional outfit for a job interview' or 'Casual brunch outfit for spring'"
              required
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label htmlFor="weather" className="label">Weather (optional)</label>
              <select
                id="weather"
                value={context.weather}
                onChange={(e) => setContext({ ...context, weather: e.target.value })}
                className="input"
              >
                <option value="">Any weather</option>
                <option value="sunny">Sunny</option>
                <option value="rainy">Rainy</option>
                <option value="cold">Cold</option>
                <option value="hot">Hot</option>
              </select>
            </div>

            <div>
              <label htmlFor="occasion" className="label">Occasion (optional)</label>
              <select
                id="occasion"
                value={context.occasion}
                onChange={(e) => setContext({ ...context, occasion: e.target.value })}
                className="input"
              >
                <option value="">Any occasion</option>
                <option value="casual">Casual</option>
                <option value="work">Work</option>
                <option value="business">Business</option>
                <option value="party">Party</option>
                <option value="date">Date</option>
                <option value="wedding">Wedding</option>
              </select>
            </div>

            <div>
              <label htmlFor="formality" className="label">Formality (optional)</label>
              <select
                id="formality"
                value={context.formality}
                onChange={(e) => setContext({ ...context, formality: e.target.value })}
                className="input"
              >
                <option value="">Any formality</option>
                <option value="casual">Casual</option>
                <option value="smart casual">Smart Casual</option>
                <option value="formal">Formal</option>
              </select>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full btn btn-primary disabled:opacity-50"
          >
            <Sparkles className="w-5 h-5 mr-2 inline" />
            {loading ? 'Getting suggestions...' : 'Get AI Suggestions'}
          </button>
        </form>
      </div>

      {/* Error */}
      {error && (
        <div className="card bg-red-50 border border-red-200">
          <p className="text-red-700">{error}</p>
        </div>
      )}

      {/* Loading */}
      {loading && <Loading message="AI is analyzing your wardrobe..." />}

      {/* Suggestions */}
      {suggestions.length > 0 && (
        <div className="space-y-6">
          <h2 className="text-2xl font-bold text-gray-900">
            Here are your outfit suggestions:
          </h2>

          {suggestions.map((suggestion, index) => (
            <div key={index} className="card border-2 border-primary-200">
              <div className="flex items-start gap-4 mb-4">
                <div className="bg-primary-100 text-primary-700 rounded-full w-8 h-8 flex items-center justify-center font-bold flex-shrink-0">
                  {index + 1}
                </div>
                <div className="flex-1">
                  <h3 className="text-xl font-bold text-gray-900 mb-2">
                    {suggestion.name || `Outfit ${index + 1}`}
                  </h3>
                  <p className="text-gray-700 mb-4">{suggestion.description}</p>

                  {suggestion.styling_tips && suggestion.styling_tips.length > 0 && (
                    <div className="mb-4">
                      <h4 className="font-semibold text-gray-900 mb-2">Styling Tips:</h4>
                      <ul className="list-disc list-inside space-y-1">
                        {suggestion.styling_tips.map((tip, i) => (
                          <li key={i} className="text-gray-600">{tip}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {suggestion.garment_ids && suggestion.garment_ids.length > 0 && (
                    <div>
                      <h4 className="font-semibold text-gray-900 mb-2">Items to combine:</h4>
                      <p className="text-sm text-gray-600">Garment IDs: {suggestion.garment_ids.join(', ')}</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* No results */}
      {!loading && suggestions.length === 0 && query && !error && (
        <div className="text-center py-12">
          <Sparkles className="w-16 h-16 mx-auto text-gray-300 mb-4" />
          <p className="text-gray-600">
            Click "Get AI Suggestions" to see outfit ideas!
          </p>
        </div>
      )}
    </div>
  );
};

export default OutfitSuggestions;

import { Trash2, Edit } from 'lucide-react';

const GarmentCard = ({ garment, onDelete, onEdit, onSelect, isSelected }) => {
  const getImagePath = (path) => {
    if (!path) return '/placeholder.jpg';

    // Handle both Windows and Unix paths
    // Replace backslashes with forward slashes for consistency
    const normalizedPath = path.replace(/\\/g, '/');
    const filename = normalizedPath.split('/').pop();

    return `http://localhost:5000/api/garments/images/${filename}`;
  };

  return (
    <div
      className={`card hover:shadow-lg transition-shadow cursor-pointer ${
        isSelected ? 'ring-2 ring-primary-500' : ''
      }`}
      onClick={() => onSelect && onSelect(garment)}
    >
      <div className="aspect-square bg-gray-200 rounded-lg mb-4 overflow-hidden">
        <img
          src={getImagePath(garment.image_path)}
          alt={garment.name}
          className="w-full h-full object-cover"
          onError={(e) => {
            e.target.src = 'https://via.placeholder.com/400x400?text=No+Image';
          }}
        />
      </div>

      <h3 className="font-semibold text-lg mb-2">{garment.name}</h3>

      <div className="flex flex-wrap gap-2 mb-3">
        <span className="px-2 py-1 bg-primary-100 text-primary-700 rounded text-xs">
          {garment.category}
        </span>
        {garment.color && (
          <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs">
            {garment.color}
          </span>
        )}
        {garment.style && (
          <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs">
            {garment.style}
          </span>
        )}
      </div>

      {garment.season && garment.season.length > 0 && (
        <p className="text-sm text-gray-600 mb-3">
          Seasons: {garment.season.join(', ')}
        </p>
      )}

      {garment.description && (
        <p className="text-sm text-gray-600 mb-3 line-clamp-2">
          {garment.description}
        </p>
      )}

      {(onEdit || onDelete) && (
        <div className="flex gap-2 mt-4 pt-4 border-t">
          {onEdit && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                onEdit(garment);
              }}
              className="flex-1 btn btn-outline text-sm"
            >
              <Edit className="w-4 h-4 inline mr-1" />
              Edit
            </button>
          )}
          {onDelete && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                onDelete(garment.id);
              }}
              className="flex-1 btn bg-red-100 text-red-700 hover:bg-red-200 text-sm"
            >
              <Trash2 className="w-4 h-4 inline mr-1" />
              Delete
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default GarmentCard;

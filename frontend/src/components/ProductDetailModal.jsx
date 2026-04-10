function ProductDetailModal({ product, onClose }) {
  if (!product) return null

  return (
    <div className="modalBackdrop" onClick={onClose}>
      <div className="modalCard" onClick={(e) => e.stopPropagation()}>
        <div className="row modalHeader">
          <h2>{product.name}</h2>
          <button className="secondary" onClick={onClose}>Close</button>
        </div>
        <p>{product.description || 'No description available.'}</p>
        <p><strong>Price:</strong> Rs. {product.price}</p>
        <p><strong>Stock:</strong> {product.stock}</p>
        <p><strong>Category:</strong> {product.category_name || 'Uncategorized'}</p>
        <p><strong>Status:</strong> {product.is_active ? 'Active' : 'Inactive'}</p>
      </div>
    </div>
  )
}

export default ProductDetailModal

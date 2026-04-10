function ProductGrid({ products, qtyByProduct, onQtyChange, onAddToCart, onViewDetail }) {
  return (
    <div className="grid">
      {products.map((product) => (
        <article key={product.id} className="card">
          <h3>{product.name}</h3>
          <p>{product.description || 'No description'}</p>
          <p className="price">Rs. {product.price}</p>
          <p className="muted">Stock: {product.stock}</p>
          <div className="row">
            <input
              type="number"
              min="1"
              max="100"
              value={qtyByProduct[product.id] || 1}
              onChange={(e) => onQtyChange(product.id, e.target.value)}
            />
            <button onClick={() => onAddToCart(product.id)}>Add</button>
            <button className="secondary" onClick={() => onViewDetail(product.id)}>
              Details
            </button>
          </div>
        </article>
      ))}
    </div>
  )
}

export default ProductGrid

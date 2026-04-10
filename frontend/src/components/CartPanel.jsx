function CartPanel({ cart, shippingAddress, onShippingChange, onUpdateItem, onRemoveItem, onPlaceOrder, onClearCart }) {
  return (
    <section>
      <h2>Your Cart</h2>
      <div className="stack">
        {cart.items?.length ? (
          cart.items.map((item) => (
            <div key={item.id} className="listItem">
              <div>
                <strong>{item.product_name}</strong>
                <p className="muted">
                  Rs. {item.product_price} x {item.quantity} = Rs. {item.subtotal}
                </p>
              </div>
              <div className="row">
                <input
                  type="number"
                  min="1"
                  value={item.quantity}
                  onChange={(e) => onUpdateItem(item.id, e.target.value)}
                />
                <button className="danger" onClick={() => onRemoveItem(item.id)}>
                  Remove
                </button>
              </div>
            </div>
          ))
        ) : (
          <p className="muted">Your cart is empty.</p>
        )}
      </div>
      <div className="checkout">
        <p><strong>Total: Rs. {cart.total_price}</strong></p>
        <input value={shippingAddress} onChange={(e) => onShippingChange(e.target.value)} placeholder="Shipping address" />
        <div className="row">
          <button onClick={onPlaceOrder} disabled={!cart.items?.length}>Place Order</button>
          <button className="secondary" onClick={onClearCart}>Clear Cart</button>
        </div>
      </div>
    </section>
  )
}

export default CartPanel

function OrdersPanel({ orders, onCancel }) {
  return (
    <section>
      <h2>Order History</h2>
      <div className="stack">
        {orders.length ? (
          orders.map((order) => (
            <article className="listItem" key={order.id}>
              <div>
                <p>
                  <strong>Order #{order.id}</strong> - {order.status_display}
                </p>
                <p className="muted">Total: Rs. {order.total_price}</p>
                <p className="muted">Address: {order.shipping_address || 'Not provided'}</p>
              </div>
              {order.status === 'PENDING' ? (
                <button className="danger" onClick={() => onCancel(order.id)}>
                  Cancel
                </button>
              ) : null}
            </article>
          ))
        ) : (
          <p className="muted">No orders yet.</p>
        )}
      </div>
    </section>
  )
}

export default OrdersPanel

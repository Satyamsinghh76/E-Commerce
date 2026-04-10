function Tabs({ activeTab, onChange, cartCount }) {
  return (
    <nav className="tabs">
      <button className={activeTab === 'products' ? 'active' : ''} onClick={() => onChange('products')}>
        Products
      </button>
      <button className={activeTab === 'cart' ? 'active' : ''} onClick={() => onChange('cart')}>
        Cart ({cartCount})
      </button>
      <button className={activeTab === 'orders' ? 'active' : ''} onClick={() => onChange('orders')}>
        Orders
      </button>
    </nav>
  )
}

export default Tabs

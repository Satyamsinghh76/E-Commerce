import { useEffect, useMemo, useState } from 'react'
import './App.css'
import { login, logout } from './api/auth'
import {
  addToCart as addToCartApi,
  cancelOrder as cancelOrderApi,
  clearCart as clearCartApi,
  fetchCart,
  fetchOrders,
  fetchProductDetail,
  fetchProducts,
  placeOrder as placeOrderApi,
  removeCartItem as removeCartItemApi,
  updateCartItem as updateCartItemApi,
} from './api/shop'
import { getAccessToken } from './utils/storage'
import LoginPanel from './components/LoginPanel'
import Tabs from './components/Tabs'
import ProductGrid from './components/ProductGrid'
import ProductDetailModal from './components/ProductDetailModal'
import CartPanel from './components/CartPanel'
import OrdersPanel from './components/OrdersPanel'

function App() {
  const [activeTab, setActiveTab] = useState('products')
  const [username, setUsername] = useState('anshika')
  const [password, setPassword] = useState('test1234')
  const [token, setToken] = useState(getAccessToken())
  const [search, setSearch] = useState('')
  const [products, setProducts] = useState([])
  const [cart, setCart] = useState({ items: [], total_price: '0.00', total_items: 0 })
  const [orders, setOrders] = useState([])
  const [shippingAddress, setShippingAddress] = useState('Noida, UP')
  const [qtyByProduct, setQtyByProduct] = useState({})
  const [detailProduct, setDetailProduct] = useState(null)
  const [statusMessage, setStatusMessage] = useState('')
  const [errorMessage, setErrorMessage] = useState('')

  const isLoggedIn = useMemo(() => Boolean(token), [token])

  async function loadProducts(term = '') {
    setErrorMessage('')
    try {
      const data = await fetchProducts(term)
      setProducts(data.results || [])
    } catch (error) {
      setErrorMessage(error.message)
    }
  }

  async function loadCart() {
    if (!token) return
    try {
      const data = await fetchCart()
      setCart(data)
    } catch (error) {
      setErrorMessage(error.message)
    }
  }

  async function loadOrders() {
    if (!token) return
    try {
      const data = await fetchOrders()
      setOrders(data)
    } catch (error) {
      setErrorMessage(error.message)
    }
  }

  useEffect(() => {
    loadProducts()
  }, [])

  useEffect(() => {
    if (token) {
      loadCart()
      loadOrders()
    } else {
      setCart({ items: [], total_price: '0.00', total_items: 0 })
      setOrders([])
    }
  }, [token])

  async function handleLogin(event) {
    event.preventDefault()
    setErrorMessage('')
    setStatusMessage('')
    try {
      const data = await login(username, password)
      setToken(data.access)
      setStatusMessage('Login successful. You can now manage cart and orders.')
    } catch (error) {
      setErrorMessage(error.message)
    }
  }

  function handleLogout() {
    logout()
    setToken('')
    setStatusMessage('Logged out successfully.')
    setErrorMessage('')
  }

  async function addToCart(productId) {
    if (!token) {
      setErrorMessage('Please log in first to add items to cart.')
      return
    }
    const quantity = Number(qtyByProduct[productId] || 1)
    setErrorMessage('')
    try {
      const data = await addToCartApi(productId, quantity)
      setCart(data)
      setStatusMessage('Item added to cart.')
    } catch (error) {
      setErrorMessage(error.message)
    }
  }

  async function updateCartItem(itemId, quantity) {
    setErrorMessage('')
    try {
      const data = await updateCartItemApi(itemId, quantity)
      setCart(data)
    } catch (error) {
      setErrorMessage(error.message)
    }
  }

  async function removeCartItem(itemId) {
    setErrorMessage('')
    try {
      const data = await removeCartItemApi(itemId)
      setCart(data)
      setStatusMessage('Item removed from cart.')
    } catch (error) {
      setErrorMessage(error.message)
    }
  }

  async function clearCart() {
    setErrorMessage('')
    try {
      await clearCartApi()
      await loadCart()
      setStatusMessage('Cart cleared.')
    } catch (error) {
      setErrorMessage(error.message)
    }
  }

  async function placeOrder() {
    setErrorMessage('')
    try {
      await placeOrderApi(shippingAddress)
      await Promise.all([loadCart(), loadOrders()])
      setActiveTab('orders')
      setStatusMessage('Order placed successfully.')
    } catch (error) {
      setErrorMessage(error.message)
    }
  }

  async function cancelOrder(orderId) {
    setErrorMessage('')
    try {
      await cancelOrderApi(orderId)
      await loadOrders()
      setStatusMessage('Order cancelled and stock restored.')
    } catch (error) {
      setErrorMessage(error.message)
    }
  }

  async function openProductDetail(productId) {
    setErrorMessage('')
    try {
      const product = await fetchProductDetail(productId)
      setDetailProduct(product)
    } catch (error) {
      setErrorMessage(error.message)
    }
  }

  return (
    <div className="shell">
      <header className="hero">
        <div>
          <p className="eyebrow">Mini Ecommerce Dashboard</p>
          <h1>Django + DRF + React</h1>
          <p className="muted">Manage products, cart, and orders from one place.</p>
        </div>
        <LoginPanel
          username={username}
          password={password}
          onUsernameChange={setUsername}
          onPasswordChange={setPassword}
          onLogin={handleLogin}
          onLogout={handleLogout}
          isLoggedIn={isLoggedIn}
        />
      </header>

      <Tabs activeTab={activeTab} onChange={setActiveTab} cartCount={cart.total_items || 0} />

      {statusMessage && <p className="message ok">{statusMessage}</p>}
      {errorMessage && <p className="message error">{errorMessage}</p>}

      <main>
        {activeTab === 'products' && (
          <section>
            <div className="toolbar">
              <input
                placeholder="Search products..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
              <button onClick={() => loadProducts(search)}>Search</button>
            </div>
            <ProductGrid
              products={products}
              qtyByProduct={qtyByProduct}
              onQtyChange={(productId, value) =>
                setQtyByProduct((prev) => ({ ...prev, [productId]: value }))
              }
              onAddToCart={addToCart}
              onViewDetail={openProductDetail}
            />
          </section>
        )}

        {activeTab === 'cart' && (
          <CartPanel
            cart={cart}
            shippingAddress={shippingAddress}
            onShippingChange={setShippingAddress}
            onUpdateItem={updateCartItem}
            onRemoveItem={removeCartItem}
            onPlaceOrder={placeOrder}
            onClearCart={clearCart}
          />
        )}

        {activeTab === 'orders' && (
          <OrdersPanel orders={orders} onCancel={cancelOrder} />
        )}
      </main>

      <ProductDetailModal product={detailProduct} onClose={() => setDetailProduct(null)} />
    </div>
  )
}

export default App

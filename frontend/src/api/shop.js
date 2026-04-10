import { request } from './client'

export function fetchProducts(search = '') {
  const query = search.trim() ? `?search=${encodeURIComponent(search.trim())}` : ''
  return request(`/api/products/${query}`)
}

export function fetchProductDetail(productId) {
  return request(`/api/products/${productId}/`)
}

export function fetchCart() {
  return request('/api/cart/', { auth: true })
}

export function addToCart(productId, quantity) {
  return request('/api/cart/', {
    method: 'POST',
    auth: true,
    body: { product_id: productId, quantity: Number(quantity) },
  })
}

export function updateCartItem(itemId, quantity) {
  return request(`/api/cart/item/${itemId}/`, {
    method: 'PATCH',
    auth: true,
    body: { quantity: Number(quantity) },
  })
}

export function removeCartItem(itemId) {
  return request(`/api/cart/item/${itemId}/`, {
    method: 'DELETE',
    auth: true,
  })
}

export function clearCart() {
  return request('/api/cart/', {
    method: 'DELETE',
    auth: true,
  })
}

export function fetchOrders() {
  return request('/api/orders/', { auth: true })
}

export function placeOrder(shippingAddress) {
  return request('/api/orders/', {
    method: 'POST',
    auth: true,
    body: { shipping_address: shippingAddress },
  })
}

export function cancelOrder(orderId) {
  return request(`/api/orders/${orderId}/cancel/`, {
    method: 'POST',
    auth: true,
  })
}

export interface Product {
  id: string
  name: string
  price: number
  description: string
  image: string
  category: string
  rating: number
  reviews: number
  inStock: boolean
  specs?: string[]
}

export interface Category {
  id: string
  name: string
  description: string
  image: string
}

export interface Order {
  id: string
  userId: string
  items: OrderItem[]
  subtotal: number
  tax: number
  shipping: number
  total: number
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled'
  createdAt: Date
  shippingAddress: ShippingAddress
}

export interface OrderItem {
  productId: string
  name: string
  price: number
  quantity: number
}

export interface ShippingAddress {
  fullName: string
  email: string
  phone: string
  street: string
  city: string
  state: string
  zipCode: string
  country: string
}

export interface User {
  id: string
  email: string
  name: string
  isAdmin: boolean
}

export type SortOption = 'relevance' | 'price-asc' | 'price-desc' | 'newest'

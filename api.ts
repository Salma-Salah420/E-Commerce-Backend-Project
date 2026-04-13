import { PRODUCTS, CATEGORIES } from './constants'
import { Product, Category, Order, ShippingAddress, OrderItem, SortOption } from './types'

// Products
export function getProducts(filters?: {
  category?: string
  searchQuery?: string
  priceRange?: [number, number]
  sortBy?: SortOption
}): Product[] {
  let filtered = [...PRODUCTS]

  if (filters?.category && filters.category !== 'all') {
    filtered = filtered.filter((p) => p.category === filters.category)
  }

  if (filters?.searchQuery) {
    const query = filters.searchQuery.toLowerCase()
    filtered = filtered.filter(
      (p) =>
        p.name.toLowerCase().includes(query) ||
        p.description.toLowerCase().includes(query)
    )
  }

  if (filters?.priceRange) {
    const [min, max] = filters.priceRange
    filtered = filtered.filter((p) => p.price >= min && p.price <= max)
  }

  if (filters?.sortBy) {
    switch (filters.sortBy) {
      case 'price-asc':
        filtered.sort((a, b) => a.price - b.price)
        break
      case 'price-desc':
        filtered.sort((a, b) => b.price - a.price)
        break
      case 'newest':
        filtered.reverse()
        break
      case 'relevance':
      default:
        // Keep original order
        break
    }
  }

  return filtered
}

export function getProductById(id: string): Product | undefined {
  return PRODUCTS.find((p) => p.id === id)
}

export function createProduct(data: Omit<Product, 'id'>): Product {
  const newProduct: Product = {
    ...data,
    id: Math.random().toString(36).substr(2, 9),
  }
  PRODUCTS.push(newProduct)
  return newProduct
}

export function updateProduct(id: string, data: Partial<Product>): Product | undefined {
  const index = PRODUCTS.findIndex((p) => p.id === id)
  if (index === -1) return undefined

  PRODUCTS[index] = { ...PRODUCTS[index], ...data }
  return PRODUCTS[index]
}

export function deleteProduct(id: string): boolean {
  const index = PRODUCTS.findIndex((p) => p.id === id)
  if (index === -1) return false

  PRODUCTS.splice(index, 1)
  return true
}

// Categories
export function getCategories(): Category[] {
  return [...CATEGORIES]
}

export function getCategoryById(id: string): Category | undefined {
  return CATEGORIES.find((c) => c.id === id)
}

export function createCategory(data: Omit<Category, 'id'>): Category {
  const newCategory: Category = {
    ...data,
    id: Math.random().toString(36).substr(2, 9),
  }
  CATEGORIES.push(newCategory)
  return newCategory
}

export function updateCategory(id: string, data: Partial<Category>): Category | undefined {
  const index = CATEGORIES.findIndex((c) => c.id === id)
  if (index === -1) return undefined

  CATEGORIES[index] = { ...CATEGORIES[index], ...data }
  return CATEGORIES[index]
}

export function deleteCategory(id: string): boolean {
  const index = CATEGORIES.findIndex((c) => c.id === id)
  if (index === -1) return false

  CATEGORIES.splice(index, 1)
  return true
}

// Orders (using localStorage)
export function getOrders(userId?: string): Order[] {
  if (typeof window === 'undefined') return []

  const orders = localStorage.getItem('orders')
  if (!orders) return []

  try {
    const parsed = JSON.parse(orders) as Order[]
    return userId ? parsed.filter((o) => o.userId === userId) : parsed
  } catch {
    return []
  }
}

export function getOrderById(id: string): Order | undefined {
  const orders = getOrders()
  return orders.find((o) => o.id === id)
}

export function createOrder(
  userId: string,
  items: OrderItem[],
  shippingAddress: ShippingAddress
): Order {
  const subtotal = items.reduce((sum, item) => sum + item.price * item.quantity, 0)
  const tax = subtotal * 0.08
  const shipping = 10

  const newOrder: Order = {
    id: Math.random().toString(36).substr(2, 9),
    userId,
    items,
    subtotal,
    tax,
    shipping,
    total: subtotal + tax + shipping,
    status: 'pending',
    createdAt: new Date(),
    shippingAddress,
  }

  if (typeof window !== 'undefined') {
    const orders = getOrders()
    orders.push(newOrder)
    localStorage.setItem('orders', JSON.stringify(orders))
  }

  return newOrder
}

export function updateOrderStatus(
  id: string,
  status: Order['status']
): Order | undefined {
  if (typeof window === 'undefined') return undefined

  const orders = getOrders()
  const index = orders.findIndex((o) => o.id === id)
  if (index === -1) return undefined

  orders[index].status = status
  localStorage.setItem('orders', JSON.stringify(orders))
  return orders[index]
}

// Dashboard Statistics
export function getDashboardStats() {
  const orders = getOrders()
  const totalProducts = PRODUCTS.length
  const totalOrders = orders.length
  const totalRevenue = orders.reduce((sum, order) => sum + order.total, 0)
  const totalUsers = new Set(orders.map((o) => o.userId)).size

  return {
    totalProducts,
    totalOrders,
    totalRevenue,
    totalUsers,
  }
}

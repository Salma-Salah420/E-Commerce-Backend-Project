'use client'

import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useCart } from '@/components/contexts/cart-context'
import Link from 'next/link'

export function CartSummary() {
  const { cartTotal, items } = useCart()
  
  const subtotal = cartTotal
  const tax = subtotal * 0.08
  const shipping = items.length > 0 ? 10 : 0
  const total = subtotal + tax + shipping

  return (
    <Card className="p-6 h-fit sticky top-24">
      <h2 className="text-lg font-bold mb-6">Order Summary</h2>
      
      <div className="space-y-3 mb-6 pb-6 border-b border-border">
        <div className="flex justify-between text-sm">
          <span className="text-muted-foreground">Subtotal</span>
          <span>${subtotal.toFixed(2)}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-muted-foreground">Tax (8%)</span>
          <span>${tax.toFixed(2)}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-muted-foreground">Shipping</span>
          <span>{items.length > 0 ? `$${shipping.toFixed(2)}` : 'FREE'}</span>
        </div>
      </div>

      <div className="flex justify-between items-center mb-6">
        <span className="font-bold">Total</span>
        <span className="text-2xl font-bold text-primary">${total.toFixed(2)}</span>
      </div>

      <Link href="/checkout">
        <Button className="w-full mb-3" disabled={items.length === 0}>
          Proceed to Checkout
        </Button>
      </Link>
      
      <Link href="/products">
        <Button variant="outline" className="w-full">
          Continue Shopping
        </Button>
      </Link>
    </Card>
  )
}

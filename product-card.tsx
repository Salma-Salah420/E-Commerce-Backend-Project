'use client'

import Image from 'next/image'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { ShoppingCart, Heart } from 'lucide-react'
import { useCart } from '@/components/contexts/cart-context'
import { useState } from 'react'
import { toast } from 'sonner'
import { Product } from '@/lib/types'

interface ProductCardProps {
  product: Product
}

export function ProductCard({ product }: ProductCardProps) {
  const { addToCart } = useCart()
  const [isWishlisted, setIsWishlisted] = useState(false)

  const handleAddToCart = () => {
    addToCart({
      id: product.id,
      name: product.name,
      price: product.price,
      image: product.image,
      category: product.category,
    })
    toast.success('Added to cart')
  }

  const handleWishlist = () => {
    setIsWishlisted(!isWishlisted)
    toast.success(isWishlisted ? 'Removed from wishlist' : 'Added to wishlist')
  }

  return (
    <Card className="overflow-hidden hover:shadow-lg transition-shadow duration-300 flex flex-col h-full">
      <Link href={`/products/${product.id}`} className="relative h-48 overflow-hidden bg-muted">
        <Image
          src={product.image}
          alt={product.name}
          fill
          className="object-cover hover:scale-105 transition-transform duration-300"
          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
        />
        {!product.inStock && (
          <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
            <span className="text-white font-semibold">Out of Stock</span>
          </div>
        )}
      </Link>

      <div className="p-4 flex flex-col flex-1">
        <Link href={`/products/${product.id}`} className="hover:text-primary transition">
          <h3 className="font-semibold text-sm line-clamp-2">{product.name}</h3>
        </Link>

        <p className="text-xs text-muted-foreground mt-1">{product.category}</p>

        {/* Rating */}
        <div className="flex items-center gap-1 my-2">
          <div className="flex gap-0.5">
            {[...Array(5)].map((_, i) => (
              <div
                key={i}
                className={`text-xs ${i < Math.floor(product.rating) ? '★' : '☆'}`}
              >
                {i < Math.floor(product.rating) ? '★' : '☆'}
              </div>
            ))}
          </div>
          <span className="text-xs text-muted-foreground">({product.reviews})</span>
        </div>

        {/* Price */}
        <div className="mt-auto">
          <p className="text-lg font-bold text-primary">${product.price.toFixed(2)}</p>

          {/* Actions */}
          <div className="flex gap-2 mt-3">
            <Button
              onClick={handleAddToCart}
              disabled={!product.inStock}
              className="flex-1 text-xs"
              size="sm"
            >
              <ShoppingCart className="w-3 h-3 mr-1" />
              Add
            </Button>
            <Button
              onClick={handleWishlist}
              variant={isWishlisted ? 'default' : 'outline'}
              className="px-3 text-xs"
              size="sm"
            >
              <Heart
                className={`w-3 h-3 ${isWishlisted ? 'fill-current' : ''}`}
              />
            </Button>
          </div>
        </div>
      </div>
    </Card>
  )
}

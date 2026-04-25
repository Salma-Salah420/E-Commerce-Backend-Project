'use client'

import Link from 'next/link'
import { useRouter, usePathname } from 'next/navigation'
import { ShoppingCart, Search, User, LogOut, Menu, X } from 'lucide-react'
import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { useCart } from '@/components/contexts/cart-context'
import { useAuth } from '@/components/contexts/auth-context'
import { useFilters } from '@/components/contexts/filter-context'

export function Navbar() {
  const router = useRouter()
  const pathname = usePathname()
  const { cartCount } = useCart()
  const { user, logout, isAuthenticated } = useAuth()
  const { setSearchQuery } = useFilters()
  const [isOpen, setIsOpen] = useState(false)
  const [searchInput, setSearchInput] = useState('')

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    setSearchQuery(searchInput)
    router.push('/products')
    setIsOpen(false)
  }

  const handleLogout = () => {
    logout()
    router.push('/')
  }

  const isAdminPath = pathname?.startsWith('/dashboard') || pathname?.startsWith('/(admin)')

  return (
    <nav className="border-b border-border bg-card sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 font-bold text-xl">
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center text-primary-foreground">
              TS
            </div>
            <span className="hidden sm:inline">TrendStyle</span>
          </Link>

          {/* Desktop Search */}
          <form onSubmit={handleSearch} className="hidden md:flex flex-1 max-w-xs mx-8">
            <div className="flex w-full">
              <Input
                type="text"
                placeholder="Search products..."
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
                className="rounded-r-none"
              />
              <Button type="submit" variant="default" className="rounded-l-none">
                <Search className="w-4 h-4" />
              </Button>
            </div>
          </form>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-1">
            <Link href="/products">
              <Button variant="ghost" size="sm">
                Shop
              </Button>
            </Link>
            {isAdminPath && (
              <Link href="/(admin)/dashboard">
                <Button variant="ghost" size="sm">
                  Dashboard
                </Button>
              </Link>
            )}
          </div>

          {/* Right Actions */}
          <div className="flex items-center gap-2">
            {/* Cart Button */}
            <Link href="/cart">
              <Button variant="outline" size="sm" className="relative">
                <ShoppingCart className="w-4 h-4" />
                {cartCount > 0 && (
                  <span className="absolute -top-2 -right-2 bg-primary text-primary-foreground text-xs rounded-full w-5 h-5 flex items-center justify-center">
                    {cartCount}
                  </span>
                )}
              </Button>
            </Link>

            {/* User Menu */}
            {isAuthenticated && user ? (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline" size="sm">
                    <User className="w-4 h-4 mr-1" />
                    {user.name}
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  {user.isAdmin && (
                    <DropdownMenuItem asChild>
                      <Link href="/(admin)/dashboard">
                        Admin Dashboard
                      </Link>
                    </DropdownMenuItem>
                  )}
                  <DropdownMenuItem asChild>
                    <Link href="/account">My Account</Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem asChild>
                    <Link href="/orders">My Orders</Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={handleLogout}>
                    <LogOut className="w-4 h-4 mr-2" />
                    Logout
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            ) : (
              <Link href="/auth">
                <Button variant="default" size="sm">
                  Sign In
                </Button>
              </Link>
            )}

            {/* Mobile Menu Button */}
            <Button
              variant="ghost"
              size="sm"
              className="md:hidden"
              onClick={() => setIsOpen(!isOpen)}
            >
              {isOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </Button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isOpen && (
          <div className="md:hidden pb-4">
            <form onSubmit={handleSearch} className="mb-4">
              <div className="flex gap-2">
                <Input
                  type="text"
                  placeholder="Search products..."
                  value={searchInput}
                  onChange={(e) => setSearchInput(e.target.value)}
                  className="flex-1"
                />
                <Button type="submit" variant="default" size="sm">
                  <Search className="w-4 h-4" />
                </Button>
              </div>
            </form>
            <Link href="/products" className="block mb-2">
              <Button variant="ghost" className="w-full justify-start">
                Shop
              </Button>
            </Link>
          </div>
        )}
      </div>
    </nav>
  )
}

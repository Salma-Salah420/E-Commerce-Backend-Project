'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Button } from '@/components/ui/button'
import {
  LayoutDashboard,
  Package,
  FolderOpen,
  ShoppingCart,
} from 'lucide-react'

const menuItems = [
  {
    label: 'Dashboard',
    href: '/(admin)/dashboard',
    icon: LayoutDashboard,
  },
  {
    label: 'Products',
    href: '/(admin)/manage-products',
    icon: Package,
  },
  {
    label: 'Categories',
    href: '/(admin)/categories',
    icon: FolderOpen,
  },
  {
    label: 'Orders',
    href: '/(admin)/orders',
    icon: ShoppingCart,
  },
]

export function AdminSidebar() {
  const pathname = usePathname()

  return (
    <aside className="w-64 border-r border-border bg-card h-screen sticky top-0">
      <nav className="p-6 space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon
          const isActive = pathname?.includes(item.href.replace(/[()]/g, ''))
          
          return (
            <Link key={item.href} href={item.href}>
              <Button
                variant={isActive ? 'default' : 'ghost'}
                className="w-full justify-start gap-3"
              >
                <Icon className="w-4 h-4" />
                {item.label}
              </Button>
            </Link>
          )
        })}
      </nav>
    </aside>
  )
}

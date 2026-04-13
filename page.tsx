'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card } from '@/components/ui/card'
import { useAuth } from '@/components/contexts/auth-context'
import { toast } from 'sonner'
import { FieldGroup, FieldLabel } from '@/components/ui/field'

export default function AuthPage() {
  const router = useRouter()
  const { login, register } = useAuth()
  const [isLogin, setIsLogin] = useState(true)
  const [isLoading, setIsLoading] = useState(false)

  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
  })

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!formData.email || !formData.password) {
      toast.error('Please fill in all fields')
      return
    }

    if (!isLogin && !formData.name) {
      toast.error('Please enter your name')
      return
    }

    setIsLoading(true)
    try {
      if (isLogin) {
        await login(formData.email, formData.password)
        toast.success('Logged in successfully!')
      } else {
        await register(formData.email, formData.password, formData.name)
        toast.success('Account created successfully!')
      }
      router.push('/')
    } catch (error: any) {
      toast.error(error.message || 'Authentication failed')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-background px-4">
      <Card className="w-full max-w-md p-8">
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-2 font-bold text-2xl mb-4">
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center text-primary-foreground">
              TS
            </div>
            <span>TrendStyle</span>
          </div>
          <h1 className="text-2xl font-bold mb-2">
            {isLogin ? 'Welcome Back' : 'Create Account'}
          </h1>
          <p className="text-sm text-muted-foreground">
            {isLogin
              ? 'Sign in to your account to continue shopping'
              : 'Create a new account to get started'}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {!isLogin && (
            <FieldGroup>
              <FieldLabel htmlFor="name">Full Name</FieldLabel>
              <Input
                id="name"
                name="name"
                placeholder="John Doe"
                value={formData.name}
                onChange={handleInputChange}
                disabled={isLoading}
              />
            </FieldGroup>
          )}

          <FieldGroup>
            <FieldLabel htmlFor="email">Email Address</FieldLabel>
            <Input
              id="email"
              name="email"
              type="email"
              placeholder="you@example.com"
              value={formData.email}
              onChange={handleInputChange}
              disabled={isLoading}
            />
          </FieldGroup>

          <FieldGroup>
            <FieldLabel htmlFor="password">Password</FieldLabel>
            <Input
              id="password"
              name="password"
              type="password"
              placeholder="••••••••"
              value={formData.password}
              onChange={handleInputChange}
              disabled={isLoading}
            />
            {isLogin && (
              <p className="text-xs text-muted-foreground mt-1">
                Minimum 6 characters
              </p>
            )}
          </FieldGroup>

          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading
              ? 'Processing...'
              : isLogin
              ? 'Sign In'
              : 'Create Account'}
          </Button>
        </form>

        <div className="my-6 relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-border" />
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-2 bg-card text-muted-foreground">OR</span>
          </div>
        </div>

        <div className="space-y-3">
          {isLogin && (
            <>
              <Button variant="outline" className="w-full" disabled>
                Continue with Google
              </Button>
              <Button variant="outline" className="w-full" disabled>
                Continue with Apple
              </Button>
            </>
          )}
        </div>

        <div className="mt-6 text-center">
          <p className="text-sm text-muted-foreground">
            {isLogin ? "Don&apos;t have an account? " : 'Already have an account? '}
            <button
              onClick={() => {
                setIsLogin(!isLogin)
                setFormData({ email: '', password: '', name: '' })
              }}
              className="text-primary hover:underline font-semibold"
            >
              {isLogin ? 'Sign up' : 'Sign in'}
            </button>
          </p>
        </div>

        <p className="text-xs text-muted-foreground text-center mt-6">
          By continuing, you agree to our{' '}
          <Link href="#" className="hover:text-foreground">
            Terms of Service
          </Link>{' '}
          and{' '}
          <Link href="#" className="hover:text-foreground">
            Privacy Policy
          </Link>
        </p>

        {isLogin && (
          <div className="mt-6 p-4 bg-muted rounded-lg">
            <p className="text-xs text-muted-foreground mb-2">
              <strong>Demo credentials:</strong>
            </p>
            <p className="text-xs text-muted-foreground mb-1">
              Email: demo@example.com
            </p>
            <p className="text-xs text-muted-foreground mb-2">
              Password: demo123
            </p>
            <p className="text-xs text-muted-foreground">
              For admin: admin@example.com / admin123
            </p>
          </div>
        )}
      </Card>
    </div>
  )
}

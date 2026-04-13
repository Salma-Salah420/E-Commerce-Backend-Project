'use client'

import React, { createContext, useContext, useState } from 'react'

export interface FilterState {
  searchQuery: string
  selectedCategory: string
  priceRange: [number, number]
  sortBy: 'relevance' | 'price-asc' | 'price-desc' | 'newest'
}

interface FilterContextType extends FilterState {
  setSearchQuery: (query: string) => void
  setSelectedCategory: (category: string) => void
  setPriceRange: (range: [number, number]) => void
  setSortBy: (sort: FilterState['sortBy']) => void
  resetFilters: () => void
}

const FilterContext = createContext<FilterContextType | undefined>(undefined)

const defaultFilters: FilterState = {
  searchQuery: '',
  selectedCategory: 'all',
  priceRange: [0, 1000],
  sortBy: 'relevance',
}

export function FilterProvider({ children }: { children: React.ReactNode }) {
  const [filters, setFilters] = useState<FilterState>(defaultFilters)

  const setSearchQuery = (query: string) => {
    setFilters((prev) => ({ ...prev, searchQuery: query }))
  }

  const setSelectedCategory = (category: string) => {
    setFilters((prev) => ({ ...prev, selectedCategory: category }))
  }

  const setPriceRange = (range: [number, number]) => {
    setFilters((prev) => ({ ...prev, priceRange: range }))
  }

  const setSortBy = (sort: FilterState['sortBy']) => {
    setFilters((prev) => ({ ...prev, sortBy: sort }))
  }

  const resetFilters = () => {
    setFilters(defaultFilters)
  }

  return (
    <FilterContext.Provider
      value={{
        ...filters,
        setSearchQuery,
        setSelectedCategory,
        setPriceRange,
        setSortBy,
        resetFilters,
      }}
    >
      {children}
    </FilterContext.Provider>
  )
}

export function useFilters() {
  const context = useContext(FilterContext)
  if (context === undefined) {
    throw new Error('useFilters must be used within a FilterProvider')
  }
  return context
}

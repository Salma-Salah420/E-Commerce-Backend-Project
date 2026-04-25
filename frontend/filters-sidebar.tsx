'use client'

import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import { Label } from '@/components/ui/label'
import { Slider } from '@/components/ui/slider'
import { useFilters } from '@/components/contexts/filter-context'
import { CATEGORIES, PRICE_RANGES } from '@/lib/constants'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'
import { ChevronDown } from 'lucide-react'

export function FiltersSidebar() {
  const {
    selectedCategory,
    setSelectedCategory,
    priceRange,
    setPriceRange,
    resetFilters,
  } = useFilters()

  return (
    <div className="w-full md:w-64 space-y-6">
      {/* Reset Filters */}
      <Button
        onClick={resetFilters}
        variant="outline"
        className="w-full"
        size="sm"
      >
        Reset Filters
      </Button>

      {/* Categories */}
      <Collapsible defaultOpen>
        <CollapsibleTrigger asChild>
          <Button
            variant="ghost"
            className="w-full justify-between px-0 font-semibold"
          >
            Categories
            <ChevronDown className="w-4 h-4" />
          </Button>
        </CollapsibleTrigger>
        <CollapsibleContent className="space-y-3 mt-3">
          <div className="flex items-center space-x-2">
            <Checkbox
              id="all"
              checked={selectedCategory === 'all'}
              onCheckedChange={() => setSelectedCategory('all')}
            />
            <Label htmlFor="all" className="cursor-pointer text-sm">
              All Categories
            </Label>
          </div>
          {CATEGORIES.map((category) => (
            <div key={category.id} className="flex items-center space-x-2">
              <Checkbox
                id={category.id}
                checked={selectedCategory === category.name}
                onCheckedChange={() => setSelectedCategory(category.name)}
              />
              <Label htmlFor={category.id} className="cursor-pointer text-sm">
                {category.name}
              </Label>
            </div>
          ))}
        </CollapsibleContent>
      </Collapsible>

      {/* Price Range */}
      <Collapsible defaultOpen>
        <CollapsibleTrigger asChild>
          <Button
            variant="ghost"
            className="w-full justify-between px-0 font-semibold"
          >
            Price Range
            <ChevronDown className="w-4 h-4" />
          </Button>
        </CollapsibleTrigger>
        <CollapsibleContent className="space-y-4 mt-3">
          <Slider
            value={priceRange}
            onValueChange={setPriceRange}
            min={0}
            max={1000}
            step={10}
            className="w-full"
          />
          <div className="flex justify-between text-sm">
            <span>${priceRange[0]}</span>
            <span>${priceRange[1]}</span>
          </div>
          <div className="space-y-2">
            {PRICE_RANGES.map((range) => (
              <div key={range.label} className="flex items-center space-x-2">
                <Checkbox
                  id={range.label}
                  checked={
                    priceRange[0] === range.min && priceRange[1] === range.max
                  }
                  onCheckedChange={() => setPriceRange([range.min, range.max])}
                />
                <Label htmlFor={range.label} className="cursor-pointer text-sm">
                  {range.label}
                </Label>
              </div>
            ))}
          </div>
        </CollapsibleContent>
      </Collapsible>
    </div>
  )
}

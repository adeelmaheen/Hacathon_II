/**
 * Reusable Spinner loading component.
 * Provides visual loading feedback with ARIA attributes for screen readers.
 */

import React from 'react'

export interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg'
  label?: string
}

export function Spinner({ size = 'md', label = 'Loading...' }: SpinnerProps) {
  const sizeClasses = {
    sm: 'h-4 w-4 border-2',
    md: 'h-8 w-8 border-3',
    lg: 'h-12 w-12 border-4',
  }

  return (
    <div className="flex flex-col items-center justify-center gap-2" role="status">
      <div
        className={`${sizeClasses[size]} animate-spin rounded-full border-solid border-blue-600 border-r-transparent`}
        aria-hidden="true"
      />
      <span className="sr-only">{label}</span>
      {size === 'lg' && (
        <p className="text-sm text-gray-600" aria-live="polite">
          {label}
        </p>
      )}
    </div>
  )
}

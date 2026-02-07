import type { Metadata, Viewport } from 'next'
import './globals.css'
import { AuthProvider } from '@/hooks/useAuth'
import { ErrorBoundary } from '@/components/ErrorBoundary'
import { LiveRegionProvider } from '@/components/LiveRegion'

export const metadata: Metadata = {
  title: 'Todo App',
  description: 'Full-stack todo application with authentication',
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  userScalable: true,
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <ErrorBoundary>
          <LiveRegionProvider>
            <AuthProvider>
              {children}
            </AuthProvider>
          </LiveRegionProvider>
        </ErrorBoundary>
      </body>
    </html>
  )
}

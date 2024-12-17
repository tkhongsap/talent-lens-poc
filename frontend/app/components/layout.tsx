'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

export default function Layout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()

  const isActive = (path: string) => {
    if (path === '/') {
      return pathname === path
    }
    return pathname?.startsWith(path)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="flex items-center">
            <Link href="/" className="text-2xl font-bold text-indigo-600">TalentLens</Link>
          </div>
          <nav className="hidden md:flex items-center space-x-8">
            <Link 
              href="/#features" 
              className={`transition-colors ${
                isActive('/') ? 'text-gray-600' : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Features
            </Link>
            <Link 
              href="/#how-it-works" 
              className={`transition-colors ${
                isActive('/') ? 'text-gray-600' : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              How It Works
            </Link>
            <Link 
              href="/dashboard" 
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/dashboard')
                  ? 'bg-indigo-600 text-white hover:bg-indigo-700'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Dashboard
            </Link>
            <Link 
              href="/resume-analysis" 
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/resume-analysis')
                  ? 'bg-indigo-600 text-white hover:bg-indigo-700'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Resume Analysis
            </Link>
            <Link 
              href="/search-network" 
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/search-network')
                  ? 'bg-indigo-600 text-white hover:bg-indigo-700'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Search Network
            </Link>
          </nav>
        </div>
      </header>
      <main className="min-h-[calc(100vh-120px)]">{children}</main>
      <footer className="bg-gray-800 text-white py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <p>&copy; 2024 TalentLens. All rights reserved.</p>
          <div className="flex space-x-4">
            <Link href="/privacy" className="hover:text-indigo-400 transition-colors">Privacy Policy</Link>
            <Link href="/terms" className="hover:text-indigo-400 transition-colors">Terms of Service</Link>
          </div>
        </div>
      </footer>
    </div>
  )
}


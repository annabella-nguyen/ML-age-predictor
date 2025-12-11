'use client'

import { useState, useEffect } from 'react'

export default function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false)
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const scrollToSection = (id: string) => {
    const element = document.getElementById(id)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' })
      setIsMobileMenuOpen(false)
    }
  }

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled ? 'bg-bg-main shadow-md' : 'bg-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex-shrink-0">
            <button
              onClick={() => scrollToSection('hero')}
              className="text-xl font-bold text-text-main hover:text-primary transition-colors flex items-center gap-2"
            >
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              ML Age Predictor
            </button>
          </div>
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-8">
              <button
                onClick={() => scrollToSection('about')}
                className="text-text-main hover:text-primary transition-colors font-medium"
              >
                About
              </button>
              <button
                onClick={() => scrollToSection('data')}
                className="text-text-main hover:text-primary transition-colors font-medium"
              >
                Data
              </button>
              <button
                onClick={() => scrollToSection('methodology')}
                className="text-text-main hover:text-primary transition-colors font-medium"
              >
                Methodology
              </button>
              <button
                onClick={() => scrollToSection('results')}
                className="text-text-main hover:text-primary transition-colors font-medium"
              >
                Results
              </button>
            </div>
          </div>
          <div className="md:hidden">
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="text-text-main hover:text-primary transition-colors"
              aria-label="Toggle menu"
            >
              {isMobileMenuOpen ? (
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              ) : (
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              )}
            </button>
          </div>
        </div>
      </div>
      
      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden bg-bg-main border-t border-text-main/10">
          <div className="px-2 pt-2 pb-3 space-y-1">
            <button
              onClick={() => scrollToSection('about')}
              className="block w-full text-left px-3 py-2 text-text-main hover:text-primary hover:bg-secondary/30 rounded-md transition-colors font-medium"
            >
              About
            </button>
            <button
              onClick={() => scrollToSection('data')}
              className="block w-full text-left px-3 py-2 text-text-main hover:text-primary hover:bg-secondary/30 rounded-md transition-colors font-medium"
            >
              Data
            </button>
            <button
              onClick={() => scrollToSection('methodology')}
              className="block w-full text-left px-3 py-2 text-text-main hover:text-primary hover:bg-secondary/30 rounded-md transition-colors font-medium"
            >
              Methodology
            </button>
            <button
              onClick={() => scrollToSection('results')}
              className="block w-full text-left px-3 py-2 text-text-main hover:text-primary hover:bg-secondary/30 rounded-md transition-colors font-medium"
            >
              Results
            </button>
          </div>
        </div>
      )}
    </nav>
  )
}


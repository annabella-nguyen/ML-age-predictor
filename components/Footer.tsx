export default function Footer() {
  return (
    <footer className="bg-text-main text-white py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <p className="text-sm text-white/80">
              ML Age Predictor Project | Codebase @ UC Berkeley
            </p>
          </div>
          <div>
            <a
              href="https://codebase.berkeley.edu"
              target="_blank"
              rel="noopener noreferrer"
              className="text-white/80 hover:text-white transition-colors text-sm"
            >
              Codebase
            </a>
          </div>
        </div>
        <div className="mt-6 pt-6 border-t border-white/20 text-center">
          <p className="text-xs text-white/60">
            © {new Date().getFullYear()} Codebase @ Berkeley. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  )
}


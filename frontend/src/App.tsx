import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import ChatInterface from './components/ChatInterface';
import CalendarPage from './components/CalendarPage';
import ResourcesPage from './components/ResourcesPage';
import { MessageSquare, Calendar, BookOpen, CheckCircle } from 'lucide-react';

function Navigation() {
  const location = useLocation();
  const navItems = [
    { path: '/', label: 'Assistant', icon: <MessageSquare size={20} /> },
    { path: '/calendar', label: 'Calendar', icon: <Calendar size={20} /> },
    { path: '/resources', label: 'Resources', icon: <BookOpen size={20} /> },
  ];

  return (
    <nav className="flex lg:flex-col gap-2 p-2 bg-slate-800/60 backdrop-blur-md rounded-2xl border border-slate-700/50 sticky top-12">
      {navItems.map((item) => (
        <Link
          key={item.path}
          to={item.path}
          className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
            location.pathname === item.path
              ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/20'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-700/50'
          }`}
        >
          {item.icon}
          <span className="font-medium hidden sm:inline">{item.label}</span>
        </Link>
      ))}
    </nav>
  );
}

function App() {
  return (
    <Router>
      <main className="min-h-screen bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-slate-800 via-slate-900 to-black py-12 px-4 sm:px-6 lg:px-8 flex flex-col items-center">
        {/* Skip to Content for Accessibility */}
        <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 bg-blue-600 text-white p-2 rounded-md z-50">
          Skip to main content
        </a>

        <header className="text-center mb-10 w-full max-w-4xl">
          <h1 className="text-4xl md:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-400 mb-4 tracking-tight">
            Election Assistant
          </h1>
          <p className="text-lg text-slate-400 max-w-2xl mx-auto">
            Your 2026 portal for voting procedures, registration timelines, and intelligent assistance.
          </p>
        </header>

        <div className="w-full max-w-6xl grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Navigation Sidebar */}
          <aside className="lg:col-span-2">
            <Navigation />
          </aside>

          {/* Content Area */}
          <div id="main-content" className="lg:col-span-7">
            <Routes>
              <Route path="/" element={<ChatInterface />} />
              <Route path="/calendar" element={<CalendarPage />} />
              <Route path="/resources" element={<ResourcesPage />} />
            </Routes>
          </div>

          {/* Quick Checklist Sidebar */}
          <aside className="lg:col-span-3 space-y-6">
            <div className="bg-slate-800/40 backdrop-blur-sm p-6 rounded-2xl border border-slate-700/50">
              <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                <CheckCircle size={20} className="text-blue-400" />
                Next Steps
              </h2>
              <ul className="space-y-4">
                {[
                  "Check Eligibility",
                  "Gather Required ID",
                  "Complete Application",
                  "Submit to Local Office"
                ].map((step, i) => (
                  <li key={i} className="flex items-center gap-3 text-slate-300">
                    <div className="w-6 h-6 rounded-full border border-slate-600 flex items-center justify-center text-xs text-slate-500 font-bold shrink-0">
                      {i + 1}
                    </div>
                    <span className="text-sm font-medium">{step}</span>
                  </li>
                ))}
              </ul>
            </div>
          </aside>
        </div>
      </main>
    </Router>
  );
}

export default App;

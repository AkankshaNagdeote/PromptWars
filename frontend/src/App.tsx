import ChatInterface from './components/ChatInterface';

function App() {
  return (
    <main className="min-h-screen bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-slate-800 via-slate-900 to-black py-12 px-4 sm:px-6 lg:px-8 flex flex-col items-center">
      {/* Semantic HTML and Accessibility Header */}
      <header className="text-center mb-10 w-full max-w-4xl">
        <h1 className="text-4xl md:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-400 mb-4 tracking-tight">
          Election Process Guide
        </h1>
        <p className="text-lg text-slate-400 max-w-2xl mx-auto">
          Your intelligent assistant for navigating voting procedures, understanding timelines, and preparing for the upcoming elections.
        </p>
      </header>

      {/* Main Chat Component */}
      <ChatInterface />
    </main>
  );
}

export default App;

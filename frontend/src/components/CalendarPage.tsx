import React from 'react';

const CalendarPage = () => {
  const events = [
    { date: "March 15, 2026", event: "Primary Voter Registration Deadline" },
    { date: "May 12, 2026", event: "Spring Primary Elections" },
    { date: "October 05, 2026", event: "General Election Registration Deadline" },
    { date: "November 03, 2026", event: "General Election Day" },
  ];

  return (
    <div className="bg-slate-800/50 backdrop-blur-md rounded-2xl p-8 border border-slate-700 shadow-2xl">
      <h2 className="text-3xl font-bold text-white mb-6">2026 Election Calendar</h2>
      <div className="space-y-4">
        {events.map((item, i) => (
          <div key={i} className="flex items-center gap-6 p-4 rounded-xl bg-slate-700/30 border border-slate-600/50 hover:border-blue-500/50 transition-colors">
            <div className="w-32 text-blue-400 font-bold text-sm uppercase tracking-wider">
              {item.date}
            </div>
            <div className="text-slate-200 font-medium">
              {item.event}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CalendarPage;

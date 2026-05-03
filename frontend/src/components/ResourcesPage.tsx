import React from 'react';
import { ExternalLink, ShieldCheck, FileText, MapPin } from 'lucide-react';

const ResourcesPage = () => {
  const resources = [
    { title: "National Voter Registration", icon: <FileText className="text-blue-400" />, desc: "Official federal portal to register to vote online." },
    { title: "Find Your Polling Place", icon: <MapPin className="text-emerald-400" />, desc: "Locate your assigned voting location based on your address." },
    { title: "Voter ID Requirements", icon: <ShieldCheck className="text-amber-400" />, desc: "Check which forms of identification are accepted in your state." },
  ];

  return (
    <div className="bg-slate-800/50 backdrop-blur-md rounded-2xl p-8 border border-slate-700 shadow-2xl">
      <h2 className="text-3xl font-bold text-white mb-6">Voting Resources</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {resources.map((item, i) => (
          <div key={i} className="p-6 rounded-xl bg-slate-700/30 border border-slate-600/50 flex flex-col gap-3 group hover:bg-slate-700/50 transition-all cursor-pointer">
            <div className="flex items-center justify-between">
              {item.icon}
              <ExternalLink size={16} className="text-slate-500 group-hover:text-white transition-colors" />
            </div>
            <h3 className="text-lg font-bold text-white">{item.title}</h3>
            <p className="text-sm text-slate-400 leading-relaxed">{item.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ResourcesPage;

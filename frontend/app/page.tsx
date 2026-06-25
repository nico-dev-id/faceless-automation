"use client";

import VideoGenerator from "@/components/VideoGenerator";
import JobStatus from "@/components/JobStatus";
import { useState } from "react";

export default function Home() {
  const [jobId, setJobId] = useState<string | null>(null);

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Navigation */}
      <nav className="border-b border-slate-700 bg-slate-900/50 backdrop-blur">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold">FA</span>
            </div>
            <h1 className="text-xl font-bold text-white">Faceless Automation</h1>
          </div>
          <p className="text-slate-400 text-sm">YouTube Shorts Generator</p>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-6 py-16">
        <div className="text-center mb-16">
          <div className="inline-block mb-4 px-4 py-2 bg-purple-500/20 border border-purple-500/50 rounded-full">
            <span className="text-purple-300 text-sm font-medium">🚀 AI-Powered Content Generator</span>
          </div>
          <h2 className="text-5xl font-bold text-white mb-4">
            Generate YouTube Shorts
            <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent"> Otomatis</span>
          </h2>
          <p className="text-slate-400 text-lg max-w-2xl mx-auto">
            Biarkan AI mengambil topik trending, membuat script, recording, dan upload video YouTube Shorts 
            secara otomatis setiap hari.
          </p>
        </div>

        {/* Main Grid */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          {/* Stats */}
          <div className="md:col-span-1 space-y-4">
            <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-6">
              <div className="text-slate-400 text-sm mb-2">Status Sistem</div>
              <div className="flex items-center gap-2 mb-4">
                <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-white font-semibold">Online</span>
              </div>
              <div className="text-slate-500 text-xs space-y-1">
                <p>✓ Backend API aktif</p>
                <p>✓ Celery Worker running</p>
                <p>✓ Redis connected</p>
              </div>
            </div>

            <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-6">
              <div className="text-slate-400 text-sm mb-2">Fitur</div>
              <ul className="space-y-2 text-sm text-slate-300">
                <li>✨ AI Script Generator</li>
                <li>🎬 Auto Video Assembly</li>
                <li>🔥 Trending Topic Scraper</li>
                <li>⏰ Scheduled Generation</li>
              </ul>
            </div>
          </div>

          {/* Generator */}
          <div className="md:col-span-2">
            <VideoGenerator onJobCreated={setJobId} />
          </div>
        </div>

        {/* Job Status */}
        {jobId && (
          <div className="mb-8">
            <JobStatus jobId={jobId} />
          </div>
        )}
      </div>
    </main>
  );
}
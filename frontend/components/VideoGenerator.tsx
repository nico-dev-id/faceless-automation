"use client";

import { useState } from "react";

interface GenerateResponse {
  status: string;
  job_id: string;
  topic: string;
  message: string;
}

interface VideoGeneratorProps {
  onJobCreated: (jobId: string) => void;
}

export default function VideoGenerator({ onJobCreated }: VideoGeneratorProps) {
  const [niche, setNiche] = useState("teknologi");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const niches = [
    { value: "teknologi", label: "💻 Teknologi", color: "from-blue-500 to-cyan-500" },
    { value: "bisnis", label: "💼 Bisnis", color: "from-green-500 to-emerald-500" },
    { value: "kesehatan", label: "❤️ Kesehatan", color: "from-red-500 to-pink-500" },
    { value: "hiburan", label: "🎬 Hiburan", color: "from-purple-500 to-pink-500" },
    { value: "pendidikan", label: "📚 Pendidikan", color: "from-yellow-500 to-orange-500" },
  ];

  const handleGenerate = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `http://localhost:8000/api/generate-from-trending/${niche}`,
        { method: "POST" }
      );

      if (!response.ok) throw new Error("Failed to generate video");

      const data: GenerateResponse = await response.json();
      onJobCreated(data.job_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 rounded-xl p-8 shadow-2xl">
      <h3 className="text-2xl font-bold text-white mb-2">Generate Video</h3>
      <p className="text-slate-400 text-sm mb-6">Pilih niche dan biarkan AI membuat video untuk Anda</p>

      <div className="mb-6">
        <label className="block text-sm font-medium text-slate-300 mb-3">Pilih Niche:</label>
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
          {niches.map((n) => (
            <button
              key={n.value}
              onClick={() => setNiche(n.value)}
              className={`p-3 rounded-lg text-sm font-medium transition-all ${
                niche === n.value
                  ? `bg-gradient-to-r ${n.color} text-white shadow-lg scale-105`
                  : "bg-slate-700 text-slate-300 hover:bg-slate-600"
              }`}
            >
              {n.label}
            </button>
          ))}
        </div>
      </div>

      <button
        onClick={handleGenerate}
        disabled={loading}
        className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 disabled:from-gray-600 disabled:to-gray-700 text-white font-bold py-3 rounded-lg transition-all duration-200 transform hover:scale-[1.02] disabled:scale-100 shadow-lg"
      >
        {loading ? (
          <span className="flex items-center justify-center gap-2">
            <span className="animate-spin">⚙️</span>
            Generating...
          </span>
        ) : (
          "🚀 Generate Video"
        )}
      </button>

      {error && (
        <div className="mt-4 p-4 bg-red-500/20 border border-red-500/50 text-red-300 rounded-lg text-sm">
          ⚠️ {error}
        </div>
      )}
    </div>
  );
}
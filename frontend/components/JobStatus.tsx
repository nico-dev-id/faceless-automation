"use client";

import { useEffect, useState } from "react";

interface JobStatusResponse {
  status: string;
  step?: string;
  title?: string;
  hashtags?: string[];
  video_url?: string;
  error?: string;
}

interface JobStatusProps {
  jobId: string;
}

export default function JobStatus({ jobId }: JobStatusProps) {
  const [status, setStatus] = useState<JobStatusResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/api/job-status/${jobId}`
        );
        if (!response.ok) throw new Error("Failed to fetch status");
        const data: JobStatusResponse = await response.json();
        setStatus(data);

        if (data.status === "success" || data.status === "failed") {
          setLoading(false);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error");
        setLoading(false);
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 2000);
    return () => clearInterval(interval);
  }, [jobId]);

  if (!status) return null;

  const statusConfig = {
    pending: {
      bg: "bg-yellow-500/20",
      border: "border-yellow-500/50",
      text: "text-yellow-300",
      icon: "⏳",
    },
    processing: {
      bg: "bg-blue-500/20",
      border: "border-blue-500/50",
      text: "text-blue-300",
      icon: "🔄",
    },
    success: {
      bg: "bg-green-500/20",
      border: "border-green-500/50",
      text: "text-green-300",
      icon: "✅",
    },
    failed: {
      bg: "bg-red-500/20",
      border: "border-red-500/50",
      text: "text-red-300",
      icon: "❌",
    },
  };

  const config =
    statusConfig[status.status as keyof typeof statusConfig] ||
    statusConfig.pending;

  return (
    <div
      className={`${config.bg} border ${config.border} rounded-xl p-8 backdrop-blur`}
    >
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <span className="text-3xl">{config.icon}</span>
          <div>
            <p className={`text-sm ${config.text}`}>Status Proses</p>
            <h3 className="text-2xl font-bold text-white capitalize">
              {status.status}
            </h3>
          </div>
        </div>
        {loading && (
          <div className="flex gap-1">
            <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
            <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce delay-100"></div>
            <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce delay-200"></div>
          </div>
        )}
      </div>

      {status.step && (
        <div className="mb-4 p-3 bg-slate-800/50 rounded-lg">
          <p className="text-slate-300 text-sm">{status.step}</p>
        </div>
      )}

      {status.status === "success" && (
        <div className="space-y-4">
          <div className="bg-slate-800/50 rounded-lg p-4">
            <p className="text-slate-400 text-xs mb-1">JUDUL VIDEO</p>
            <p className="text-white font-semibold">{status.title}</p>
          </div>

          <div className="bg-slate-800/50 rounded-lg p-4">
            <p className="text-slate-400 text-xs mb-3">HASHTAGS</p>
            <div className="flex flex-wrap gap-2">
              {status.hashtags?.map((tag) => (
                <span
                  key={tag}
                  className="bg-purple-500/30 text-purple-300 px-3 py-1 rounded-full text-xs border border-purple-500/50"
                >
                  #{tag}
                </span>
              ))}
            </div>
          </div>

          <a
            href={`http://localhost:8000${status.video_url}`}
            download
            className="w-full inline-block text-center bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white font-bold py-3 rounded-lg transition-all transform hover:scale-[1.02] shadow-lg"
          >
            ⬇️ Download Video
          </a>
        </div>
      )}

      {status.status === "failed" && (
        <p className="text-red-300 text-sm">
          {status.error || "Unknown error occurred"}
        </p>
      )}

      {error && <p className="text-red-300 text-sm">{error}</p>}
    </div>
  );
}
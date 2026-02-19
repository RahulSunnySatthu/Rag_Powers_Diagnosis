import { useState } from "react";
import { askQuestion, resetDocuments } from "../api";

export default function Chat() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [confidence, setConfidence] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!query) return;

    setLoading(true);

    try {
      const res = await askQuestion(query);
      setResponse(res.data.response);
      setConfidence(res.data.confidence_score);
    } catch {
      setResponse("Something went wrong.");
    }

    setLoading(false);
  };

  const handleReset = async () => {
    await resetDocuments();
    setResponse("");
    setConfidence(null);
  };

  return (
    <div className="bg-white shadow-2xl rounded-3xl p-10">
      <h3 className="text-3xl font-bold mb-6 text-slate-800">
        Ask About Your Report
      </h3>

      <div className="flex gap-4 mb-6">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Is my Ferritin level normal?"
          className="flex-1 border border-gray-300 rounded-xl px-5 py-3 focus:ring-2 focus:ring-blue-500 focus:outline-none"
        />

        <button
          onClick={handleAsk}
          className="bg-green-600 hover:bg-green-700 text-white px-8 py-3 rounded-xl font-semibold transition"
        >
          Ask
        </button>

        <button
          onClick={handleReset}
          className="bg-red-500 hover:bg-red-600 text-white px-6 py-3 rounded-xl transition"
        >
          Reset
        </button>
      </div>

      {loading && (
        <div className="text-gray-500 animate-pulse">
          Analyzing your medical report...
        </div>
      )}

      {response && (
        <div className="mt-8 bg-slate-50 border border-gray-200 p-8 rounded-2xl">
          <h4 className="text-xl font-semibold mb-4 text-slate-700">
            AI Response
          </h4>

          <p className="whitespace-pre-wrap text-gray-700 leading-relaxed">
            {response}
          </p>

          {confidence !== null && (
            <div className="mt-6 text-sm text-gray-500">
              Confidence Score:{" "}
              <span className="font-semibold">
                {(confidence * 100).toFixed(1)}%
              </span>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

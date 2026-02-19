import React, { useState } from "react";
import {
  FileText,
  Image as ImageIcon,
  Upload,
  X,
  ShieldCheck,
  Search,
  ArrowRight,
  History,
  FileUp,
  Database,
  Zap
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { uploadPDF, uploadImage, askQuestion } from "./api";

const App = () => {
  const [files, setFiles] = useState([]);
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);

  // ================= Upload Handler =================
  const handleUpload = async (type) => {
    const input = document.createElement("input");
    input.type = "file";

    input.onchange = async (e) => {
      const file = e.target.files[0];
      if (!file) return;

      setIsProcessing(true);

      try {
        if (type === "pdf") {
          await uploadPDF(file);
        } else {
          await uploadImage(file);
        }

        const newFile = {
          id: Date.now(),
          name: file.name,
          type,
          date: new Date().toLocaleDateString()
        };

        setFiles((prev) => [newFile, ...prev]);
      } catch {
        alert("Upload failed");
      }

      setIsProcessing(false);
    };

    input.click();
  };

  // ================= Query Handler =================
  const handleSearch = async () => {
    if (!query) return;

    const userMessage = {
      id: Date.now(),
      role: "user",
      content: query
    };

    setMessages((prev) => [...prev, userMessage]);
    setQuery("");
    setIsProcessing(true);

    try {
      const res = await askQuestion(userMessage.content);

      const aiMessage = {
        id: Date.now() + 1,
        role: "assistant",
        content: res.data.response,
        confidence: res.data.confidence_score
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch {
      alert("Query failed");
    }

    setIsProcessing(false);
  };

  const removeFile = (id) => {
    setFiles(files.filter((f) => f.id !== id));
  };

  return (
    <div className="relative min-h-screen w-full bg-[#fdfdff] text-[#0F172A] font-sans overflow-x-hidden">

      {/* Background */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <motion.div
          animate={{ x: [0, 40, 0], y: [0, -40, 0] }}
          transition={{ duration: 15, repeat: Infinity }}
          className="absolute -top-[10%] -left-[10%] w-[60%] h-[60%] rounded-full bg-indigo-200/30 blur-[120px]"
        />
      </div>

      {/* NAVBAR */}
      <nav className="relative z-20 border-b bg-white/40 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-slate-900 rounded-xl flex items-center justify-center">
              <Database className="text-white w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold">Medical RAG</h1>
              <p className="text-[10px] uppercase text-emerald-600">
                Augmented Intelligence
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2 px-4 py-2 bg-indigo-600/5 text-indigo-700 rounded-full text-[11px] font-bold border">
            <ShieldCheck className="w-3.5 h-3.5" />
            Secure RAG
          </div>
        </div>
      </nav>

      <main className="relative z-10 max-w-7xl mx-auto px-6 py-20">

        {/* Hero */}
        <header className="max-w-3xl mb-20">
          <h2 className="text-5xl font-black leading-tight mb-6">
            Analyze documents grounded in RAG.
          </h2>
          <p className="text-lg text-slate-500">
            Upload medical records and extract grounded insights with confidence scoring.
          </p>
        </header>

        {/* Upload Section */}
        <div className="grid grid-cols-12 gap-6 mb-16">

          {/* PDF Card */}
          <div className="col-span-12 lg:col-span-4 bg-white/70 p-8 rounded-3xl shadow-xl">
            <FileText className="mb-4 text-indigo-600" />
            <h3 className="font-bold mb-2">Upload PDF</h3>
            <button
              onClick={() => handleUpload("pdf")}
              className="w-full bg-slate-900 text-white py-3 rounded-xl mt-4"
            >
              Upload Context
            </button>
          </div>

          {/* Image Card */}
          <div className="col-span-12 lg:col-span-4 bg-white/70 p-8 rounded-3xl shadow-xl">
            <ImageIcon className="mb-4 text-emerald-600" />
            <h3 className="font-bold mb-2">Upload Image</h3>
            <button
              onClick={() => handleUpload("image")}
              className="w-full bg-emerald-600 text-white py-3 rounded-xl mt-4"
            >
              Process OCR
            </button>
          </div>

          {/* History */}
          <div className="col-span-12 lg:col-span-4 bg-slate-100 p-8 rounded-3xl">
            <h3 className="font-bold mb-4 flex items-center gap-2">
              <History size={18} />
              Indexed Files
            </h3>

            {files.length === 0 ? (
              <p className="text-sm text-slate-400">No files yet</p>
            ) : (
              files.map((file) => (
                <div
                  key={file.id}
                  className="flex items-center justify-between bg-white p-3 rounded-xl mb-3"
                >
                  <span className="text-sm truncate">{file.name}</span>
                  <button onClick={() => removeFile(file.id)}>
                    <X size={14} />
                  </button>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Chat Section */}
        <div className="max-w-4xl mx-auto space-y-8">

          {/* Messages */}
          <AnimatePresence>
            {messages.map((msg) => (
              <motion.div
                key={msg.id}
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                className={`flex ${
                  msg.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`max-w-xl px-6 py-4 rounded-3xl shadow-lg ${
                    msg.role === "user"
                      ? "bg-indigo-600 text-white"
                      : "bg-white text-slate-800"
                  }`}
                >
                  <p className="whitespace-pre-wrap text-sm">
                    {msg.content}
                  </p>

                  {msg.role === "assistant" && msg.confidence !== undefined && (
                    <div className="mt-3 text-xs font-bold text-indigo-600">
                      Confidence: {(msg.confidence * 100).toFixed(1)}%
                    </div>
                  )}
                </div>
              </motion.div>
            ))}
          </AnimatePresence>

          {/* Typing */}
          {isProcessing && (
            <div className="flex justify-start">
              <div className="bg-white px-6 py-4 rounded-3xl shadow">
                <span className="animate-pulse text-indigo-600">
                  Generating response...
                </span>
              </div>
            </div>
          )}

          {/* Input Bar */}
          <div className="bg-white/90 p-4 rounded-3xl shadow-xl flex gap-4">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask about your uploaded reports..."
              className="flex-1 px-4 py-3 rounded-xl border border-slate-200 focus:outline-none"
            />
            <button
              onClick={handleSearch}
              className="bg-slate-900 text-white px-6 rounded-xl"
            >
              <ArrowRight size={20} />
            </button>
          </div>
        </div>
      </main>
    </div>
  );
};

export default App;

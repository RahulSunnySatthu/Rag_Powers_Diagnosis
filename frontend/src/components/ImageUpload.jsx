import { useState } from "react";
import { uploadImage } from "../api";

export default function ImageUpload() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleUpload = async () => {
    if (!file) return;

    try {
      const res = await uploadImage(file);
      setMessage(res.data.message);
    } catch {
      setMessage("Upload failed.");
    }
  };

  return (
    <div className="bg-white shadow-xl rounded-2xl p-8 hover:shadow-2xl transition">
      <h3 className="text-2xl font-semibold mb-6 text-slate-700">
        Upload Image (OCR)
      </h3>

      <input
        type="file"
        className="mb-6 w-full text-sm"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button
        onClick={handleUpload}
        className="w-full bg-purple-600 hover:bg-purple-700 text-white py-3 rounded-xl font-semibold transition duration-200"
      >
        Upload Image
      </button>

      {message && (
        <p className="mt-4 text-green-600 text-sm">{message}</p>
      )}
    </div>
  );
}

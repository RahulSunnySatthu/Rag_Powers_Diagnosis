import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "https://rag-powers-diagnosis.onrender.com";

export const uploadPDF = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return axios.post(`${API_BASE}/upload_pdf`, formData);
};

export const uploadImage = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return axios.post(`${API_BASE}/upload_image`, formData);
};

export const askQuestion = async (query) => {
  const formData = new URLSearchParams();
  formData.append("query", query);

  return axios.post(`${API_BASE}/ask`, formData);
};

export const resetDocuments = async () => {
  return axios.post(`${API_BASE}/reset`);
};

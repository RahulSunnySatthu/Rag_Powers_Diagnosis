import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

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

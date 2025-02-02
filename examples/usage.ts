import axios from "axios";
import FormData from "form-data";
import fs from "fs";
import { basename } from "path";

export const BASE_URL = "https://your-api-url.com";
export const API_KEY = process.env.API_KEY || "";

export interface TokenCount {
  o200k_base: number;
  cl100k_base: number;
}

export interface ProcessDocumentResponse {
  markdown: string;
  language: string;
  mimetype: string;
  token_count: TokenCount;
}

export async function processDocument(
  filePath: string,
  useLLM: boolean = false
): Promise<ProcessDocumentResponse> {
  if (!fs.existsSync(filePath)) {
    throw new Error(`File not found: ${filePath}`);
  }
  const formData = new FormData();
  formData.append("file", fs.createReadStream(filePath), basename(filePath));
  formData.append("use_llm", String(useLLM).toLowerCase());

  const response = await axios.post(`${BASE_URL}/process/document`, formData, {
    headers: {
      "X-API-Key": API_KEY,
      ...formData.getHeaders(),
    },
  });

  return response.data as ProcessDocumentResponse;
}

export async function processUrl(
  url: string
): Promise<ProcessDocumentResponse> {
  const response = await axios.post(`${BASE_URL}/process/url`, null, {
    params: { url },
    headers: {
      "X-API-Key": API_KEY,
    },
  });
  return response.data as ProcessDocumentResponse;
}

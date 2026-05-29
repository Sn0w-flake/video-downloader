import axios, { AxiosError } from "axios";

export const api = axios.create({
  baseURL: "/api",
  timeout: 60000,
});

export interface FormatItem {
  format_id: string;
  ext?: string;
  resolution?: string;
  fps?: number;
  filesize?: number;
  filesize_approx?: number;
  vcodec?: string;
  acodec?: string;
  format_note?: string;
  tbr?: number;
  abr?: number;
  kind: "video" | "audio" | "video_only" | "unknown";
}

export interface VideoInfo {
  url: string;
  title: string;
  uploader?: string;
  thumbnail?: string;
  duration?: number;
  extractor?: string;
  description?: string;
  formats: FormatItem[];
  subtitles: string[];
}

export interface BatchItem {
  url: string;
  ok: boolean;
  info?: VideoInfo;
  error?: string;
}

export async function fetchInfo(url: string): Promise<VideoInfo> {
  const { data } = await api.get<VideoInfo>("/info", { params: { url } });
  return data;
}

export async function fetchBatch(urls: string[]): Promise<BatchItem[]> {
  const { data } = await api.post<{ results: BatchItem[] }>("/batch", { urls });
  return data.results;
}

export function downloadUrl(url: string, format_id: string): string {
  const u = new URLSearchParams({ url, format_id });
  return `/api/download?${u.toString()}`;
}

export function readableError(e: unknown): string {
  if (e instanceof AxiosError) {
    const d = e.response?.data as { detail?: string } | undefined;
    if (d?.detail) return d.detail;
    if (e.response?.status) return `HTTP ${e.response.status}`;
    return e.message;
  }
  if (e instanceof Error) return e.message;
  return "unknown error";
}

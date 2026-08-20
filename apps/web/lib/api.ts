export const apiBaseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/$/, "") ?? "http://localhost:8000";

export type ReliefRequest = {
  reference: string;
  district: string;
  location: string;
  needType: string;
  peopleCount: number;
  priority: string;
  description: string;
  status: string;
  createdAt: string;
  updatedAt: string;
  contactMethod?: string;
  contactValue?: string;
};

export async function readError(response: Response): Promise<string> {
  try {
    const body = (await response.json()) as { detail?: string; error?: { message?: string } };
    return body.detail ?? body.error?.message ?? `Request failed (${response.status})`;
  } catch {
    return `Request failed (${response.status})`;
  }
}


const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "http://localhost:8000").replace(/\/$/, "");

/**
 * Request one audit report from the FastAPI backend.
 *
 * Error responses from Page Pulse have a stable `error.message` shape. The
 * fallback keeps the UI helpful if a proxy or unexpected server sends another
 * response format.
 */
export async function requestAudit(url) {
  let response;

  try {
    response = await fetch(`${API_BASE_URL}/api/audit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });
  } catch {
    throw new Error("Could not reach Page Pulse. Check that the backend is running and try again.");
  }

  const body = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(body?.error?.message || "The audit could not be completed. Please try again.");
  }

  return body;
}


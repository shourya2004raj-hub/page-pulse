import { useEffect, useState } from "react";

import AuditForm from "./components/AuditForm";
import AuditReport from "./components/AuditReport";
import ThemeToggle from "./components/ThemeToggle";
import { requestAudit } from "./services/auditApi";

const initialTheme = window.localStorage.getItem("page-pulse-theme") || "light";

export default function App() {
  const [url, setUrl] = useState("");
  const [report, setReport] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [theme, setTheme] = useState(initialTheme);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    document.documentElement.style.colorScheme = theme;
    window.localStorage.setItem("page-pulse-theme", theme);
  }, [theme]);

  async function handleSubmit(event) {
    event.preventDefault();
    const normalizedUrl = url.trim();

    if (!normalizedUrl) {
      setError("Enter a website URL to begin the audit.");
      setReport(null);
      return;
    }

    setError("");
    setReport(null);
    setIsLoading(true);

    try {
      const nextReport = await requestAudit(normalizedUrl);
      setReport(nextReport);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="app-shell">
      <header className="site-header">
        <a className="brand" href="/" aria-label="Page Pulse home">
          <span className="brand__mark" aria-hidden="true">P</span>
          <span>Page Pulse</span>
        </a>
        <ThemeToggle theme={theme} onToggle={() => setTheme((currentTheme) => (currentTheme === "dark" ? "light" : "dark"))} />
      </header>

      <main>
        <section className="hero" aria-labelledby="page-title">
          <p className="eyebrow">Webpage intelligence, in seconds</p>
          <h1 id="page-title">A clearer pulse on every page.</h1>
          <p className="hero__copy">
            Check a webpage’s technical response, content fundamentals, and key SEO signals in one focused report.
          </p>
          <AuditForm url={url} onUrlChange={setUrl} onSubmit={handleSubmit} isLoading={isLoading} />
          <p className="form-note">Public HTTP and HTTPS pages only. We never store your audits.</p>
        </section>

        <section className="workspace" aria-live="polite" aria-busy={isLoading}>
          {isLoading ? (
            <div className="state-card state-card--loading">
              <span className="loading-orb" aria-hidden="true" />
              <h2>Reading the page…</h2>
              <p>We’re checking its response, content, and metadata.</p>
            </div>
          ) : null}

          {error ? (
            <div className="state-card state-card--error" role="alert">
              <span aria-hidden="true">!</span>
              <div>
                <h2>The audit could not run</h2>
                <p>{error}</p>
              </div>
            </div>
          ) : null}

          {report ? <AuditReport report={report} /> : null}

          {!isLoading && !error && !report ? (
            <div className="empty-state">
              <span className="empty-state__icon" aria-hidden="true">⌁</span>
              <h2>Ready when you are</h2>
              <p>Enter a full URL above to create your first audit report.</p>
            </div>
          ) : null}
        </section>
      </main>

      <footer className="site-footer">
        <span>Page Pulse · Focused webpage audits</span>
        <a href="https://digitalheroesco.com" target="_blank" rel="noreferrer">
          Built for Digital Heroes Training Task
        </a>
      </footer>
    </div>
  );
}


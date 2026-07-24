import ReportCard from "./ReportCard";

function formatResponseTime(milliseconds) {
  return milliseconds < 1_000 ? `${milliseconds} ms` : `${(milliseconds / 1_000).toFixed(2)} s`;
}

function shortUrl(url) {
  try {
    return new URL(url).hostname;
  } catch {
    return url;
  }
}

export default function AuditReport({ report }) {
  const statusTone = report.http_status >= 400 ? "warning" : "success";
  const imageTone = report.images_missing_alt > 0 ? "warning" : "success";

  return (
    <section className="report" aria-labelledby="report-heading">
      <div className="report__heading">
        <div>
          <p className="eyebrow">Audit complete</p>
          <h2 id="report-heading">{shortUrl(report.final_url)}</h2>
        </div>
        <a className="external-link" href={report.final_url} target="_blank" rel="noreferrer">
          Visit page <span aria-hidden="true">↗</span>
        </a>
      </div>

      <div className="report-grid">
        <ReportCard label="HTTP status" value={report.http_status} detail="Server response" tone={statusTone} />
        <ReportCard label="Response time" value={formatResponseTime(report.response_time_ms)} detail="Total request time" />
        <ReportCard label="Secure connection" value={report.is_https ? "HTTPS" : "HTTP"} detail="Final destination" tone={report.is_https ? "success" : "warning"} />
        <ReportCard label="H1 headings" value={report.h1_count} detail="Primary page headings" />
        <ReportCard label="Images without alt" value={report.images_missing_alt} detail="Accessibility check" tone={imageTone} />
        <ReportCard label="Approx. word count" value={report.approximate_word_count.toLocaleString()} detail="Visible page content" />
        <ReportCard label="Page title" value={report.title} detail="Browser tab and search result title" wide />
        <ReportCard label="Meta description" value={report.meta_description} detail="Search result summary" wide />
        <ReportCard label="Open Graph title" value={report.open_graph_title} detail="Social-sharing title" wide />
        <ReportCard label="Canonical URL" value={report.canonical_url} detail="Preferred indexing URL" wide />
        <ReportCard label="Favicon" value={report.favicon_url ? "Found" : "Not found"} detail={report.favicon_url || "No favicon URL was detected"} wide />
      </div>

      {report.url !== report.final_url ? (
        <p className="redirect-note">
          Redirected from <code>{report.url}</code>
        </p>
      ) : null}
    </section>
  );
}


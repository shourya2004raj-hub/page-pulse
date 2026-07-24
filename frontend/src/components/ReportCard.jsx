export default function ReportCard({ label, value, detail, tone = "default", wide = false }) {
  return (
    <article className={`report-card report-card--${tone}${wide ? " report-card--wide" : ""}`}>
      <p className="report-card__label">{label}</p>
      <p className="report-card__value">{value ?? "Not found"}</p>
      {detail ? <p className="report-card__detail">{detail}</p> : null}
    </article>
  );
}


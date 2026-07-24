export default function AuditForm({ url, onUrlChange, onSubmit, isLoading }) {
  return (
    <form className="audit-form" onSubmit={onSubmit} noValidate>
      <label className="sr-only" htmlFor="website-url">
        Website URL to audit
      </label>
      <input
        id="website-url"
        name="url"
        type="url"
        inputMode="url"
        autoComplete="url"
        placeholder="https://example.com"
        value={url}
        onChange={(event) => onUrlChange(event.target.value)}
        disabled={isLoading}
        required
      />
      <button type="submit" disabled={isLoading}>
        {isLoading ? <span className="spinner" aria-hidden="true" /> : <span aria-hidden="true">✦</span>}
        {isLoading ? "Auditing…" : "Audit page"}
      </button>
    </form>
  );
}


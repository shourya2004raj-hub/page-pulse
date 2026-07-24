# Page Pulse

Page Pulse is a lightweight webpage audit tool built for the Digital Heroes Software Development internship qualification task. Enter any public HTTP or HTTPS URL to receive a focused report on its technical response, content fundamentals, and SEO metadata.

> **Live demo:** https://page-pulse-sigma-opal.vercel.app  
> **API:** https://page-pulse-api-y6ll.onrender.com

## Features

- Audits public HTTP and HTTPS webpages through `POST /api/audit`.
- Reports HTTP status, response time, page title, meta description, H1 count, images missing alt text, and approximate word count.
- Also reports canonical URL, HTTPS status, favicon URL, and Open Graph title.
- Handles invalid URLs, unsupported protocols, timeouts, redirects, DNS failures, SSL failures, network failures, non-HTML responses, oversized responses, and unexpected parsing failures.
- Blocks private, loopback, and local-network destinations to reduce SSRF risk.
- Responsive React UI with loading, empty, error, and report states.
- Dark mode, keyboard-friendly controls, reduced-motion support, and a required Digital Heroes footer credit.
- GitHub Actions verifies backend tests and the frontend production build on every push to `main`.

## Architecture

```text
React + Vite frontend
        |
        | POST /api/audit
        v
FastAPI route -> Audit service -> Safe HTTP fetcher -> HTML parser
        |               |                 |                |
     Pydantic        orchestration     httpx            BeautifulSoup + lxml
```

The route contains no business logic. `AuditService` coordinates an audit, `page_fetcher.py` performs bounded and redirect-aware requests, and `html_parser.py` is a pure HTML-to-metrics function.

## Folder structure

```text
.
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routes
│   │   ├── core/         # configuration, errors, SSRF protection
│   │   ├── models/       # Pydantic request/response contracts
│   │   ├── parsers/      # HTML metric extraction
│   │   └── services/     # fetching and audit orchestration
│   └── tests/            # parser, service, and API tests
├── frontend/
│   └── src/              # React components, API client, styles
├── docs/                 # Loom outline, AI-disclosure guidance, submission list
└── render.yaml           # Render Blueprint deployment configuration
```

## Installation

Prerequisites:

- Python 3.12 or later
- Node.js 20 or later
- npm

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

The API starts at `http://localhost:8000`. Interactive OpenAPI documentation is available at `http://localhost:8000/docs`.

### Frontend

Open a second terminal:

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```

The Vite app normally starts at `http://localhost:5173`.

## Environment variables

### Backend

| Variable | Required | Default | Purpose |
|---|---:|---|---|
| `APP_ENV` | No | `development` | Runtime environment label. |
| `CORS_ORIGINS` | Yes in production | `http://localhost:5173` | Comma-separated frontend origins allowed to call the API. |
| `REQUEST_TIMEOUT_SECONDS` | No | `10` | Maximum time allowed for a page request. |
| `MAX_RESPONSE_BYTES` | No | `2000000` | Maximum downloaded HTML size. |
| `MAX_REDIRECTS` | No | `5` | Maximum redirect hops. |
| `USER_AGENT` | No | `PagePulse/1.0` | Identifier sent when requesting a webpage. |

### Frontend

| Variable | Required | Default | Purpose |
|---|---:|---|---|
| `VITE_API_BASE_URL` | Yes in production | `http://localhost:8000` | Public Render API URL, without a trailing slash. |

## API documentation

### `POST /api/audit`

Request:

```json
{
  "url": "https://example.com"
}
```

Successful response:

```json
{
  "url": "https://example.com",
  "final_url": "https://example.com/",
  "http_status": 200,
  "response_time_ms": 184,
  "is_https": true,
  "title": "Example Domain",
  "meta_description": null,
  "h1_count": 1,
  "images_missing_alt": 0,
  "approximate_word_count": 42,
  "canonical_url": null,
  "favicon_url": "https://example.com/favicon.ico",
  "open_graph_title": null
}
```

Known failures use a stable shape:

```json
{
  "error": {
    "code": "timeout",
    "message": "The website took too long to respond."
  }
}
```

| Status | Example code | Meaning |
|---:|---|---|
| 400 | `invalid_url`, `unsafe_url` | Invalid input or blocked internal destination. |
| 422 | `non_html_content`, `content_too_large` | A reachable resource cannot be safely audited as HTML. |
| 502 | `dns_failure`, `ssl_failure`, `network_failure` | The remote host could not be reached safely. |
| 504 | `timeout` | The remote host took too long to respond. |
| 500 | `parser_failure` | An unexpected parsing error was contained. |

## Testing

```powershell
cd backend
.\.venv\Scripts\python -m pytest -v
```

The tests cover:

- parser happy path and missing metadata;
- invalid URL rejection;
- parser failure containment;
- success, timeout, and non-HTML API responses.

## Deployment

For a deadline-focused walkthrough, use [`docs/DEPLOY_TODAY.md`](docs/DEPLOY_TODAY.md).

### 1. Push to GitHub

```powershell
git init
git add .
git commit -m "feat: build Page Pulse audit application"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/page-pulse.git
git push -u origin main
```

Create the remote repository as **public** before running the final two commands.

### 2. Deploy the API on Render

1. In Render, choose **New +** → **Blueprint** and connect the GitHub repository.
2. Render reads `render.yaml` and deploys the `backend/` directory.
3. Set `CORS_ORIGINS` to the Vercel URL after the frontend exists.
4. Copy the public service URL and verify `/health`.

### 3. Deploy the UI on Vercel

1. In Vercel, import the same GitHub repository.
2. Set **Root Directory** to `frontend`.
3. Add `VITE_API_BASE_URL` with the Render URL, for example `https://page-pulse-api.onrender.com`.
4. Deploy and test a real public page.
5. Return to Render and set `CORS_ORIGINS` to the Vercel deployment URL if you have not already.

## Three important design decisions

### 1. Separate HTTP retrieval from HTML parsing

The HTML parser takes HTML and a base URL as input, with no network access. That makes parsing tests fast and deterministic. The alternative—fetching inside the parser—would make unit tests slow and dependent on outside websites.

### 2. Use explicit API error contracts

The frontend receives `{ "error": { "code", "message" } }` for expected failures. This prevents the UI from interpreting low-level library exceptions and gives users a useful explanation. The alternative, returning raw server errors, would leak implementation details and create fragile UI code.

### 3. Protect the backend from SSRF

A public URL-fetching service must not be able to access internal hosts. Page Pulse validates allowed protocols, resolves hostnames, blocks non-public IP addresses, and validates every redirect destination. This small amount of complexity is justified because it protects the deployed service.

## Future improvements

- Persist audit history for signed-in users.
- Add Lighthouse or Core Web Vitals data through an asynchronous job system.
- Offer an opt-in browser-rendered audit mode for JavaScript-heavy sites.
- Add rate limiting and observability for production traffic.
- Add Playwright end-to-end tests after deployment.

## AI-use disclosure

See [`docs/AI_DISCLOSURE.md`](docs/AI_DISCLOSURE.md). Personalize it so that it truthfully reflects your own review, testing, debugging, refinements, and final validation.

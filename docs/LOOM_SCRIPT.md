# Page Pulse Loom script

Aim for two to three minutes. Do not read it word-for-word; use it as a clear outline.

## 0:00 - 0:20: Introduce the project

"This is Page Pulse, a small web application that audits a public webpage. I built it for the Digital Heroes SDE qualification task. A user enters a URL and receives technical, content, and SEO metadata in one report."

## 0:20 - 0:55: Demonstrate a successful audit

1. Enter a stable public page, such as `https://example.com`.
2. Point out the loading state.
3. Show the returned HTTP status, response time, title, H1 count, word count, and image-alt result.
4. If available, mention the canonical URL, favicon, and Open Graph title cards.

Suggested narration:

"The frontend makes one POST request to `/api/audit`. The API fetches the page, verifies that it is HTML, and returns a typed JSON report."

## 0:55 - 1:25: Demonstrate failure handling

1. Enter `ftp://example.com` to show invalid protocol handling.
2. Explain that non-HTML responses and slow/unreachable sites return a helpful message instead of crashing.

Suggested narration:

"I intentionally map network, timeout, DNS, SSL, parsing, and content-type failures into clear API errors. That gives the frontend predictable states to display."

## 1:25 - 2:05: Walk through one code decision

Show `backend/app/services/audit_service.py` and `backend/app/parsers/html_parser.py`.

"I separated the route, fetching, and parsing responsibilities. The route only handles HTTP. The audit service coordinates the work. The parser is a pure function, so it can be tested with fixed HTML files without real network calls."

## 2:05 - 2:30: Self-critique

"With another day, I would add an optional browser-rendered audit mode for JavaScript-heavy websites. This version intentionally analyzes the server-delivered HTML because it is simpler, faster, and easier to deploy on a free tier."

## Before recording

- Start both services and confirm the frontend can call the deployed backend.
- Use your own voice and explain choices you understand.
- Keep the recording under three minutes.


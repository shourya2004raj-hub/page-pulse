# Page Pulse interview preparation

## 1. Why FastAPI?

FastAPI gives me typed request validation with Pydantic, automatic OpenAPI documentation, and async support for network-bound work. It kept the API small and readable without adding a larger framework.

## 2. Why use asynchronous HTTP requests?

Fetching a remote webpage spends most of its time waiting on the network. `httpx.AsyncClient` lets the API serve other requests while a site is responding, which is more suitable than blocking the server thread.

## 3. Why keep parsing separate from fetching?

The parser receives HTML and returns metrics. It has no network dependency, so I can test it using known HTML fixtures. This makes tests quick and avoids failures caused by a third-party site changing.

## 4. How do you handle invalid or failed URLs?

The backend validates URL format and allowed protocols first. It maps known failures—DNS, SSL, timeout, non-HTML, network, and parser errors—to stable JSON errors with meaningful HTTP status codes.

## 5. What is SSRF and how is it addressed?

Server-side request forgery occurs when an attacker convinces a server to request internal resources. Page Pulse only allows HTTP(S), rejects localhost and private IP addresses, resolves hostnames before fetching, and checks every redirect destination.

## 6. Why return `422` for non-HTML content?

The URL can be valid and reachable while still being unsuitable for an HTML audit, such as a PDF or image. `422 Unprocessable Content` communicates that distinction more clearly than pretending it is a network failure.

## 7. What do Pydantic models add?

They define the API contract in code. Request models validate incoming JSON, response models prevent accidental response-shape drift, and the automatic docs reflect the same contract.

## 8. Why not use Playwright to render JavaScript sites?

Browser rendering would improve coverage for client-side applications, but it adds browser binaries, longer jobs, and more deployment complexity. I deliberately scoped this version to server-delivered HTML to keep it fast and reliable on a free tier.

## 9. How did you test it?

I tested parsing with a fixed HTML fixture, service behavior with mocked dependencies, and public API error responses. The test suite covers success, invalid URLs, parser failure, timeout, and non-HTML results.

## 10. What would you improve next?

I would add rate limiting, structured logging, browser-rendered audits as an opt-in job, and persistent audit history. I would keep those separate from the current synchronous audit path.


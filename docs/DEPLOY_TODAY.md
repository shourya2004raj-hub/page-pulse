# Deploy Page Pulse today

This is the fastest safe deployment path for the task.

## 1. Get the project onto GitHub

Download and extract `page-pulse-project.zip` somewhere outside the Codex workspace. Then create a **new empty public** GitHub repository called `page-pulse` (do not add a README or `.gitignore` on GitHub).

From the extracted project folder, run:

```powershell
git init
git add .
git commit -m "feat: build Page Pulse audit application"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/page-pulse.git
git push -u origin main
```

Copy the GitHub repository URL. It is one of the required submission links.

## 2. Deploy the FastAPI backend to Render

1. Sign in to Render with GitHub.
2. Select **New +** → **Blueprint** and select the `page-pulse` repository.
3. Render reads `render.yaml`; choose the free plan if prompted.
4. Render asks for `CORS_ORIGINS`. Enter a temporary value now, such as `http://localhost:5173`. You will replace it after Vercel gives you the frontend URL.
5. Wait until the service is live. Copy the URL, for example `https://page-pulse-api.onrender.com`.
6. Open `https://YOUR-RENDER-URL/health`. It must return:

```json
{"status":"ok"}
```

If Blueprint setup is unavailable, create a **Web Service** manually with these settings:

| Setting | Value |
|---|---|
| Root Directory | `backend` |
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

## 3. Deploy the frontend to Vercel

1. Sign in to Vercel with GitHub and choose **Add New → Project**.
2. Import the same `page-pulse` repository.
3. Set **Root Directory** to `frontend`.
4. In Environment Variables, add:

```text
VITE_API_BASE_URL=https://YOUR-RENDER-URL
```

Do not include a trailing slash.

5. Deploy. Copy the Vercel URL, for example `https://page-pulse.vercel.app`.

## 4. Connect both deployments

In Render → your API service → Environment, update:

```text
CORS_ORIGINS=https://YOUR-VERCEL-URL
```

Save the value and manually redeploy the Render service. Vercel environment-variable changes apply only to a new deployment, so redeploy Vercel too if you change `VITE_API_BASE_URL`.

## 5. Verify before recording Loom

- Open the Vercel URL in an incognito window.
- Enter `https://example.com` and confirm a report appears.
- Enter `ftp://example.com` and confirm a readable error appears.
- Confirm the footer includes the Digital Heroes credit and link.
- Open the GitHub Actions tab. The CI workflow should show backend tests and frontend build results.

## If you get a CORS error

The Render `CORS_ORIGINS` value must match the Vercel site origin exactly:

```text
https://page-pulse.vercel.app
```

No trailing slash, no path, no quotes. Save it and redeploy Render.


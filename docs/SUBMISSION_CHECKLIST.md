# Submission checklist

## Code and deployment

- [ ] Create a public GitHub repository named `page-pulse`.
- [ ] Push this project to the repository.
- [ ] Deploy the backend to Render from `render.yaml`.
- [ ] Open `https://YOUR-RENDER-URL/health` and confirm it returns `{ "status": "ok" }`.
- [ ] Deploy `frontend/` to Vercel.
- [ ] Set Vercel environment variable `VITE_API_BASE_URL` to your Render URL, without a trailing slash.
- [ ] Set Render `CORS_ORIGINS` to your Vercel URL, for example `https://page-pulse.vercel.app`.
- [ ] Redeploy both services after changing environment variables.
- [ ] Audit a public URL from the live Vercel site.

## Required task evidence

- [ ] Public GitHub repository URL.
- [ ] Live Vercel URL.
- [ ] README in the repository.
- [ ] Test files in the repository.
- [ ] Loom recording, two to three minutes.
- [ ] Short, truthful AI-use disclosure.
- [ ] Footer visibly says "Built for Digital Heroes Training Task" and links to `https://digitalheroesco.com`.

## Final submission

- [ ] Put links in a Google Drive folder named `Software Development (SDE)_YourFullName`.
- [ ] Set the folder to "Anyone with the link can view".
- [ ] Follow `@realshreyanshsingh` on Instagram.
- [ ] Send the single Google Drive folder link by Instagram DM.


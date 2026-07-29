# Solar Forecast

A tiny installable PWA that shows a warm, Apple-Weather-style solar production
forecast, powered by the free [Forecast.Solar](https://forecast.solar) public API
(no API key needed).

## Deploy to GitHub Pages

1. Create a new GitHub repo and push this folder to it.
2. In the repo settings, enable **Pages** → deploy from the `main` branch, root folder.
3. Open the published URL on your phone/Mac in Safari or Chrome, then
   "Add to Home Screen" (iOS) or "Install App" (Chrome/Edge) to use it like a native app.

## Notes

- Location/tilt/azimuth/system size are baked into the API URL in `index.html`
  (`-40.819, 175.207694, 45°, 0° azimuth, 1.6 kWp`). Edit `API_URL` there to change them.
- The forecast refreshes every 30 minutes automatically, and falls back to the
  last cached result (stored in `localStorage` + a service worker cache) if the
  API is unreachable.
- No build step — it's plain HTML/CSS/JS, so it runs straight from GitHub Pages.

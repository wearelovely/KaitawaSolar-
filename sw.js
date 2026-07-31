const SHELL_CACHE = "solar-shell-v3";
const API_CACHE = "solar-api-v1";
const SHELL_FILES = [
  "./",
  "./index.html",
  "./manifest.json",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./icons/apple-touch-icon.png",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(SHELL_CACHE).then((cache) => cache.addAll(SHELL_FILES))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== SHELL_CACHE && key !== API_CACHE)
          .map((key) => caches.delete(key))
      )
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Solcast uses Bearer auth — let the browser handle it directly so CORS works cleanly
  if (url.hostname === "api.solcast.com.au") return;

  if (url.hostname === "api.forecast.solar" || url.hostname === "api.open-meteo.com") {
    event.respondWith(networkFirst(request));
    return;
  }

  if (request.method === "GET" && url.origin === self.location.origin) {
    if (request.mode === "navigate") {
      // Always network-first for HTML so deployments show immediately
      event.respondWith(fetch(request).catch(() => caches.match(request)));
    } else {
      event.respondWith(
        caches.match(request).then((cached) => cached || fetch(request))
      );
    }
  }
});

async function networkFirst(request) {
  const cache = await caches.open(API_CACHE);
  try {
    const response = await fetch(request);
    if (response.ok) cache.put(request, response.clone());
    return response;
  } catch (err) {
    const cached = await cache.match(request);
    if (cached) return cached;
    throw err;
  }
}

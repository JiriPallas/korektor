// Service worker pro všechny čtyři jazyky (/korektor/, /de/, /en/, /sv/).
// Program se uloží hned, slovník daného jazyka až při prvním použití – pak funguje i bez internetu.
const CACHE = "korektor-v2";
const SOUBORY = ["hunspell.js", "jazyky.js"];
self.addEventListener("install", e => { self.skipWaiting(); e.waitUntil(caches.open(CACHE).then(c => c.addAll(SOUBORY))); });
self.addEventListener("activate", e => e.waitUntil(self.clients.claim().then(() => caches.keys()).then(k =>
  Promise.all(k.filter(n => n.startsWith("korektor-") && n !== CACHE).map(n => caches.delete(n))))));
self.addEventListener("fetch", e => {
  const url = new URL(e.request.url);
  if (url.origin !== location.origin || e.request.method !== "GET") return;
  if (url.pathname.includes("/slovnik/") || url.pathname.endsWith("hunspell.js")) {      // slovník: z paměti, mění se zřídka
    e.respondWith(caches.match(e.request).then(r => r || fetch(e.request).then(o => { const k = o.clone(); caches.open(CACHE).then(c => c.put(e.request, k)); return o; })));
    return;
  }
  const pozadavek = e.request.mode === "navigate"
    ? new Request(e.request.url, { cache: "no-cache", credentials: "same-origin" })
    : new Request(e.request, { cache: "no-cache" });
  e.respondWith(fetch(pozadavek).then(r => { const k = r.clone(); caches.open(CACHE).then(c => c.put(e.request, k)); return r; })
    .catch(() => caches.match(e.request, { ignoreSearch: true })));
});

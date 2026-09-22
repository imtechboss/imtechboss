// Service Worker Uninstaller & Cache Cleaner for Tech Boss
self.addEventListener('install', () => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.map((key) => caches.delete(key).catch(() => {}))))
      .then(() => self.registration.unregister())
      .catch((err) => console.error('SW cleanup error:', err))
  );
});

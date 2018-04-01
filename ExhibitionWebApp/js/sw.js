
console.log('Script loaded!')
var cacheStorageKey = 'ExhibitionWebApp-1.2'

var cacheList = [
  '/',
  "/index.html",
  "/expo_info.py",
  "/index.py",
  "/top.png",
  "/sniec.json",
  "/shexpo.json",
  '/js/amazeui.min.js',
  '/js/brython.js',
  '/js/brython_modules.js',
  '/js/jquery-3.3.1.min.js',
  '/fonts/fontawesome-webfont.woff2',
  '/css/amazeui.min.css'
]

self.addEventListener('install', function(e) {
  console.log('Cache event!')
  e.waitUntil(
    caches.open(cacheStorageKey).then(function(cache) {
      console.log('Adding to Cache:', cacheList)
      return cache.addAll(cacheList)
    }).then(function() {
      console.log('Skip waiting!')
      return self.skipWaiting()
    })
  )
})

self.addEventListener('activate', function(event) {
  console.log('Activate event')
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(cacheName) {
          // 如果当前版本和缓存版本不一致
          if (cacheName !== cacheStorageKey) {
            console.log('Activate event: del cache')
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

self.addEventListener('fetch', function(e) {
  // console.log('Fetch event:', e.request.url)
  e.respondWith(
    caches.match(e.request).then(function(response) {
      if (response != null) {
        console.log('Using cache for:', e.request.url)
        return response
      }
      console.log('Fallback to fetch:', e.request.url)
      return fetch(e.request.url)
    })
  )
})

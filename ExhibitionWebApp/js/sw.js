
console.log('Script loaded!')
var cacheStorageKey = 'ExhibitionWebApp-1.2'

var cacheList = [
  '/ExhibitionWebApp/',
  "/ExhibitionWebApp/index.html",
  "/ExhibitionWebApp/expo_info.py",
  "/ExhibitionWebApp/index.py",
  "/ExhibitionWebApp/top.png",
  "/ExhibitionWebApp/sniec.json",
  '/ExhibitionWebApp/js/amazeui.min.js',
  '/ExhibitionWebApp/js/brython.js',
  '/ExhibitionWebApp/js/brython_modules.js',
  '/ExhibitionWebApp/js/jquery-3.3.1.min.js',
  '/ExhibitionWebApp/fonts/fontawesome-webfont.woff2',
  '/ExhibitionWebApp/css/amazeui.min.css'
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
          // �����ǰ�汾�ͻ���汾��һ��
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

var staticCacheName = 'Food Pharmacy App-v3';

self.addEventListener('install', function(event) {

});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    fetch(event.request)
  )
});

// Enable navigation preload
// const enableNavigationPreload = async () => {
//   if (self.registration.navigationPreload) {
//     await self.registration.navigationPreload.enable();
//   }
// };

// const deleteCache = async (key) => {
//   await caches.delete(key);
// };

// const deleteOldCaches = async () => {
//   const cacheKeepList = [staticCacheName];
//   const keyList = await caches.keys();
//   const cachesToDelete = keyList.filter((key) => !cacheKeepList.includes(key));
//   await Promise.all(cachesToDelete.map(deleteCache));
// };


// self.addEventListener("activate", (event) => {
//   event.waitUntil(enableNavigationPreload());
//   event.waitUntil(deleteOldCaches());
// });

// const addResourcesToCache = async (resources) => {
//   const cache = await caches.open(staticCacheName);
//   await cache.addAll(resources);
// };

// self.addEventListener('install', function(event) {
//   event.waitUntil(
//     addResourcesToCache([
//       '/',
//     ])
//   );
// });


// const putInCache = async (request, response) => {
//   const cache = await caches.open(staticCacheName);
//   await cache.put(request, response);
// };

// const cacheFirst = async ({ request, fallbackUrl }) => {
//   // First try to get the resource from the cache
//   const responseFromCache = await caches.match(request);
//   if (responseFromCache) {
//     return responseFromCache;
//   }

//   // Next try to get the resource from the network
//   try {
//     const responseFromNetwork = await fetch(request);
//     if(responseFromNetwork.status >= 200 && responseFromNetwork.status < 300) {
//       putInCache(request, responseFromNetwork.clone());
//     }
//     return responseFromNetwork;
//   } 
//   catch (error) {
//     const fallbackResponse = await caches.match(fallbackUrl);
//     if (fallbackResponse) {
//       return fallbackResponse;
//     }
//     return new Response("Network error", {
//       status: 408,
//       headers: { "Content-Type": "text/plain" },
//     });
//   }
// };


// self.addEventListener('fetch', function(event) {
//   if (event.request.method !== 'GET') {
//     return;
//   }
//   event.respondWith(
//     cacheFirst({
//       request: event.request,
//       fallbackUrl: "/",
//     })
//   );
// });
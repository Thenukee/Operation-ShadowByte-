// Open IndexedDB
function openDatabase() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open('ShadowByteDB', 1);
        request.onupgradeneeded = event => {
            const db = event.target.result;
            db.createObjectStore('suspects', { keyPath: 'id' });
        };
        request.onsuccess = event => resolve(event.target.result);
        request.onerror = event => reject(event.target.error);
    });
}

// Save data to IndexedDB
async function saveToIndexedDB(storeName, data) {
    const db = await openDatabase();
    const tx = db.transaction(storeName, 'readwrite');
    const store = tx.objectStore(storeName);
    data.forEach(item => store.put(item));
    tx.oncomplete = () => console.log('Data saved to IndexedDB');
}

// Example: Fetch and store suspects
async function fetchAndCacheSuspects() {
    const response = await fetch('/api/get-results?suspect_id=12345');
    const suspects = await response.json();
    await saveToIndexedDB('suspects', suspects.data);
}
fetchAndCacheSuspects();

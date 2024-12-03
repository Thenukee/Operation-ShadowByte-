<script>
// Function to fetch and cache data from the server
async function fetchAndCache(endpoint) {
    try {
        const response = await fetch(endpoint);
        if (!response.ok) throw new Error("Failed to fetch data");
        const data = await response.json();

        // Save the data locally in LocalStorage
        localStorage.setItem(endpoint, JSON.stringify(data));

        console.log("Data cached locally:", data);
        return data;
    } catch (error) {
        console.error("Error fetching data:", error);

        // Load from cache if available
        const cachedData = localStorage.getItem(endpoint);
        if (cachedData) {
            console.log("Using cached data:", JSON.parse(cachedData));
            return JSON.parse(cachedData);
        }
    }
}

// Example usage: Fetch and cache suspects
fetchAndCache('/api/get-results?suspect_id=12345');
</script>

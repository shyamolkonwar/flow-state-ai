// FlowFacilitator Extension Popup Script

document.addEventListener('DOMContentLoaded', () => {
    loadStatus();

    // Event listeners
    document.getElementById('open-dashboard').addEventListener('click', () => {
        chrome.tabs.create({ url: 'http://localhost:3000' });
    });

    document.getElementById('settings').addEventListener('click', () => {
        chrome.runtime.openOptionsPage();
    });

    // Refresh status every 2 seconds
    setInterval(loadStatus, 2000);
});

async function loadStatus() {
    try {
        const result = await chrome.storage.local.get([
            'isBlocking',
            'blockedDomains',
            'blocksToday'
        ]);

        const isBlocking = result.isBlocking || false;
        const blockedDomains = result.blockedDomains || [];
        const blocksToday = result.blocksToday || 0;

        // Update status
        const statusEl = document.getElementById('status');
        const statusText = document.getElementById('status-text');

        if (isBlocking) {
            statusEl.className = 'status active';
            statusText.textContent = '🎯 Blocking Active';
        } else {
            statusEl.className = 'status inactive';
            statusText.textContent = 'Not Blocking';
        }

        // Update stats
        document.getElementById('blocks-today').textContent = blocksToday;
        document.getElementById('domain-count').textContent = blockedDomains.length;

    } catch (error) {
        console.error('Error loading status:', error);
    }
}

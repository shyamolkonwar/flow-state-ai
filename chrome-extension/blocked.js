// Blocked page script

document.addEventListener('DOMContentLoaded', () => {
    // Get blocked domain from URL
    const params = new URLSearchParams(window.location.search);
    const domain = params.get('domain') || 'this site';

    document.getElementById('blocked-domain').textContent = domain;

    // Load stats
    loadStats();

    // Event listeners
    document.getElementById('whitelist-btn').addEventListener('click', whitelistSite);
    document.getElementById('pause-btn').addEventListener('click', pauseProtection);
});

async function loadStats() {
    try {
        const result = await chrome.storage.local.get(['blocksToday']);
        const blocksToday = result.blocksToday || 0;
        document.getElementById('block-count').textContent = blocksToday;
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

async function whitelistSite() {
    const params = new URLSearchParams(window.location.search);
    const domain = params.get('domain');

    if (!domain) return;

    const confirmed = confirm(`Add ${domain} to whitelist?\n\nThis site will no longer be blocked during flow states.`);

    if (confirmed) {
        try {
            // Get current whitelist
            const result = await chrome.storage.local.get(['whitelist']);
            const whitelist = result.whitelist || [];

            // Add domain if not already there
            if (!whitelist.includes(domain)) {
                whitelist.push(domain);
                await chrome.storage.local.set({ whitelist });

                // TODO: Notify agent via native messaging
                console.log('Added to whitelist:', domain);

                // Reload page to unblock
                window.location.href = `https://${domain}`;
            }
        } catch (error) {
            console.error('Error whitelisting site:', error);
            alert('Failed to whitelist site. Please try again.');
        }
    }
}

async function pauseProtection() {
    const confirmed = confirm('Pause protection for 10 minutes?\n\nAll blocked sites will be accessible during this time.');

    if (confirmed) {
        try {
            // TODO: Send pause command to agent
            console.log('Pausing protection for 10 minutes');

            // For now, just disable blocking
            const background = chrome.extension.getBackgroundPage();
            if (background && background.disableBlocking) {
                await background.disableBlocking();

                // Re-enable after 10 minutes
                setTimeout(() => {
                    // TODO: Re-enable blocking
                    console.log('Re-enabling protection');
                }, 10 * 60 * 1000);

                // Go back
                window.history.back();
            }
        } catch (error) {
            console.error('Error pausing protection:', error);
            alert('Failed to pause protection. Please try again.');
        }
    }
}

// FlowFacilitator Chrome Extension - Background Service Worker

let isBlocking = false;
let blockedDomains = [];
let blockingRuleIds = [];

// Listen for messages from native host (agent)
chrome.runtime.onMessageExternal.addListener((message, sender, sendResponse) => {
    console.log('Received message from agent:', message);

    if (message.cmd === 'enable_blocking') {
        enableBlocking(message.domains);
        sendResponse({ status: 'success', rules_added: message.domains.length });
    } else if (message.cmd === 'disable_blocking') {
        disableBlocking();
        sendResponse({ status: 'success' });
    } else if (message.cmd === 'update_blocklist') {
        updateBlocklist(message.domains);
        sendResponse({ status: 'success', total_domains: message.domains.length });
    }

    return true; // Keep channel open for async response
});

// Enable blocking for specified domains
async function enableBlocking(domains) {
    console.log('Enabling blocking for:', domains);

    blockedDomains = domains;
    isBlocking = true;

    // Create blocking rules
    const rules = domains.map((domain, index) => ({
        id: index + 1,
        priority: 1,
        action: {
            type: 'redirect',
            redirect: {
                url: chrome.runtime.getURL('blocked.html') + '?domain=' + encodeURIComponent(domain)
            }
        },
        condition: {
            urlFilter: `*://*.${domain}/*`,
            resourceTypes: ['main_frame']
        }
    }));

    try {
        // Remove existing rules first
        const existingRules = await chrome.declarativeNetRequest.getDynamicRules();
        const existingIds = existingRules.map(rule => rule.id);

        await chrome.declarativeNetRequest.updateDynamicRules({
            removeRuleIds: existingIds,
            addRules: rules
        });

        blockingRuleIds = rules.map(r => r.id);

        // Update icon
        chrome.action.setIcon({ path: 'icons/icon-blocking.png' });
        chrome.action.setBadgeText({ text: 'ON' });
        chrome.action.setBadgeBackgroundColor({ color: '#10b981' });

        // Save state
        chrome.storage.local.set({ isBlocking: true, blockedDomains: domains });

        console.log('Blocking enabled successfully');
    } catch (error) {
        console.error('Error enabling blocking:', error);
    }
}

// Disable blocking
async function disableBlocking() {
    console.log('Disabling blocking');

    isBlocking = false;

    try {
        // Remove all dynamic rules
        await chrome.declarativeNetRequest.updateDynamicRules({
            removeRuleIds: blockingRuleIds
        });

        blockingRuleIds = [];

        // Update icon
        chrome.action.setIcon({ path: 'icons/icon16.png' });
        chrome.action.setBadgeText({ text: '' });

        // Save state
        chrome.storage.local.set({ isBlocking: false });

        console.log('Blocking disabled successfully');
    } catch (error) {
        console.error('Error disabling blocking:', error);
    }
}

// Update blocklist
async function updateBlocklist(domains) {
    console.log('Updating blocklist:', domains);

    blockedDomains = domains;

    // If currently blocking, update the rules
    if (isBlocking) {
        await enableBlocking(domains);
    }

    // Save to storage
    chrome.storage.local.set({ blockedDomains: domains });
}

// Track block attempts
chrome.declarativeNetRequest.onRuleMatchedDebug.addListener((details) => {
    console.log('Rule matched:', details);

    // Log block attempt
    const url = new URL(details.request.url);
    const domain = url.hostname;

    // Increment block count
    chrome.storage.local.get(['blocksToday', 'lastReset'], (result) => {
        const today = new Date().toDateString();
        let blocksToday = result.blocksToday || 0;
        const lastReset = result.lastReset || '';

        // Reset if new day
        if (lastReset !== today) {
            blocksToday = 0;
        }

        blocksToday++;

        chrome.storage.local.set({
            blocksToday: blocksToday,
            lastReset: today
        });

        // TODO: Send block attempt to agent via native messaging
        console.log('Block attempt:', domain, 'Total today:', blocksToday);
    });
});

// Restore state on startup
chrome.runtime.onStartup.addListener(() => {
    chrome.storage.local.get(['isBlocking', 'blockedDomains'], (result) => {
        if (result.isBlocking && result.blockedDomains) {
            enableBlocking(result.blockedDomains);
        }
    });
});

// Initialize on install
chrome.runtime.onInstalled.addListener(() => {
    console.log('FlowFacilitator Helper installed');

    // Set default values
    chrome.storage.local.set({
        isBlocking: false,
        blockedDomains: [],
        whitelist: [],
        blocksToday: 0,
        lastReset: new Date().toDateString()
    });
});

console.log('FlowFacilitator Helper background script loaded');

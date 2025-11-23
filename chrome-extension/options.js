// FlowFacilitator Options Page Script

document.addEventListener('DOMContentLoaded', () => {
    loadSettings();
    setupEventListeners();
});

function setupEventListeners() {
    document.getElementById('save-settings').addEventListener('click', saveSettings);
}

async function loadSettings() {
    try {
        const result = await chrome.storage.sync.get([
            'enableBlocking',
            'showNotifications',
            'autoStart',
            'sessionReminders',
            'analytics',
            'syncData'
        ]);

        // Set default values if not set
        document.getElementById('enable-blocking').checked = result.enableBlocking !== false;
        document.getElementById('show-notifications').checked = result.showNotifications !== false;
        document.getElementById('auto-start').checked = result.autoStart !== false;
        document.getElementById('session-reminders').checked = result.sessionReminders !== false;
        document.getElementById('analytics').checked = result.analytics !== false;
        document.getElementById('sync-data').checked = result.syncData !== false;

    } catch (error) {
        console.error('Error loading settings:', error);
        showStatus('Error loading settings', 'error');
    }
}

async function saveSettings() {
    const saveBtn = document.getElementById('save-settings');
    const originalText = saveBtn.textContent;

    saveBtn.textContent = 'Saving...';
    saveBtn.disabled = true;

    try {
        const settings = {
            enableBlocking: document.getElementById('enable-blocking').checked,
            showNotifications: document.getElementById('show-notifications').checked,
            autoStart: document.getElementById('auto-start').checked,
            sessionReminders: document.getElementById('session-reminders').checked,
            analytics: document.getElementById('analytics').checked,
            syncData: document.getElementById('sync-data').checked
        };

        await chrome.storage.sync.set(settings);
        showStatus('Settings saved successfully!', 'success');

    } catch (error) {
        console.error('Error saving settings:', error);
        showStatus('Error saving settings', 'error');
    } finally {
        saveBtn.textContent = originalText;
        saveBtn.disabled = false;
    }
}

function showStatus(message, type) {
    const statusEl = document.getElementById('save-status');
    statusEl.textContent = message;
    statusEl.className = `save-status ${type}`;
    statusEl.style.display = 'block';

    // Hide after 3 seconds
    setTimeout(() => {
        statusEl.style.display = 'none';
    }, 3000);
}

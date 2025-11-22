import { useState, useEffect } from 'react'
import { supabase } from '../lib/api'

export default function Settings() {
    const [flowConfig, setFlowConfig] = useState(null)
    const [blocklist, setBlocklist] = useState([])
    const [loading, setLoading] = useState(true)
    const [saving, setSaving] = useState(false)

    useEffect(() => {
        loadSettings()
    }, [])

    async function loadSettings() {
        try {
            // Load flow detection config
            const { data: flowData } = await supabase
                .from('settings')
                .select('value')
                .eq('key', 'flow_detection')
                .single()

            if (flowData) {
                setFlowConfig(flowData.value)
            }

            // Load blocklist
            const { data: blocklistData } = await supabase
                .from('settings')
                .select('value')
                .eq('key', 'blocklist')
                .single()

            if (blocklistData && blocklistData.value.domains) {
                setBlocklist(blocklistData.value.domains)
            }
        } catch (error) {
            console.error('Error loading settings:', error)
        } finally {
            setLoading(false)
        }
    }

    async function saveSettings() {
        setSaving(true)
        try {
            // Save flow config
            await supabase.rpc('upsert_setting', {
                p_user_id: 'local_user',
                p_key: 'flow_detection',
                p_value: flowConfig
            })

            // Save blocklist
            await supabase.rpc('upsert_setting', {
                p_user_id: 'local_user',
                p_key: 'blocklist',
                p_value: { domains: blocklist }
            })

            alert('Settings saved successfully!')
        } catch (error) {
            console.error('Error saving settings:', error)
            alert('Failed to save settings')
        } finally {
            setSaving(false)
        }
    }

    if (loading) {
        return (
            <div style={{ display: 'flex', justifyContent: 'center', padding: '64px' }}>
                <div className="spinner"></div>
            </div>
        )
    }

    return (
        <div>
            <div style={{ marginBottom: '32px' }}>
                <h1 style={{ fontSize: '32px', fontWeight: '700', marginBottom: '8px' }}>
                    Settings
                </h1>
                <p style={{ color: '#6b7280' }}>
                    Configure flow detection and blocklist
                </p>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                {/* Flow Detection Settings */}
                <div className="card">
                    <h2 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '16px' }}>
                        Flow Detection Thresholds
                    </h2>

                    {flowConfig && (
                        <div style={{ display: 'grid', gap: '16px' }}>
                            <div>
                                <label>Minimum Typing Rate (kpm)</label>
                                <input
                                    type="number"
                                    value={flowConfig.entry.typing_rate_min}
                                    onChange={(e) => setFlowConfig({
                                        ...flowConfig,
                                        entry: { ...flowConfig.entry, typing_rate_min: parseInt(e.target.value) }
                                    })}
                                />
                            </div>

                            <div>
                                <label>Max App Switches (per 5 min)</label>
                                <input
                                    type="number"
                                    value={flowConfig.entry.app_switches_max}
                                    onChange={(e) => setFlowConfig({
                                        ...flowConfig,
                                        entry: { ...flowConfig.entry, app_switches_max: parseInt(e.target.value) }
                                    })}
                                />
                            </div>

                            <div>
                                <label>Max Idle Gap (seconds)</label>
                                <input
                                    type="number"
                                    value={flowConfig.entry.max_idle_gap_seconds}
                                    onChange={(e) => setFlowConfig({
                                        ...flowConfig,
                                        entry: { ...flowConfig.entry, max_idle_gap_seconds: parseInt(e.target.value) }
                                    })}
                                />
                            </div>

                            <div>
                                <label>Entry Window (seconds)</label>
                                <input
                                    type="number"
                                    value={flowConfig.entry.window_seconds}
                                    onChange={(e) => setFlowConfig({
                                        ...flowConfig,
                                        entry: { ...flowConfig.entry, window_seconds: parseInt(e.target.value) }
                                    })}
                                />
                            </div>
                        </div>
                    )}
                </div>

                {/* Blocklist */}
                <div className="card">
                    <h2 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '16px' }}>
                        Blocklist
                    </h2>
                    <p style={{ fontSize: '14px', color: '#6b7280', marginBottom: '16px' }}>
                        Domains to block during flow states (one per line)
                    </p>
                    <textarea
                        rows="10"
                        value={blocklist.join('\n')}
                        onChange={(e) => setBlocklist(e.target.value.split('\n').filter(d => d.trim()))}
                        placeholder="youtube.com&#10;reddit.com&#10;twitter.com"
                    />
                </div>

                {/* Save Button */}
                <div>
                    <button
                        className="button button-primary"
                        onClick={saveSettings}
                        disabled={saving}
                        style={{ minWidth: '150px' }}
                    >
                        {saving ? 'Saving...' : 'Save Settings'}
                    </button>
                </div>

                {/* Danger Zone */}
                <div className="card" style={{ borderLeft: '4px solid #ef4444' }}>
                    <h2 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '16px', color: '#ef4444' }}>
                        Danger Zone
                    </h2>
                    <p style={{ fontSize: '14px', color: '#6b7280', marginBottom: '16px' }}>
                        Permanently delete all your data. This action cannot be undone.
                    </p>
                    <button
                        className="button button-danger"
                        onClick={() => {
                            if (confirm('Are you sure you want to delete ALL data? This cannot be undone!')) {
                                // TODO: Implement delete all data
                                alert('Delete all data functionality coming soon')
                            }
                        }}
                    >
                        Delete All Data
                    </button>
                </div>
            </div>
        </div>
    )
}

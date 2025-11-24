import { useState, useEffect } from 'react'
import { supabase } from '../lib/api'
import { useAuth } from '../lib/AuthContext'

export default function Settings() {
    const { user } = useAuth()
    const [flowConfig, setFlowConfig] = useState(null)
    const [blocklist, setBlocklist] = useState([])
    const [loading, setLoading] = useState(true)
    const [saving, setSaving] = useState(false)

    useEffect(() => {
        if (user) {
            loadSettings()
        }
    }, [user])

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
        if (!user) {
            alert('You must be logged in to save settings')
            return
        }

        setSaving(true)
        try {
            // Save flow config
            await supabase.rpc('upsert_setting', {
                p_user_id: user.id,
                p_key: 'flow_detection',
                p_value: flowConfig
            })

            // Save blocklist
            await supabase.rpc('upsert_setting', {
                p_user_id: user.id,
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
            <div style={{ marginBottom: '48px' }}>
                <h1 className="headline" style={{
                    fontSize: '42px',
                    background: 'linear-gradient(135deg, var(--prism-cyan), var(--hyper-teal))',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    backgroundClip: 'text',
                    marginBottom: '12px',
                    letterSpacing: '0.02em'
                }}>
                    Crystal Settings ⚙️
                </h1>
                <p className="body-text" style={{
                    fontSize: '18px',
                    color: 'rgba(255, 255, 255, 0.7)',
                    marginBottom: '8px'
                }}>
                    Tune your flow detection parameters
                </p>
                <div style={{
                    width: '80px',
                    height: '3px',
                    background: 'linear-gradient(90deg, var(--prism-cyan), var(--hyper-teal))',
                    borderRadius: '2px'
                }}></div>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
                {/* Flow Detection Settings */}
                <div className="glass-card">
                    <div style={{
                        marginBottom: '24px',
                        paddingBottom: '16px',
                        borderBottom: '1px solid rgba(255, 255, 255, 0.1)'
                    }}>
                        <h2 className="headline" style={{
                            fontSize: '24px',
                            color: 'var(--prism-cyan)',
                            marginBottom: '8px',
                            letterSpacing: '0.02em'
                        }}>
                            Flow Detection Parameters
                        </h2>
                        <p className="body-text" style={{
                            fontSize: '14px',
                            color: 'rgba(255, 255, 255, 0.6)'
                        }}>
                            Fine-tune how FlowFacilitator detects your optimal focus states
                        </p>
                    </div>

                    {flowConfig && (
                        <div style={{ display: 'grid', gap: '20px' }}>
                            <div style={{
                                padding: '20px',
                                background: 'rgba(255, 255, 255, 0.03)',
                                borderRadius: '12px',
                                border: '1px solid rgba(255, 255, 255, 0.08)'
                            }}>
                                <label className="body-text" style={{
                                    display: 'block',
                                    fontSize: '14px',
                                    fontWeight: '600',
                                    color: 'var(--hyper-teal)',
                                    marginBottom: '12px'
                                }}>
                                    Minimum Typing Rate (kpm)
                                </label>
                                <input
                                    type="number"
                                    value={flowConfig.entry.typing_rate_min}
                                    onChange={(e) => setFlowConfig({
                                        ...flowConfig,
                                        entry: { ...flowConfig.entry, typing_rate_min: parseInt(e.target.value) }
                                    })}
                                    className="glow-focus"
                                    style={{
                                        width: '100%',
                                        padding: '12px 16px',
                                        background: 'rgba(255, 255, 255, 0.05)',
                                        border: '1px solid rgba(255, 255, 255, 0.2)',
                                        borderRadius: '8px',
                                        color: 'var(--crystal-white)',
                                        fontSize: '16px',
                                        outline: 'none'
                                    }}
                                />
                                <p className="body-text" style={{
                                    fontSize: '12px',
                                    color: 'rgba(255, 255, 255, 0.5)',
                                    marginTop: '8px'
                                }}>
                                    Characters per minute threshold to enter flow state
                                </p>
                            </div>

                            <div style={{
                                padding: '20px',
                                background: 'rgba(255, 255, 255, 0.03)',
                                borderRadius: '12px',
                                border: '1px solid rgba(255, 255, 255, 0.08)'
                            }}>
                                <label className="body-text" style={{
                                    display: 'block',
                                    fontSize: '14px',
                                    fontWeight: '600',
                                    color: 'var(--aurora-magenta)',
                                    marginBottom: '12px'
                                }}>
                                    Max App Switches (per 5 min)
                                </label>
                                <input
                                    type="number"
                                    value={flowConfig.entry.app_switches_max}
                                    onChange={(e) => setFlowConfig({
                                        ...flowConfig,
                                        entry: { ...flowConfig.entry, app_switches_max: parseInt(e.target.value) }
                                    })}
                                    className="glow-focus"
                                    style={{
                                        width: '100%',
                                        padding: '12px 16px',
                                        background: 'rgba(255, 255, 255, 0.05)',
                                        border: '1px solid rgba(255, 255, 255, 0.2)',
                                        borderRadius: '8px',
                                        color: 'var(--crystal-white)',
                                        fontSize: '16px',
                                        outline: 'none'
                                    }}
                                />
                                <p className="body-text" style={{
                                    fontSize: '12px',
                                    color: 'rgba(255, 255, 255, 0.5)',
                                    marginTop: '8px'
                                }}>
                                    Maximum application switches allowed in flow state
                                </p>
                            </div>

                            <div style={{
                                padding: '20px',
                                background: 'rgba(255, 255, 255, 0.03)',
                                borderRadius: '12px',
                                border: '1px solid rgba(255, 255, 255, 0.08)'
                            }}>
                                <label className="body-text" style={{
                                    display: 'block',
                                    fontSize: '14px',
                                    fontWeight: '600',
                                    color: 'var(--solar-gold)',
                                    marginBottom: '12px'
                                }}>
                                    Max Idle Gap (seconds)
                                </label>
                                <input
                                    type="number"
                                    value={flowConfig.entry.max_idle_gap_seconds}
                                    onChange={(e) => setFlowConfig({
                                        ...flowConfig,
                                        entry: { ...flowConfig.entry, max_idle_gap_seconds: parseInt(e.target.value) }
                                    })}
                                    className="glow-focus"
                                    style={{
                                        width: '100%',
                                        padding: '12px 16px',
                                        background: 'rgba(255, 255, 255, 0.05)',
                                        border: '1px solid rgba(255, 255, 255, 0.2)',
                                        borderRadius: '8px',
                                        color: 'var(--crystal-white)',
                                        fontSize: '16px',
                                        outline: 'none'
                                    }}
                                />
                                <p className="body-text" style={{
                                    fontSize: '12px',
                                    color: 'rgba(255, 255, 255, 0.5)',
                                    marginTop: '8px'
                                }}>
                                    Maximum idle time allowed before exiting flow state
                                </p>
                            </div>

                            <div style={{
                                padding: '20px',
                                background: 'rgba(255, 255, 255, 0.03)',
                                borderRadius: '12px',
                                border: '1px solid rgba(255, 255, 255, 0.08)'
                            }}>
                                <label className="body-text" style={{
                                    display: 'block',
                                    fontSize: '14px',
                                    fontWeight: '600',
                                    color: 'var(--green-flash)',
                                    marginBottom: '12px'
                                }}>
                                    Entry Window (seconds)
                                </label>
                                <input
                                    type="number"
                                    value={flowConfig.entry.window_seconds}
                                    onChange={(e) => setFlowConfig({
                                        ...flowConfig,
                                        entry: { ...flowConfig.entry, window_seconds: parseInt(e.target.value) }
                                    })}
                                    className="glow-focus"
                                    style={{
                                        width: '100%',
                                        padding: '12px 16px',
                                        background: 'rgba(255, 255, 255, 0.05)',
                                        border: '1px solid rgba(255, 255, 255, 0.2)',
                                        borderRadius: '8px',
                                        color: 'var(--crystal-white)',
                                        fontSize: '16px',
                                        outline: 'none'
                                    }}
                                />
                                <p className="body-text" style={{
                                    fontSize: '12px',
                                    color: 'rgba(255, 255, 255, 0.5)',
                                    marginTop: '8px'
                                }}>
                                    Time window to analyze for flow state entry
                                </p>
                            </div>
                        </div>
                    )}
                </div>

                {/* Blocklist */}
                <div className="glass-card">
                    <div style={{
                        marginBottom: '24px',
                        paddingBottom: '16px',
                        borderBottom: '1px solid rgba(255, 255, 255, 0.1)'
                    }}>
                        <h2 className="headline" style={{
                            fontSize: '24px',
                            color: 'var(--flare-orange)',
                            marginBottom: '8px',
                            letterSpacing: '0.02em'
                        }}>
                            Distraction Blocklist
                        </h2>
                        <p className="body-text" style={{
                            fontSize: '14px',
                            color: 'rgba(255, 255, 255, 0.6)'
                        }}>
                            Websites blocked during flow states to maintain crystal-clear focus
                        </p>
                    </div>

                    <textarea
                        rows="8"
                        value={blocklist.join('\n')}
                        onChange={(e) => setBlocklist(e.target.value.split('\n').filter(d => d.trim()))}
                        className="glow-focus"
                        placeholder="youtube.com&#10;reddit.com&#10;twitter.com&#10;facebook.com"
                        style={{
                            width: '100%',
                            padding: '16px',
                            background: 'rgba(255, 255, 255, 0.05)',
                            border: '1px solid rgba(255, 255, 255, 0.2)',
                            borderRadius: '12px',
                            color: 'var(--crystal-white)',
                            fontSize: '14px',
                            fontFamily: 'inherit',
                            outline: 'none',
                            resize: 'vertical',
                            lineHeight: '1.5'
                        }}
                    />
                    <p className="body-text" style={{
                        fontSize: '12px',
                        color: 'rgba(255, 255, 255, 0.5)',
                        marginTop: '8px'
                    }}>
                        Enter one domain per line. These sites will be blocked during your flow sessions.
                    </p>
                </div>

                {/* Save Button */}
                <div style={{ textAlign: 'center', marginTop: '16px' }}>
                    <button
                        className="button crystal-hover"
                        onClick={saveSettings}
                        disabled={saving}
                        style={{
                            padding: '16px 32px',
                            background: 'linear-gradient(135deg, var(--prism-cyan), var(--hyper-teal))',
                            border: 'none',
                            borderRadius: '12px',
                            color: 'var(--deep-night)',
                            fontSize: '16px',
                            fontWeight: '600',
                            cursor: saving ? 'not-allowed' : 'pointer',
                            minWidth: '200px'
                        }}
                    >
                        {saving ? '💎 Saving Crystal Settings...' : '💎 Save Settings'}
                    </button>
                </div>

                {/* Danger Zone */}
                <div className="glass-card" style={{
                    border: '1px solid rgba(255, 99, 71, 0.3)',
                    background: 'rgba(255, 99, 71, 0.05)'
                }}>
                    <div style={{
                        marginBottom: '20px',
                        paddingBottom: '16px',
                        borderBottom: '1px solid rgba(255, 99, 71, 0.2)'
                    }}>
                        <h2 className="headline" style={{
                            fontSize: '20px',
                            color: '#FF6347',
                            marginBottom: '8px',
                            letterSpacing: '0.02em'
                        }}>
                            ⚠️ Danger Zone
                        </h2>
                        <p className="body-text" style={{
                            fontSize: '14px',
                            color: 'rgba(255, 99, 71, 0.8)'
                        }}>
                            Irreversible actions that will permanently alter your crystal data
                        </p>
                    </div>

                    <button
                        className="button crystal-hover"
                        onClick={() => {
                            if (confirm('Are you sure you want to delete ALL data? This cannot be undone!')) {
                                // TODO: Implement delete all data
                                alert('Delete all data functionality coming soon')
                            }
                        }}
                        style={{
                            width: '100%',
                            padding: '14px 20px',
                            background: 'rgba(255, 99, 71, 0.1)',
                            border: '1px solid rgba(255, 99, 71, 0.3)',
                            borderRadius: '8px',
                            color: '#FF6347',
                            fontSize: '14px',
                            fontWeight: '500',
                            cursor: 'pointer'
                        }}
                    >
                        🗑️ Delete All Crystal Data
                    </button>
                </div>
            </div>
        </div>
    )
}

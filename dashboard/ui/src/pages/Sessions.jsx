import { useState, useEffect } from 'react'
import { supabase } from '../lib/api'
import { format } from 'date-fns'

export default function Sessions() {
    const [sessions, setSessions] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        loadSessions()
    }, [])

    async function loadSessions() {
        try {
            const { data, error } = await supabase
                .from('sessions')
                .select('*')
                .not('end_ts', 'is', null)
                .order('start_ts', { ascending: false })
                .limit(50)

            if (error) throw error
            setSessions(data || [])
        } catch (error) {
            console.error('Error loading sessions:', error)
        } finally {
            setLoading(false)
        }
    }

    function formatDuration(seconds) {
        if (!seconds) return '0m'
        const minutes = Math.floor(seconds / 60)
        const hours = Math.floor(minutes / 60)
        const remainingMinutes = minutes % 60

        if (hours > 0) {
            return `${hours}h ${remainingMinutes}m`
        }
        return `${minutes}m`
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
                    Flow Sessions ✨
                </h1>
                <p className="body-text" style={{
                    fontSize: '18px',
                    color: 'rgba(255, 255, 255, 0.7)',
                    marginBottom: '8px'
                }}>
                    Crystal-clear history of your focus journey
                </p>
                <div style={{
                    width: '80px',
                    height: '3px',
                    background: 'linear-gradient(90deg, var(--prism-cyan), var(--hyper-teal))',
                    borderRadius: '2px'
                }}></div>
            </div>

            {/* Session Stats Overview */}
            {sessions.length > 0 && (
                <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
                    gap: '32px',
                    marginBottom: '48px'
                }}>
                    <div className="glass-card crystal-hover" style={{
                        position: 'relative',
                        overflow: 'hidden'
                    }}>
                        <div style={{
                            position: 'absolute',
                            top: '20px',
                            right: '20px',
                            width: '40px',
                            height: '40px',
                            background: 'linear-gradient(135deg, var(--prism-cyan), var(--hyper-teal))',
                            borderRadius: '50%',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            fontSize: '20px'
                        }}>
                            📊
                        </div>
                        <div className="numeric" style={{
                            fontSize: '48px',
                            fontWeight: '700',
                            color: 'var(--prism-cyan)',
                            marginBottom: '8px'
                        }}>
                            {sessions.length}
                        </div>
                        <div className="body-text" style={{
                            fontSize: '16px',
                            color: 'rgba(255, 255, 255, 0.7)',
                            textTransform: 'uppercase',
                            letterSpacing: '0.5px',
                            fontWeight: '500'
                        }}>
                            Total Flow Sessions
                        </div>
                        <div style={{
                            position: 'absolute',
                            bottom: '20px',
                            left: '20px',
                            width: '60px',
                            height: '3px',
                            background: 'linear-gradient(90deg, var(--prism-cyan), var(--hyper-teal))',
                            borderRadius: '2px'
                        }}></div>
                    </div>

                    <div className="glass-card crystal-hover" style={{
                        position: 'relative',
                        overflow: 'hidden'
                    }}>
                        <div style={{
                            position: 'absolute',
                            top: '20px',
                            right: '20px',
                            width: '40px',
                            height: '40px',
                            background: 'linear-gradient(135deg, var(--hyper-teal), var(--aurora-magenta))',
                            borderRadius: '50%',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            fontSize: '20px'
                        }}>
                            ⏱️
                        </div>
                        <div className="numeric" style={{
                            fontSize: '48px',
                            fontWeight: '700',
                            color: 'var(--hyper-teal)',
                            marginBottom: '8px'
                        }}>
                            {formatDuration(sessions.reduce((sum, s) => sum + (s.duration_seconds || 0), 0))}
                        </div>
                        <div className="body-text" style={{
                            fontSize: '16px',
                            color: 'rgba(255, 255, 255, 0.7)',
                            textTransform: 'uppercase',
                            letterSpacing: '0.5px',
                            fontWeight: '500'
                        }}>
                            Total Flow Time
                        </div>
                        <div style={{
                            position: 'absolute',
                            bottom: '20px',
                            left: '20px',
                            width: '60px',
                            height: '3px',
                            background: 'linear-gradient(90deg, var(--hyper-teal), var(--aurora-magenta))',
                            borderRadius: '2px'
                        }}></div>
                    </div>

                    <div className="glass-card crystal-hover" style={{
                        position: 'relative',
                        overflow: 'hidden'
                    }}>
                        <div style={{
                            position: 'absolute',
                            top: '20px',
                            right: '20px',
                            width: '40px',
                            height: '40px',
                            background: 'linear-gradient(135deg, var(--solar-gold), var(--flare-orange))',
                            borderRadius: '50%',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            fontSize: '20px'
                        }}>
                            🏆
                        </div>
                        <div className="numeric" style={{
                            fontSize: '48px',
                            fontWeight: '700',
                            color: 'var(--solar-gold)',
                            marginBottom: '8px'
                        }}>
                            {formatDuration(Math.max(...sessions.map(s => s.duration_seconds || 0), 0))}
                        </div>
                        <div className="body-text" style={{
                            fontSize: '16px',
                            color: 'rgba(255, 255, 255, 0.7)',
                            textTransform: 'uppercase',
                            letterSpacing: '0.5px',
                            fontWeight: '500'
                        }}>
                            Longest Session
                        </div>
                        <div style={{
                            position: 'absolute',
                            bottom: '20px',
                            left: '20px',
                            width: '60px',
                            height: '3px',
                            background: 'linear-gradient(90deg, var(--solar-gold), var(--flare-orange))',
                            borderRadius: '2px'
                        }}></div>
                    </div>
                </div>
            )}

            {/* Sessions List */}
            <div className="glass-card">
                {sessions.length === 0 ? (
                    <div style={{
                        textAlign: 'center',
                        padding: '80px 40px',
                        color: 'rgba(255, 255, 255, 0.6)'
                    }}>
                        <div style={{
                            fontSize: '64px',
                            marginBottom: '24px',
                            opacity: '0.3'
                        }}>
                            💎
                        </div>
                        <h3 className="headline" style={{
                            fontSize: '24px',
                            color: 'var(--prism-cyan)',
                            marginBottom: '12px'
                        }}>
                            No Flow Sessions Yet
                        </h3>
                        <p className="body-text" style={{
                            fontSize: '16px',
                            color: 'rgba(255, 255, 255, 0.5)'
                        }}>
                            Start your focus journey to see your crystal-clear session history
                        </p>
                    </div>
                ) : (
                    <div>
                        <div style={{
                            marginBottom: '32px',
                            paddingBottom: '20px',
                            borderBottom: '1px solid rgba(255, 255, 255, 0.1)'
                        }}>
                            <h2 className="headline" style={{
                                fontSize: '28px',
                                color: 'var(--crystal-white)',
                                marginBottom: '8px',
                                letterSpacing: '0.02em'
                            }}>
                                Session Timeline
                            </h2>
                            <p className="body-text" style={{
                                fontSize: '16px',
                                color: 'rgba(255, 255, 255, 0.6)'
                            }}>
                                Your flow state journey, crystal by crystal
                            </p>
                        </div>

                        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                            {sessions.map((session, index) => (
                                <div
                                    key={session.id}
                                    className="crystal-hover"
                                    style={{
                                        padding: '24px',
                                        background: 'rgba(255, 255, 255, 0.03)',
                                        borderRadius: '16px',
                                        border: '1px solid rgba(255, 255, 255, 0.08)',
                                        position: 'relative',
                                        overflow: 'hidden'
                                    }}
                                >
                                    {/* Timeline indicator */}
                                    <div style={{
                                        position: 'absolute',
                                        left: '24px',
                                        top: '24px',
                                        width: '12px',
                                        height: '12px',
                                        background: 'linear-gradient(135deg, var(--prism-cyan), var(--hyper-teal))',
                                        borderRadius: '50%',
                                        boxShadow: '0 0 12px rgba(77, 229, 255, 0.4)'
                                    }}></div>

                                    <div style={{
                                        display: 'grid',
                                        gridTemplateColumns: '1fr auto',
                                        gap: '24px',
                                        alignItems: 'center',
                                        marginLeft: '48px'
                                    }}>
                                        <div>
                                            <div style={{
                                                display: 'flex',
                                                alignItems: 'center',
                                                gap: '12px',
                                                marginBottom: '8px'
                                            }}>
                                                <div className="numeric" style={{
                                                    fontSize: '24px',
                                                    color: 'var(--prism-cyan)',
                                                    fontWeight: '600'
                                                }}>
                                                    {formatDuration(session.duration_seconds)}
                                                </div>
                                                <div style={{
                                                    padding: '4px 12px',
                                                    borderRadius: '12px',
                                                    fontSize: '12px',
                                                    fontWeight: '500',
                                                    background: session.trigger_reason === 'manual' ?
                                                        'rgba(124, 255, 207, 0.1)' :
                                                        'rgba(255, 198, 107, 0.1)',
                                                    color: session.trigger_reason === 'manual' ?
                                                        'var(--green-flash)' :
                                                        'var(--solar-gold)',
                                                    border: `1px solid ${session.trigger_reason === 'manual' ?
                                                        'rgba(124, 255, 207, 0.3)' :
                                                        'rgba(255, 198, 107, 0.3)'}`
                                                }}>
                                                    {session.trigger_reason || 'auto'}
                                                </div>
                                            </div>

                                            <div className="body-text" style={{
                                                fontSize: '14px',
                                                color: 'rgba(255, 255, 255, 0.6)',
                                                marginBottom: '4px'
                                            }}>
                                                {format(new Date(session.start_ts), 'EEEE, MMMM d, yyyy • h:mm a')}
                                            </div>

                                            <div style={{
                                                display: 'flex',
                                                gap: '16px',
                                                fontSize: '14px',
                                                color: 'rgba(255, 255, 255, 0.5)'
                                            }}>
                                                <span>📱 {session.start_app || 'Unknown App'}</span>
                                                {session.avg_typing_rate && (
                                                    <span>⌨️ {session.avg_typing_rate.toFixed(0)} kpm</span>
                                                )}
                                            </div>
                                        </div>

                                        {/* Progress bar visualization */}
                                        <div style={{
                                            width: '120px',
                                            height: '8px',
                                            background: 'rgba(255, 255, 255, 0.1)',
                                            borderRadius: '4px',
                                            overflow: 'hidden'
                                        }}>
                                            <div style={{
                                                width: `${Math.min((session.duration_seconds / 3600) * 100, 100)}%`,
                                                height: '100%',
                                                background: 'linear-gradient(90deg, var(--prism-cyan), var(--hyper-teal))',
                                                borderRadius: '4px',
                                                transition: 'width 0.3s ease'
                                            }}></div>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}

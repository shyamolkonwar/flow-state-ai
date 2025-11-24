import { useState, useEffect } from 'react'
import { supabase, agentAPI } from '../lib/api'
import { useAuth } from '../lib/AuthContext'

export default function Home() {
    const { user } = useAuth()
    const [stats, setStats] = useState({
        totalFlowTime: 0,
        sessionCount: 0,
        longestSession: 0,
        averageSession: 0
    })
    const [agentStatus, setAgentStatus] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        if (user) {
            loadTodayStats()
        }
        loadAgentStatus()

        // Refresh agent status every 5 seconds
        const interval = setInterval(loadAgentStatus, 5000)
        return () => clearInterval(interval)
    }, [user])

    async function loadAgentStatus() {
        try {
            const status = await agentAPI.getStatus()
            setAgentStatus(status)
        } catch (error) {
            console.error('Error loading agent status:', error)
        }
    }

    async function loadTodayStats() {
        try {
            const today = new Date()
            today.setHours(0, 0, 0, 0)

            const { data, error } = await supabase
                .from('sessions')
                .select('start_ts, end_ts')
                .eq('user_id', user.id)
                .gte('start_ts', today.toISOString())
                .not('end_ts', 'is', null)

            if (error) throw error

            // Calculate durations from timestamps
            const sessionsWithDuration = data.map(session => {
                const startTime = new Date(session.start_ts)
                const endTime = new Date(session.end_ts)
                const durationSeconds = Math.floor((endTime - startTime) / 1000)
                return { ...session, duration_seconds: durationSeconds }
            })

            const sessionCount = sessionsWithDuration.length
            const totalSeconds = sessionsWithDuration.reduce((sum, s) => sum + (s.duration_seconds || 0), 0)
            const longestSeconds = Math.max(...sessionsWithDuration.map(s => s.duration_seconds || 0), 0)
            const averageSeconds = sessionCount > 0 ? totalSeconds / sessionCount : 0

            setStats({
                totalFlowTime: Math.round(totalSeconds / 60), // minutes
                sessionCount,
                longestSession: Math.round(longestSeconds / 60), // minutes
                averageSession: Math.round(averageSeconds / 60) // minutes
            })
        } catch (error) {
            console.error('Error loading stats:', error)
        } finally {
            setLoading(false)
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
                    Welcome Back! ✨
                </h1>
                <p className="body-text" style={{
                    fontSize: '18px',
                    color: 'rgba(255, 255, 255, 0.7)',
                    marginBottom: '8px'
                }}>
                    Crystal clarity in your focus journey
                </p>
                <div style={{
                    width: '80px',
                    height: '3px',
                    background: 'linear-gradient(90deg, var(--prism-cyan), var(--hyper-teal))',
                    borderRadius: '2px'
                }}></div>
            </div>

            {/* Agent Status Banner */}
            {agentStatus && (
                <div className="glass-card crystal-hover" style={{
                    marginBottom: '32px',
                    border: agentStatus.flow_state === 'in_flow'
                        ? '1px solid rgba(124, 255, 207, 0.3)'
                        : '1px solid rgba(255, 255, 255, 0.1)',
                    position: 'relative',
                    overflow: 'hidden'
                }}>
                    <div style={{
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        width: '4px',
                        height: '100%',
                        background: agentStatus.flow_state === 'in_flow'
                            ? 'linear-gradient(180deg, var(--green-flash), var(--hyper-teal))'
                            : 'rgba(255, 255, 255, 0.2)'
                    }}></div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div>
                            <div className="body-text" style={{
                                fontSize: '14px',
                                fontWeight: '600',
                                color: 'rgba(255, 255, 255, 0.6)',
                                marginBottom: '8px',
                                textTransform: 'uppercase',
                                letterSpacing: '0.5px'
                            }}>
                                Current Flow State
                            </div>
                            <div className="headline" style={{
                                fontSize: '24px',
                                color: agentStatus.flow_state === 'in_flow'
                                    ? 'var(--green-flash)'
                                    : agentStatus.flow_state === 'working'
                                        ? 'var(--solar-gold)'
                                        : 'rgba(255, 255, 255, 0.7)'
                            }}>
                                {agentStatus.flow_state === 'in_flow' ? '💎 In Crystal Flow' :
                                    agentStatus.flow_state === 'working' ? '⚡ Focused Work' : '🌙 Resting'}
                            </div>
                        </div>
                        {agentStatus.flow_state === 'in_flow' && (
                            <div style={{ textAlign: 'right' }}>
                                <div className="body-text" style={{
                                    fontSize: '14px',
                                    color: 'rgba(255, 255, 255, 0.6)',
                                    marginBottom: '4px'
                                }}>
                                    Time in Flow
                                </div>
                                <div className="numeric" style={{
                                    fontSize: '32px',
                                    color: 'var(--green-flash)',
                                    fontWeight: '700'
                                }}>
                                    {Math.floor(agentStatus.time_in_state_seconds / 60)}m
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            )}

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
                        ⏱️
                    </div>
                    <div className="numeric" style={{
                        fontSize: '48px',
                        fontWeight: '700',
                        color: 'var(--prism-cyan)',
                        marginBottom: '8px'
                    }}>
                        {stats.totalFlowTime}m
                    </div>
                    <div className="body-text" style={{
                        fontSize: '16px',
                        color: 'rgba(255, 255, 255, 0.7)',
                        textTransform: 'uppercase',
                        letterSpacing: '0.5px',
                        fontWeight: '500'
                    }}>
                        Total Flow Time Today
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
                        📈
                    </div>
                    <div className="numeric" style={{
                        fontSize: '48px',
                        fontWeight: '700',
                        color: 'var(--hyper-teal)',
                        marginBottom: '8px'
                    }}>
                        {stats.sessionCount}
                    </div>
                    <div className="body-text" style={{
                        fontSize: '16px',
                        color: 'rgba(255, 255, 255, 0.7)',
                        textTransform: 'uppercase',
                        letterSpacing: '0.5px',
                        fontWeight: '500'
                    }}>
                        Flow Sessions Today
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
                        {stats.longestSession}m
                    </div>
                    <div className="body-text" style={{
                        fontSize: '16px',
                        color: 'rgba(255, 255, 255, 0.7)',
                        textTransform: 'uppercase',
                        letterSpacing: '0.5px',
                        fontWeight: '500'
                    }}>
                        Longest Crystal Session
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
                        background: 'linear-gradient(135deg, var(--aurora-magenta), var(--violet-edge))',
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
                        color: 'var(--aurora-magenta)',
                        marginBottom: '8px'
                    }}>
                        {stats.averageSession}m
                    </div>
                    <div className="body-text" style={{
                        fontSize: '16px',
                        color: 'rgba(255, 255, 255, 0.7)',
                        textTransform: 'uppercase',
                        letterSpacing: '0.5px',
                        fontWeight: '500'
                    }}>
                        Average Flow Depth
                    </div>
                    <div style={{
                        position: 'absolute',
                        bottom: '20px',
                        left: '20px',
                        width: '60px',
                        height: '3px',
                        background: 'linear-gradient(90deg, var(--aurora-magenta), var(--violet-edge))',
                        borderRadius: '2px'
                    }}></div>
                </div>
            </div>

            <div className="glass-card">
                <h2 className="headline" style={{
                    fontSize: '24px',
                    color: 'var(--crystal-white)',
                    marginBottom: '24px',
                    letterSpacing: '0.02em'
                }}>
                    Crystal Actions
                </h2>
                <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
                    <button className="button crystal-hover" style={{
                        padding: '14px 24px',
                        background: 'linear-gradient(135deg, var(--prism-cyan), var(--hyper-teal))',
                        color: 'var(--deep-night)',
                        border: 'none',
                        borderRadius: '12px',
                        fontSize: '16px',
                        fontWeight: '600',
                        cursor: 'pointer',
                        transition: 'all 0.3s ease',
                        position: 'relative',
                        overflow: 'hidden'
                    }} onClick={() => window.location.href = '/sessions'}>
                        View Flow Sessions
                    </button>
                    <button className="button crystal-hover" style={{
                        padding: '14px 24px',
                        background: 'rgba(255, 255, 255, 0.1)',
                        color: 'var(--crystal-white)',
                        border: '1px solid rgba(255, 255, 255, 0.2)',
                        borderRadius: '12px',
                        fontSize: '16px',
                        fontWeight: '600',
                        cursor: 'pointer',
                        transition: 'all 0.3s ease'
                    }} onClick={() => window.location.href = '/settings'}>
                        Tune Crystal Settings
                    </button>
                    <button className="button crystal-hover" style={{
                        padding: '14px 24px',
                        background: 'rgba(255, 255, 255, 0.1)',
                        color: 'var(--crystal-white)',
                        border: '1px solid rgba(255, 255, 255, 0.2)',
                        borderRadius: '12px',
                        fontSize: '16px',
                        fontWeight: '600',
                        cursor: 'pointer',
                        transition: 'all 0.3s ease'
                    }} onClick={() => window.location.href = '/gamification'}>
                        RPG Crystal Stats
                    </button>
                </div>
            </div>
        </div>
    )
}

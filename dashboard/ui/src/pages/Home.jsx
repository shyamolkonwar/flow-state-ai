import { useState, useEffect } from 'react'
import { supabase, agentAPI } from '../lib/api'

export default function Home() {
    const [stats, setStats] = useState({
        totalFlowTime: 0,
        sessionCount: 0,
        longestSession: 0,
        averageSession: 0
    })
    const [agentStatus, setAgentStatus] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        loadTodayStats()
        loadAgentStatus()

        // Refresh agent status every 5 seconds
        const interval = setInterval(loadAgentStatus, 5000)
        return () => clearInterval(interval)
    }, [])

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
                .select('duration_seconds')
                .gte('start_ts', today.toISOString())
                .not('end_ts', 'is', null)

            if (error) throw error

            const sessionCount = data.length
            const totalSeconds = data.reduce((sum, s) => sum + (s.duration_seconds || 0), 0)
            const longestSeconds = Math.max(...data.map(s => s.duration_seconds || 0), 0)
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
            <div style={{ marginBottom: '32px' }}>
                <h1 style={{ fontSize: '32px', fontWeight: '700', marginBottom: '8px' }}>
                    Welcome Back! 👋
                </h1>
                <p style={{ color: '#6b7280' }}>
                    Here's your focus summary for today
                </p>
            </div>

            {/* Agent Status Banner */}
            {agentStatus && (
                <div className="card" style={{
                    marginBottom: '24px',
                    background: agentStatus.flow_state === 'in_flow' ? '#d1fae5' : '#f3f4f6',
                    borderLeft: `4px solid ${agentStatus.flow_state === 'in_flow' ? '#10b981' : '#9ca3af'}`
                }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div>
                            <div style={{ fontSize: '14px', fontWeight: '600', color: '#6b7280', marginBottom: '4px' }}>
                                Current Status
                            </div>
                            <div style={{ fontSize: '20px', fontWeight: '700', color: agentStatus.flow_state === 'in_flow' ? '#065f46' : '#4b5563' }}>
                                {agentStatus.flow_state === 'in_flow' ? '🎯 In Flow' :
                                    agentStatus.flow_state === 'working' ? '⚡ Working' : '💤 Idle'}
                            </div>
                        </div>
                        {agentStatus.flow_state === 'in_flow' && (
                            <div style={{ textAlign: 'right' }}>
                                <div style={{ fontSize: '14px', color: '#6b7280' }}>Time in Flow</div>
                                <div style={{ fontSize: '24px', fontWeight: '700', color: '#065f46' }}>
                                    {Math.floor(agentStatus.time_in_state_seconds / 60)}m
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            )}

            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
                gap: '24px',
                marginBottom: '32px'
            }}>
                <div className="metric-card">
                    <div className="metric-icon">⏱️</div>
                    <div className="metric-value">{stats.totalFlowTime}m</div>
                    <div className="metric-label">Total Flow Time Today</div>
                </div>

                <div className="metric-card">
                    <div className="metric-icon">📈</div>
                    <div className="metric-value">{stats.sessionCount}</div>
                    <div className="metric-label">Sessions Today</div>
                </div>

                <div className="metric-card">
                    <div className="metric-icon">🏆</div>
                    <div className="metric-value">{stats.longestSession}m</div>
                    <div className="metric-label">Longest Session</div>
                </div>

                <div className="metric-card">
                    <div className="metric-icon">📊</div>
                    <div className="metric-value">{stats.averageSession}m</div>
                    <div className="metric-label">Average Session</div>
                </div>
            </div>

            <div className="card">
                <h2 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '16px' }}>
                    Quick Actions
                </h2>
                <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
                    <button className="button button-primary" onClick={() => window.location.href = '/sessions'}>
                        View All Sessions
                    </button>
                    <button className="button button-secondary" onClick={() => window.location.href = '/settings'}>
                        Adjust Settings
                    </button>
                    <button className="button button-secondary" onClick={() => window.location.href = '/gamification'}>
                        View RPG Stats
                    </button>
                </div>
            </div>
        </div>
    )
}

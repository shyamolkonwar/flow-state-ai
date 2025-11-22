import { useState, useEffect } from 'react'
import { supabase } from '../lib/api'

export default function Home() {
    const [stats, setStats] = useState({
        totalFlowTime: 0,
        sessionCount: 0,
        longestSession: 0,
        averageSession: 0
    })
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        loadTodayStats()
    }, [])

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
                    <button className="button button-primary">
                        View All Sessions
                    </button>
                    <button className="button button-secondary">
                        Adjust Settings
                    </button>
                    <button className="button button-secondary">
                        Export Data
                    </button>
                </div>
            </div>
        </div>
    )
}

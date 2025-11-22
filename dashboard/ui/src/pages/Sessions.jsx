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
            <div style={{ marginBottom: '32px' }}>
                <h1 style={{ fontSize: '32px', fontWeight: '700', marginBottom: '8px' }}>
                    Flow Sessions
                </h1>
                <p style={{ color: '#6b7280' }}>
                    Complete history of your flow states
                </p>
            </div>

            <div className="card">
                {sessions.length === 0 ? (
                    <div style={{ textAlign: 'center', padding: '64px', color: '#9ca3af' }}>
                        <div style={{ fontSize: '48px', marginBottom: '16px' }}>📊</div>
                        <p>No sessions yet. Start working to track your first flow session!</p>
                    </div>
                ) : (
                    <table>
                        <thead>
                            <tr>
                                <th>Start Time</th>
                                <th>Duration</th>
                                <th>App</th>
                                <th>Typing Rate</th>
                                <th>End Reason</th>
                            </tr>
                        </thead>
                        <tbody>
                            {sessions.map((session) => (
                                <tr key={session.id}>
                                    <td>
                                        {format(new Date(session.start_ts), 'MMM d, yyyy h:mm a')}
                                    </td>
                                    <td>
                                        <strong>{formatDuration(session.duration_seconds)}</strong>
                                    </td>
                                    <td>{session.start_app || 'Unknown'}</td>
                                    <td>{session.avg_typing_rate?.toFixed(0) || 0} kpm</td>
                                    <td>
                                        <span style={{
                                            padding: '4px 8px',
                                            borderRadius: '4px',
                                            fontSize: '12px',
                                            background: '#f3f4f6',
                                            color: '#4b5563'
                                        }}>
                                            {session.trigger_reason || 'unknown'}
                                        </span>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>
        </div>
    )
}

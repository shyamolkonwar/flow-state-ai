import { useState, useEffect } from 'react'
import { supabase } from '../lib/api'

export default function Gamification() {
    const [stats, setStats] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        loadStats()
    }, [])

    async function loadStats() {
        try {
            // Load gamification stats from settings
            const { data, error } = await supabase
                .from('settings')
                .select('value')
                .eq('key', 'gamification_stats')
                .single()

            if (error) throw error

            if (data && data.value) {
                setStats(data.value)
            }
        } catch (error) {
            console.error('Error loading gamification stats:', error)
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

    if (!stats) {
        return (
            <div className="card" style={{ textAlign: 'center', padding: '64px' }}>
                <div style={{ fontSize: '48px', marginBottom: '16px' }}>🎮</div>
                <p style={{ color: '#6b7280' }}>No stats available yet. Complete your first flow session!</p>
            </div>
        )
    }

    const { level, experience, next_level_xp, stamina, resilience, consistency, progressive_goal } = stats

    return (
        <div>
            <div style={{ marginBottom: '32px' }}>
                <h1 style={{ fontSize: '32px', fontWeight: '700', marginBottom: '8px' }}>
                    RPG Stats 🎮
                </h1>
                <p style={{ color: '#6b7280' }}>
                    Your focus journey, gamified
                </p>
            </div>

            {/* Level and XP */}
            <div className="card" style={{ marginBottom: '24px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                    <div>
                        <h2 style={{ fontSize: '24px', fontWeight: '700', color: '#667eea' }}>
                            Level {level}
                        </h2>
                        <p style={{ fontSize: '14px', color: '#6b7280' }}>
                            {experience} / {next_level_xp} XP
                        </p>
                    </div>
                    <div style={{ fontSize: '48px' }}>⭐</div>
                </div>

                {/* XP Progress Bar */}
                <div style={{
                    width: '100%',
                    height: '12px',
                    background: '#e5e7eb',
                    borderRadius: '6px',
                    overflow: 'hidden'
                }}>
                    <div style={{
                        width: `${(experience / next_level_xp) * 100}%`,
                        height: '100%',
                        background: 'linear-gradient(90deg, #667eea 0%, #764ba2 100%)',
                        transition: 'width 0.3s'
                    }}></div>
                </div>
            </div>

            {/* Stats Grid */}
            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
                gap: '24px',
                marginBottom: '32px'
            }}>
                {/* Stamina */}
                <div className="metric-card">
                    <div className="metric-icon">💪</div>
                    <div className="metric-value">{stamina.total_hours}h</div>
                    <div className="metric-label">Stamina (Total Flow Time)</div>
                    <div style={{ marginTop: '12px', fontSize: '14px', color: '#6b7280' }}>
                        <div>Avg: {stamina.average_session}m per session</div>
                        <div>Best: {stamina.personal_best}m</div>
                    </div>
                </div>

                {/* Resilience */}
                <div className="metric-card">
                    <div className="metric-icon">🛡️</div>
                    <div className="metric-value">{resilience.total}</div>
                    <div className="metric-label">Resilience (Distractions Resisted)</div>
                    <div style={{ marginTop: '12px' }}>
                        <span style={{
                            padding: '4px 12px',
                            borderRadius: '12px',
                            fontSize: '12px',
                            fontWeight: '600',
                            background: '#fef3c7',
                            color: '#92400e'
                        }}>
                            {resilience.rank} Rank
                        </span>
                    </div>
                </div>

                {/* Consistency */}
                <div className="metric-card">
                    <div className="metric-icon">🔥</div>
                    <div className="metric-value">{consistency.current_streak}</div>
                    <div className="metric-label">Consistency (Day Streak)</div>
                    <div style={{ marginTop: '12px', fontSize: '14px', color: '#6b7280' }}>
                        <div>Best Streak: {consistency.best_streak} days</div>
                    </div>
                </div>
            </div>

            {/* Progressive Goal */}
            <div className="card" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
                <h2 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '12px' }}>
                    🎯 Progressive Goal
                </h2>
                <p style={{ fontSize: '32px', fontWeight: '700', marginBottom: '8px' }}>
                    {progressive_goal} minutes
                </p>
                <p style={{ fontSize: '14px', opacity: 0.9 }}>
                    Your next target session duration. The system adapts to your performance!
                </p>
            </div>

            {/* Achievements Section */}
            <div className="card" style={{ marginTop: '24px' }}>
                <h2 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '16px' }}>
                    🏆 Achievements
                </h2>
                <div style={{ display: 'grid', gap: '12px' }}>
                    {stamina.total_hours >= 10 && (
                        <div style={{ padding: '12px', background: '#fef3c7', borderRadius: '8px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                            <span style={{ fontSize: '32px' }}>🏅</span>
                            <div>
                                <div style={{ fontWeight: '600', color: '#92400e' }}>10 Hour Club</div>
                                <div style={{ fontSize: '14px', color: '#78350f' }}>Accumulated 10+ hours of flow time</div>
                            </div>
                        </div>
                    )}

                    {resilience.total >= 25 && (
                        <div style={{ padding: '12px', background: '#d1fae5', borderRadius: '8px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                            <span style={{ fontSize: '32px' }}>🛡️</span>
                            <div>
                                <div style={{ fontWeight: '600', color: '#065f46' }}>Iron Will</div>
                                <div style={{ fontSize: '14px', color: '#047857' }}>Resisted 25+ distractions</div>
                            </div>
                        </div>
                    )}

                    {consistency.current_streak >= 7 && (
                        <div style={{ padding: '12px', background: '#fee2e2', borderRadius: '8px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                            <span style={{ fontSize: '32px' }}>🔥</span>
                            <div>
                                <div style={{ fontWeight: '600', color: '#991b1b' }}>Week Warrior</div>
                                <div style={{ fontSize: '14px', color: '#b91c1c' }}>7-day streak active</div>
                            </div>
                        </div>
                    )}

                    {(!stamina.total_hours || stamina.total_hours < 10) &&
                        (!resilience.total || resilience.total < 25) &&
                        (!consistency.current_streak || consistency.current_streak < 7) && (
                            <div style={{ textAlign: 'center', padding: '32px', color: '#9ca3af' }}>
                                <p>Keep going! Achievements unlock as you progress.</p>
                            </div>
                        )}
                </div>
            </div>
        </div>
    )
}

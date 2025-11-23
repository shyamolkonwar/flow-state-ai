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
                    Crystal RPG 🏆
                </h1>
                <p className="body-text" style={{
                    fontSize: '18px',
                    color: 'rgba(255, 255, 255, 0.7)',
                    marginBottom: '8px'
                }}>
                    Your focus journey, gamified in crystal form
                </p>
                <div style={{
                    width: '80px',
                    height: '3px',
                    background: 'linear-gradient(90deg, var(--prism-cyan), var(--hyper-teal))',
                    borderRadius: '2px'
                }}></div>
            </div>

            {/* Level and XP */}
            <div className="glass-card crystal-hover" style={{
                marginBottom: '48px',
                position: 'relative',
                overflow: 'hidden'
            }}>
                <div style={{
                    position: 'absolute',
                    top: '24px',
                    right: '24px',
                    width: '80px',
                    height: '80px',
                    background: 'linear-gradient(135deg, var(--solar-gold), var(--flare-orange))',
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '32px',
                    boxShadow: '0 0 20px rgba(255, 198, 107, 0.3)'
                }}>
                    ⭐
                </div>

                <div style={{
                    display: 'grid',
                    gridTemplateColumns: '1fr auto',
                    gap: '32px',
                    alignItems: 'center'
                }}>
                    <div>
                        <div style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '16px',
                            marginBottom: '16px'
                        }}>
                            <div className="numeric" style={{
                                fontSize: '48px',
                                fontWeight: '700',
                                color: 'var(--solar-gold)',
                                textShadow: '0 0 10px rgba(255, 198, 107, 0.5)'
                            }}>
                                {level}
                            </div>
                            <div style={{
                                padding: '8px 16px',
                                borderRadius: '20px',
                                fontSize: '14px',
                                fontWeight: '600',
                                background: 'linear-gradient(135deg, var(--prism-cyan), var(--hyper-teal))',
                                color: 'var(--deep-night)'
                            }}>
                                Crystal Level
                            </div>
                        </div>

                        <div className="body-text" style={{
                            fontSize: '16px',
                            color: 'rgba(255, 255, 255, 0.7)',
                            marginBottom: '20px'
                        }}>
                            {experience.toLocaleString()} / {next_level_xp.toLocaleString()} Focus Crystals
                        </div>

                        {/* XP Progress Bar */}
                        <div style={{
                            width: '100%',
                            height: '16px',
                            background: 'rgba(255, 255, 255, 0.1)',
                            borderRadius: '8px',
                            overflow: 'hidden',
                            position: 'relative'
                        }}>
                            <div style={{
                                width: `${(experience / next_level_xp) * 100}%`,
                                height: '100%',
                                background: 'linear-gradient(90deg, var(--prism-cyan), var(--hyper-teal), var(--aurora-magenta))',
                                borderRadius: '8px',
                                transition: 'width 0.8s ease',
                                boxShadow: '0 0 10px rgba(77, 229, 255, 0.4)'
                            }}></div>
                            <div style={{
                                position: 'absolute',
                                top: '0',
                                left: '0',
                                right: '0',
                                bottom: '0',
                                background: 'linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent)',
                                animation: 'shimmer 2s ease-in-out infinite'
                            }}></div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Stats Grid */}
            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
                gap: '32px',
                marginBottom: '48px'
            }}>
                {/* Stamina */}
                <div className="glass-card crystal-hover" style={{
                    position: 'relative',
                    overflow: 'hidden'
                }}>
                    <div style={{
                        position: 'absolute',
                        top: '20px',
                        right: '20px',
                        width: '50px',
                        height: '50px',
                        background: 'linear-gradient(135deg, var(--hyper-teal), var(--green-flash))',
                        borderRadius: '50%',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '24px'
                    }}>
                        💪
                    </div>
                    <div className="numeric" style={{
                        fontSize: '42px',
                        fontWeight: '700',
                        color: 'var(--hyper-teal)',
                        marginBottom: '8px'
                    }}>
                        {stamina.total_hours}h
                    </div>
                    <div className="body-text" style={{
                        fontSize: '18px',
                        color: 'rgba(255, 255, 255, 0.8)',
                        fontWeight: '600',
                        marginBottom: '16px'
                    }}>
                        Crystal Stamina
                    </div>
                    <div style={{
                        display: 'flex',
                        gap: '16px',
                        fontSize: '14px',
                        color: 'rgba(255, 255, 255, 0.6)'
                    }}>
                        <div>📊 Avg: {stamina.average_session}m</div>
                        <div>🏆 Best: {stamina.personal_best}m</div>
                    </div>
                    <div style={{
                        position: 'absolute',
                        bottom: '20px',
                        left: '20px',
                        width: '80px',
                        height: '3px',
                        background: 'linear-gradient(90deg, var(--hyper-teal), var(--green-flash))',
                        borderRadius: '2px'
                    }}></div>
                </div>

                {/* Resilience */}
                <div className="glass-card crystal-hover" style={{
                    position: 'relative',
                    overflow: 'hidden'
                }}>
                    <div style={{
                        position: 'absolute',
                        top: '20px',
                        right: '20px',
                        width: '50px',
                        height: '50px',
                        background: 'linear-gradient(135deg, var(--aurora-magenta), var(--flare-orange))',
                        borderRadius: '50%',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '24px'
                    }}>
                        🛡️
                    </div>
                    <div className="numeric" style={{
                        fontSize: '42px',
                        fontWeight: '700',
                        color: 'var(--aurora-magenta)',
                        marginBottom: '8px'
                    }}>
                        {resilience.total}
                    </div>
                    <div className="body-text" style={{
                        fontSize: '18px',
                        color: 'rgba(255, 255, 255, 0.8)',
                        fontWeight: '600',
                        marginBottom: '16px'
                    }}>
                        Crystal Resilience
                    </div>
                    <div style={{
                        padding: '6px 16px',
                        borderRadius: '16px',
                        fontSize: '14px',
                        fontWeight: '600',
                        background: 'linear-gradient(135deg, var(--aurora-magenta), var(--flare-orange))',
                        color: 'var(--deep-night)',
                        display: 'inline-block'
                    }}>
                        {resilience.rank} Crystal Rank
                    </div>
                    <div style={{
                        position: 'absolute',
                        bottom: '20px',
                        left: '20px',
                        width: '80px',
                        height: '3px',
                        background: 'linear-gradient(90deg, var(--aurora-magenta), var(--flare-orange))',
                        borderRadius: '2px'
                    }}></div>
                </div>

                {/* Consistency */}
                <div className="glass-card crystal-hover" style={{
                    position: 'relative',
                    overflow: 'hidden'
                }}>
                    <div style={{
                        position: 'absolute',
                        top: '20px',
                        right: '20px',
                        width: '50px',
                        height: '50px',
                        background: 'linear-gradient(135deg, var(--flare-orange), var(--solar-gold))',
                        borderRadius: '50%',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '24px'
                    }}>
                        🔥
                    </div>
                    <div className="numeric" style={{
                        fontSize: '42px',
                        fontWeight: '700',
                        color: 'var(--flare-orange)',
                        marginBottom: '8px'
                    }}>
                        {consistency.current_streak}
                    </div>
                    <div className="body-text" style={{
                        fontSize: '18px',
                        color: 'rgba(255, 255, 255, 0.8)',
                        fontWeight: '600',
                        marginBottom: '16px'
                    }}>
                        Crystal Consistency
                    </div>
                    <div style={{
                        fontSize: '14px',
                        color: 'rgba(255, 255, 255, 0.6)',
                        marginBottom: '8px'
                    }}>
                        🔥 Best Streak: {consistency.best_streak} days
                    </div>
                    <div style={{
                        position: 'absolute',
                        bottom: '20px',
                        left: '20px',
                        width: '80px',
                        height: '3px',
                        background: 'linear-gradient(90deg, var(--flare-orange), var(--solar-gold))',
                        borderRadius: '2px'
                    }}></div>
                </div>
            </div>

            {/* Progressive Goal */}
            <div className="glass-card crystal-hover" style={{
                background: 'linear-gradient(135deg, var(--deep-night), rgba(11, 7, 16, 0.8))',
                border: '1px solid rgba(77, 229, 255, 0.2)',
                marginBottom: '48px',
                position: 'relative',
                overflow: 'hidden'
            }}>
                <div style={{
                    position: 'absolute',
                    top: '0',
                    left: '0',
                    right: '0',
                    bottom: '0',
                    background: 'radial-gradient(circle at 30% 70%, rgba(77, 229, 255, 0.1) 0%, transparent 50%), radial-gradient(circle at 70% 30%, rgba(255, 110, 199, 0.1) 0%, transparent 50%)',
                    pointerEvents: 'none'
                }}></div>

                <div style={{
                    position: 'absolute',
                    top: '24px',
                    right: '24px',
                    width: '60px',
                    height: '60px',
                    background: 'linear-gradient(135deg, var(--prism-cyan), var(--hyper-teal))',
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '28px',
                    boxShadow: '0 0 20px rgba(77, 229, 255, 0.4)'
                }}>
                    🎯
                </div>

                <div style={{ position: 'relative', zIndex: '1', padding: '32px' }}>
                    <h2 className="headline" style={{
                        fontSize: '28px',
                        color: 'var(--prism-cyan)',
                        marginBottom: '16px',
                        letterSpacing: '0.02em'
                    }}>
                        Progressive Crystal Goal
                    </h2>
                    <div className="numeric" style={{
                        fontSize: '56px',
                        fontWeight: '700',
                        color: 'var(--hyper-teal)',
                        marginBottom: '12px',
                        textShadow: '0 0 15px rgba(47, 230, 193, 0.5)'
                    }}>
                        {progressive_goal} minutes
                    </div>
                    <p className="body-text" style={{
                        fontSize: '16px',
                        color: 'rgba(255, 255, 255, 0.7)',
                        lineHeight: '1.6'
                    }}>
                        Your next crystal focus target. The system adapts to your performance, growing stronger with each session.
                    </p>
                </div>
            </div>

            {/* Achievements Section */}
            <div className="glass-card">
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
                        Crystal Achievements 🏆
                    </h2>
                    <p className="body-text" style={{
                        fontSize: '16px',
                        color: 'rgba(255, 255, 255, 0.6)'
                    }}>
                        Your focus milestones, crystallized forever
                    </p>
                </div>

                <div style={{ display: 'grid', gap: '20px' }}>
                    {stamina.total_hours >= 10 && (
                        <div className="crystal-hover" style={{
                            padding: '24px',
                            background: 'linear-gradient(135deg, rgba(255, 198, 107, 0.1), rgba(255, 154, 99, 0.1))',
                            borderRadius: '16px',
                            border: '1px solid rgba(255, 198, 107, 0.3)',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '20px',
                            position: 'relative',
                            overflow: 'hidden'
                        }}>
                            <div style={{
                                width: '60px',
                                height: '60px',
                                background: 'linear-gradient(135deg, var(--solar-gold), var(--flare-orange))',
                                borderRadius: '50%',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                fontSize: '28px',
                                boxShadow: '0 0 15px rgba(255, 198, 107, 0.4)'
                            }}>
                                🏅
                            </div>
                            <div>
                                <div className="headline" style={{
                                    fontSize: '20px',
                                    fontWeight: '600',
                                    color: 'var(--solar-gold)',
                                    marginBottom: '4px'
                                }}>
                                    10 Hour Crystal Club
                                </div>
                                <div className="body-text" style={{
                                    fontSize: '14px',
                                    color: 'rgba(255, 198, 107, 0.8)'
                                }}>
                                    Accumulated 10+ hours of pure flow time
                                </div>
                            </div>
                        </div>
                    )}

                    {resilience.total >= 25 && (
                        <div className="crystal-hover" style={{
                            padding: '24px',
                            background: 'linear-gradient(135deg, rgba(47, 230, 193, 0.1), rgba(77, 229, 255, 0.1))',
                            borderRadius: '16px',
                            border: '1px solid rgba(47, 230, 193, 0.3)',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '20px',
                            position: 'relative',
                            overflow: 'hidden'
                        }}>
                            <div style={{
                                width: '60px',
                                height: '60px',
                                background: 'linear-gradient(135deg, var(--hyper-teal), var(--green-flash))',
                                borderRadius: '50%',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                fontSize: '28px',
                                boxShadow: '0 0 15px rgba(47, 230, 193, 0.4)'
                            }}>
                                🛡️
                            </div>
                            <div>
                                <div className="headline" style={{
                                    fontSize: '20px',
                                    fontWeight: '600',
                                    color: 'var(--hyper-teal)',
                                    marginBottom: '4px'
                                }}>
                                    Iron Crystal Will
                                </div>
                                <div className="body-text" style={{
                                    fontSize: '14px',
                                    color: 'rgba(47, 230, 193, 0.8)'
                                }}>
                                    Resisted 25+ distractions with unbreakable focus
                                </div>
                            </div>
                        </div>
                    )}

                    {consistency.current_streak >= 7 && (
                        <div className="crystal-hover" style={{
                            padding: '24px',
                            background: 'linear-gradient(135deg, rgba(255, 110, 199, 0.1), rgba(196, 139, 255, 0.1))',
                            borderRadius: '16px',
                            border: '1px solid rgba(255, 110, 199, 0.3)',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '20px',
                            position: 'relative',
                            overflow: 'hidden'
                        }}>
                            <div style={{
                                width: '60px',
                                height: '60px',
                                background: 'linear-gradient(135deg, var(--aurora-magenta), var(--violet-edge))',
                                borderRadius: '50%',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                fontSize: '28px',
                                boxShadow: '0 0 15px rgba(255, 110, 199, 0.4)'
                            }}>
                                🔥
                            </div>
                            <div>
                                <div className="headline" style={{
                                    fontSize: '20px',
                                    fontWeight: '600',
                                    color: 'var(--aurora-magenta)',
                                    marginBottom: '4px'
                                }}>
                                    Week Crystal Warrior
                                </div>
                                <div className="body-text" style={{
                                    fontSize: '14px',
                                    color: 'rgba(255, 110, 199, 0.8)'
                                }}>
                                    7-day crystal focus streak active
                                </div>
                            </div>
                        </div>
                    )}

                    {(!stamina.total_hours || stamina.total_hours < 10) &&
                        (!resilience.total || resilience.total < 25) &&
                        (!consistency.current_streak || consistency.current_streak < 7) && (
                            <div style={{
                                textAlign: 'center',
                                padding: '60px 40px',
                                color: 'rgba(255, 255, 255, 0.6)'
                            }}>
                                <div style={{
                                    fontSize: '48px',
                                    marginBottom: '20px',
                                    opacity: '0.3'
                                }}>
                                    💎
                                </div>
                                <h3 className="headline" style={{
                                    fontSize: '20px',
                                    color: 'var(--prism-cyan)',
                                    marginBottom: '8px'
                                }}>
                                    Crystal Achievements Await
                                </h3>
                                <p className="body-text" style={{
                                    fontSize: '14px',
                                    color: 'rgba(255, 255, 255, 0.5)'
                                }}>
                                    Keep focusing! Your crystal achievements will unlock as you progress.
                                </p>
                            </div>
                        )}
                </div>
            </div>
        </div>
    )
}

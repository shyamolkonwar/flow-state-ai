import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../lib/AuthContext'

export default function Layout({ children }) {
    const { signOut, profile } = useAuth()
    const navigate = useNavigate()

    const handleLogout = async () => {
        await signOut()
        navigate('/login')
    }

    return (
        <div className="app-layout">
            {/* Background Elements */}
            <div className="particle-field">
                {[...Array(20)].map((_, i) => (
                    <div
                        key={i}
                        className="particle"
                        style={{
                            left: `${Math.random() * 100}%`,
                            animationDelay: `${Math.random() * 20}s`
                        }}
                    />
                ))}
            </div>

            <div className="crystal-shard"></div>
            <div className="crystal-shard"></div>
            <div className="crystal-shard"></div>

            <div className="ambient-pulse"></div>

            {/* Glass Navigation Panel */}
            <aside className="glass-card" style={{
                width: '280px',
                margin: '24px',
                height: 'calc(100vh - 48px)',
                display: 'flex',
                flexDirection: 'column',
                position: 'relative',
                zIndex: 10
            }}>
                <div style={{ marginBottom: '48px' }}>
                    <h1 className="headline" style={{
                        fontSize: '28px',
                        background: 'linear-gradient(135deg, var(--prism-cyan), var(--hyper-teal))',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                        backgroundClip: 'text',
                        marginBottom: '8px'
                    }}>
                        FlowFacilitator
                    </h1>
                    <p className="body-text" style={{
                        fontSize: '14px',
                        color: 'rgba(255, 255, 255, 0.7)',
                        marginTop: '4px'
                    }}>
                        Crystal Clarity Focus
                    </p>
                </div>

                <nav style={{ flex: 1 }}>
                    <NavLink to="/" className="nav-link crystal-hover" style={{
                        display: 'flex',
                        alignItems: 'center',
                        padding: '16px 20px',
                        marginBottom: '8px',
                        borderRadius: '16px',
                        color: 'rgba(255, 255, 255, 0.8)',
                        textDecoration: 'none',
                        transition: 'all 0.3s ease',
                        fontSize: '16px',
                        fontWeight: '500'
                    }}>
                        <span style={{ marginRight: '12px', fontSize: '20px' }}>🏠</span>
                        Home
                    </NavLink>
                    <NavLink to="/sessions" className="nav-link crystal-hover" style={{
                        display: 'flex',
                        alignItems: 'center',
                        padding: '16px 20px',
                        marginBottom: '8px',
                        borderRadius: '16px',
                        color: 'rgba(255, 255, 255, 0.8)',
                        textDecoration: 'none',
                        transition: 'all 0.3s ease',
                        fontSize: '16px',
                        fontWeight: '500'
                    }}>
                        <span style={{ marginRight: '12px', fontSize: '20px' }}>📊</span>
                        Sessions
                    </NavLink>
                    <NavLink to="/gamification" className="nav-link crystal-hover" style={{
                        display: 'flex',
                        alignItems: 'center',
                        padding: '16px 20px',
                        marginBottom: '8px',
                        borderRadius: '16px',
                        color: 'rgba(255, 255, 255, 0.8)',
                        textDecoration: 'none',
                        transition: 'all 0.3s ease',
                        fontSize: '16px',
                        fontWeight: '500'
                    }}>
                        <span style={{ marginRight: '12px', fontSize: '20px' }}>🎮</span>
                        RPG Stats
                    </NavLink>
                    <NavLink to="/settings" className="nav-link crystal-hover" style={{
                        display: 'flex',
                        alignItems: 'center',
                        padding: '16px 20px',
                        marginBottom: '8px',
                        borderRadius: '16px',
                        color: 'rgba(255, 255, 255, 0.8)',
                        textDecoration: 'none',
                        transition: 'all 0.3s ease',
                        fontSize: '16px',
                        fontWeight: '500'
                    }}>
                        <span style={{ marginRight: '12px', fontSize: '20px' }}>⚙️</span>
                        Settings
                    </NavLink>
                </nav>

                <div style={{ marginTop: 'auto' }}>
                    {/* Flow State Indicator */}
                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        marginBottom: '24px',
                        padding: '16px',
                        background: 'rgba(255, 255, 255, 0.05)',
                        borderRadius: '12px'
                    }}>
                        <div className="flow-indicator" style={{ marginRight: '12px' }}></div>
                        <div>
                            <div className="body-text" style={{
                                fontSize: '12px',
                                color: 'rgba(255, 255, 255, 0.6)',
                                marginBottom: '4px'
                            }}>
                                Flow Status
                            </div>
                            <div className="body-text" style={{
                                fontSize: '14px',
                                color: 'var(--green-flash)',
                                fontWeight: '600'
                            }}>
                                <span id="agent-status">Checking...</span>
                            </div>
                        </div>
                    </div>

                    <div style={{
                        padding: '16px',
                        background: 'rgba(255, 255, 255, 0.03)',
                        borderRadius: '12px',
                        fontSize: '12px',
                        color: 'rgba(255, 255, 255, 0.6)',
                        marginBottom: '16px'
                    }}>
                        <div style={{ marginBottom: '8px' }}>
                            <strong>Version:</strong> <span className="numeric">1.0.0</span>
                        </div>
                        <div style={{ marginBottom: '12px' }}>
                            <strong>Crystal Core:</strong> Active
                        </div>
                        {profile && (
                            <div style={{ marginBottom: '12px', fontSize: '11px' }}>
                                <strong>Welcome:</strong> {profile.full_name || profile.email}
                            </div>
                        )}
                    </div>

                    <button
                        onClick={handleLogout}
                        className="crystal-hover"
                        style={{
                            width: '100%',
                            padding: '12px 16px',
                            background: 'rgba(255, 99, 71, 0.1)',
                            border: '1px solid rgba(255, 99, 71, 0.3)',
                            borderRadius: '12px',
                            color: '#FF6347',
                            fontSize: '14px',
                            fontWeight: '500',
                            cursor: 'pointer',
                            transition: 'all 0.3s ease'
                        }}
                    >
                        🚪 Sign Out
                    </button>
                </div>
            </aside>

            <main className="main-content" style={{ position: 'relative', zIndex: 10 }}>
                {children}
            </main>
        </div>
    )
}

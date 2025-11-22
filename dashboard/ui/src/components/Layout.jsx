import { NavLink } from 'react-router-dom'

export default function Layout({ children }) {
    return (
        <div className="app-layout">
            <aside className="sidebar">
                <div style={{ marginBottom: '32px' }}>
                    <h1 style={{ fontSize: '24px', fontWeight: '700', color: '#667eea' }}>
                        FlowFacilitator
                    </h1>
                    <p style={{ fontSize: '14px', color: '#6b7280', marginTop: '4px' }}>
                        Focus Analytics
                    </p>
                </div>

                <nav>
                    <NavLink to="/" className="nav-link">
                        🏠 Home
                    </NavLink>
                    <NavLink to="/sessions" className="nav-link">
                        📊 Sessions
                    </NavLink>
                    <NavLink to="/gamification" className="nav-link">
                        🎮 RPG Stats
                    </NavLink>
                    <NavLink to="/settings" className="nav-link">
                        ⚙️ Settings
                    </NavLink>
                </nav>

                <div style={{ marginTop: 'auto', paddingTop: '32px' }}>
                    <div style={{
                        padding: '12px',
                        background: '#f9fafb',
                        borderRadius: '8px',
                        fontSize: '12px',
                        color: '#6b7280'
                    }}>
                        <div style={{ marginBottom: '4px' }}>
                            <strong>Status:</strong> <span id="agent-status">Checking...</span>
                        </div>
                        <div>
                            <strong>Version:</strong> 1.0.0
                        </div>
                    </div>
                </div>
            </aside>

            <main className="main-content">
                {children}
            </main>
        </div>
    )
}

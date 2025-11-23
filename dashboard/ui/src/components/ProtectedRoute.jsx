import { useAuth } from '../lib/AuthContext'
import { Navigate } from 'react-router-dom'

export default function ProtectedRoute({ children }) {
    const { user, loading } = useAuth()

    console.log('🔒 ProtectedRoute - user:', user, 'loading:', loading)

    if (loading) {
        console.log('🔄 ProtectedRoute showing loading spinner')
        return (
            <div style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                minHeight: '100vh',
                background: 'var(--deep-night)',
                color: 'var(--crystal-white)'
            }}>
                <div className="spinner"></div>
            </div>
        )
    }

    if (!user) {
        console.log('🚫 ProtectedRoute redirecting to login - no user')
        return <Navigate to="/login" replace />
    }

    console.log('✅ ProtectedRoute rendering children')
    return children
}

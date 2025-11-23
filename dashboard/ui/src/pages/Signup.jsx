import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../lib/AuthContext'

export default function Signup() {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')
    const [fullName, setFullName] = useState('')
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')
    const { signUp } = useAuth()
    const navigate = useNavigate()

    const handleSubmit = async (e) => {
        e.preventDefault()
        setLoading(true)
        setError('')

        if (password !== confirmPassword) {
            setError('Passwords do not match')
            setLoading(false)
            return
        }

        if (password.length < 6) {
            setError('Password must be at least 6 characters long')
            setLoading(false)
            return
        }

        try {
            const { error } = await signUp(email, password, fullName)
            if (error) throw error

            // Show success message and redirect to login
            alert('Account created successfully! Please check your email to verify your account.')
            navigate('/login')
        } catch (error) {
            setError(error.message)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div style={{
            minHeight: '100vh',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: 'var(--deep-night)',
            position: 'relative',
            overflow: 'hidden'
        }}>
            {/* Background Elements */}
            <div style={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                background:
                    'radial-gradient(circle at 20% 80%, rgba(77, 229, 255, 0.1) 0%, transparent 50%), ' +
                    'radial-gradient(circle at 80% 20%, rgba(255, 110, 199, 0.1) 0%, transparent 50%), ' +
                    'radial-gradient(circle at 40% 40%, rgba(47, 230, 193, 0.05) 0%, transparent 50%)',
                pointerEvents: 'none',
                zIndex: 0
            }}></div>

            <div style={{
                width: '100%',
                maxWidth: '400px',
                padding: '40px',
                position: 'relative',
                zIndex: 1
            }}>
                {/* Header */}
                <div style={{ textAlign: 'center', marginBottom: '40px' }}>
                    <h1 style={{
                        fontSize: '32px',
                        fontWeight: '600',
                        background: 'linear-gradient(135deg, var(--prism-cyan), var(--hyper-teal))',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                        backgroundClip: 'text',
                        marginBottom: '12px',
                        letterSpacing: '0.02em'
                    }}>
                        Join FlowFacilitator
                    </h1>
                    <p style={{
                        color: 'rgba(255, 255, 255, 0.7)',
                        fontSize: '16px',
                        marginBottom: '8px'
                    }}>
                        Create your account to start your flow journey
                    </p>
                    <div style={{
                        width: '60px',
                        height: '2px',
                        background: 'linear-gradient(90deg, var(--prism-cyan), var(--hyper-teal))',
                        borderRadius: '1px',
                        margin: '0 auto'
                    }}></div>
                </div>

                {/* Signup Form */}
                <div className="glass-card" style={{
                    padding: '32px',
                    backdropFilter: 'blur(20px)',
                    WebkitBackdropFilter: 'blur(20px)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: '20px'
                }}>
                    <form onSubmit={handleSubmit}>
                        {error && (
                            <div style={{
                                padding: '12px',
                                background: 'rgba(255, 99, 71, 0.1)',
                                border: '1px solid rgba(255, 99, 71, 0.3)',
                                borderRadius: '8px',
                                color: '#FF6347',
                                marginBottom: '20px',
                                fontSize: '14px'
                            }}>
                                {error}
                            </div>
                        )}

                        <div style={{ marginBottom: '20px' }}>
                            <label style={{
                                display: 'block',
                                color: 'rgba(255, 255, 255, 0.8)',
                                fontSize: '14px',
                                fontWeight: '500',
                                marginBottom: '8px'
                            }}>
                                Full Name
                            </label>
                            <input
                                type="text"
                                value={fullName}
                                onChange={(e) => setFullName(e.target.value)}
                                className="glow-focus"
                                style={{
                                    width: '100%',
                                    padding: '14px 16px',
                                    background: 'rgba(255, 255, 255, 0.05)',
                                    border: '1px solid rgba(255, 255, 255, 0.2)',
                                    borderRadius: '12px',
                                    color: 'var(--crystal-white)',
                                    fontSize: '16px',
                                    outline: 'none',
                                    transition: 'all 0.3s ease'
                                }}
                                placeholder="Enter your full name"
                                required
                            />
                        </div>

                        <div style={{ marginBottom: '20px' }}>
                            <label style={{
                                display: 'block',
                                color: 'rgba(255, 255, 255, 0.8)',
                                fontSize: '14px',
                                fontWeight: '500',
                                marginBottom: '8px'
                            }}>
                                Email Address
                            </label>
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="glow-focus"
                                style={{
                                    width: '100%',
                                    padding: '14px 16px',
                                    background: 'rgba(255, 255, 255, 0.05)',
                                    border: '1px solid rgba(255, 255, 255, 0.2)',
                                    borderRadius: '12px',
                                    color: 'var(--crystal-white)',
                                    fontSize: '16px',
                                    outline: 'none',
                                    transition: 'all 0.3s ease'
                                }}
                                placeholder="Enter your email"
                                required
                            />
                        </div>

                        <div style={{ marginBottom: '20px' }}>
                            <label style={{
                                display: 'block',
                                color: 'rgba(255, 255, 255, 0.8)',
                                fontSize: '14px',
                                fontWeight: '500',
                                marginBottom: '8px'
                            }}>
                                Password
                            </label>
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="glow-focus"
                                style={{
                                    width: '100%',
                                    padding: '14px 16px',
                                    background: 'rgba(255, 255, 255, 0.05)',
                                    border: '1px solid rgba(255, 255, 255, 0.2)',
                                    borderRadius: '12px',
                                    color: 'var(--crystal-white)',
                                    fontSize: '16px',
                                    outline: 'none',
                                    transition: 'all 0.3s ease'
                                }}
                                placeholder="Create a password (min 6 characters)"
                                required
                            />
                        </div>

                        <div style={{ marginBottom: '24px' }}>
                            <label style={{
                                display: 'block',
                                color: 'rgba(255, 255, 255, 0.8)',
                                fontSize: '14px',
                                fontWeight: '500',
                                marginBottom: '8px'
                            }}>
                                Confirm Password
                            </label>
                            <input
                                type="password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                className="glow-focus"
                                style={{
                                    width: '100%',
                                    padding: '14px 16px',
                                    background: 'rgba(255, 255, 255, 0.05)',
                                    border: '1px solid rgba(255, 255, 255, 0.2)',
                                    borderRadius: '12px',
                                    color: 'var(--crystal-white)',
                                    fontSize: '16px',
                                    outline: 'none',
                                    transition: 'all 0.3s ease'
                                }}
                                placeholder="Confirm your password"
                                required
                            />
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className="crystal-hover"
                            style={{
                                width: '100%',
                                padding: '16px',
                                background: 'linear-gradient(135deg, var(--prism-cyan), var(--hyper-teal))',
                                border: 'none',
                                borderRadius: '12px',
                                color: 'var(--deep-night)',
                                fontSize: '16px',
                                fontWeight: '600',
                                cursor: loading ? 'not-allowed' : 'pointer',
                                transition: 'all 0.3s ease',
                                marginBottom: '20px',
                                position: 'relative',
                                overflow: 'hidden'
                            }}
                        >
                            {loading ? 'Creating Account...' : 'Create Account'}
                        </button>
                    </form>

                    <div style={{ textAlign: 'center' }}>
                        <p style={{
                            color: 'rgba(255, 255, 255, 0.6)',
                            fontSize: '14px',
                            marginBottom: '16px'
                        }}>
                            Already have an account?{' '}
                            <Link
                                to="/login"
                                style={{
                                    color: 'var(--prism-cyan)',
                                    textDecoration: 'none',
                                    fontWeight: '500'
                                }}
                            >
                                Sign in
                            </Link>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    )
}

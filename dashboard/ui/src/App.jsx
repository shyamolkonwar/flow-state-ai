import { Routes, Route } from 'react-router-dom'
import { AuthProvider } from './lib/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'
import Layout from './components/Layout'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Home from './pages/Home'
import Sessions from './pages/Sessions'
import Settings from './pages/Settings'
import Gamification from './pages/Gamification'

function App() {
    console.log('📱 App component rendering...')

    return (
        <AuthProvider>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<Signup />} />
                <Route path="/" element={
                    <ProtectedRoute>
                        <Layout>
                            <Home />
                        </Layout>
                    </ProtectedRoute>
                } />
                <Route path="/sessions" element={
                    <ProtectedRoute>
                        <Layout>
                            <Sessions />
                        </Layout>
                    </ProtectedRoute>
                } />
                <Route path="/gamification" element={
                    <ProtectedRoute>
                        <Layout>
                            <Gamification />
                        </Layout>
                    </ProtectedRoute>
                } />
                <Route path="/settings" element={
                    <ProtectedRoute>
                        <Layout>
                            <Settings />
                        </Layout>
                    </ProtectedRoute>
                } />
            </Routes>
        </AuthProvider>
    )
}

export default App

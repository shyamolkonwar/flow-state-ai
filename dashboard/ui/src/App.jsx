import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import Sessions from './pages/Sessions'
import Settings from './pages/Settings'
import Gamification from './pages/Gamification'

function App() {
    return (
        <Layout>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/sessions" element={<Sessions />} />
                <Route path="/gamification" element={<Gamification />} />
                <Route path="/settings" element={<Settings />} />
            </Routes>
        </Layout>
    )
}

export default App

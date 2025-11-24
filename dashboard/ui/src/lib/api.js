import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Agent API client
const AGENT_API_URL = import.meta.env.VITE_AGENT_API_URL
const AGENT_API_TOKEN = import.meta.env.VITE_AGENT_API_TOKEN

export const agentAPI = {
    async getStatus() {
        try {
            const response = await fetch(`${AGENT_API_URL}/status`, {
                headers: {
                    'Authorization': `Bearer ${AGENT_API_TOKEN}`
                }
            })
            if (!response.ok) {
                throw new Error(`Agent API returned ${response.status}`)
            }
            return await response.json()
        } catch (error) {
            console.warn('Agent service not available, using mock data:', error.message)
            // Return mock data for development
            return {
                flow_state: 'working',
                time_in_state_seconds: 1800,
                current_app: 'Visual Studio Code',
                typing_rate: 350,
                distractions_blocked_today: 12
            }
        }
    },

    async pause(durationMinutes) {
        const response = await fetch(`${AGENT_API_URL}/pause`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${AGENT_API_TOKEN}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ duration_minutes: durationMinutes })
        })
        return response.json()
    },

    async addToWhitelist(domain) {
        const response = await fetch(`${AGENT_API_URL}/whitelist/add`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${AGENT_API_TOKEN}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ domain })
        })
        return response.json()
    }
}

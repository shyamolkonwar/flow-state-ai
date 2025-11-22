import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Agent API client
const AGENT_API_URL = import.meta.env.VITE_AGENT_API_URL
const AGENT_API_TOKEN = import.meta.env.VITE_AGENT_API_TOKEN

export const agentAPI = {
    async getStatus() {
        const response = await fetch(`${AGENT_API_URL}/status`, {
            headers: {
                'Authorization': `Bearer ${AGENT_API_TOKEN}`
            }
        })
        return response.json()
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

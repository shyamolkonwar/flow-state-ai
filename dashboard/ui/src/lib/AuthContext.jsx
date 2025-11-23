import { createContext, useContext, useEffect, useState } from 'react'
import { supabase } from './api'

const AuthContext = createContext({})

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null)
    const [loading, setLoading] = useState(true)
    const [profile, setProfile] = useState(null)

    useEffect(() => {
        let mounted = true;

        // Get initial session
        const initializeAuth = async () => {
            try {
                console.log('Initializing auth...');
                const { data: { session }, error } = await supabase.auth.getSession();

                if (error) {
                    console.error('Error getting session:', error);
                    if (mounted) {
                        setLoading(false);
                    }
                    return;
                }

                console.log('Session retrieved:', session ? 'exists' : 'none');
                if (mounted) {
                    setUser(session?.user ?? null);
                    if (session?.user) {
                        console.log('Fetching profile for user:', session.user.id);
                        await fetchProfile(session.user.id);
                    } else {
                        console.log('No user session found');
                    }
                    setLoading(false);
                }
            } catch (error) {
                console.error('Error initializing auth:', error);
                if (mounted) {
                    setLoading(false);
                }
            }
        };

        initializeAuth();

        // Fallback timeout to ensure loading doesn't get stuck
        const loadingTimeout = setTimeout(() => {
            if (mounted) {
                console.log('Loading timeout reached, forcing loading to false');
                setLoading(false);
            }
        }, 5000); // 5 second timeout

        // Listen for auth changes
        const { data: { subscription } } = supabase.auth.onAuthStateChange(
            async (event, session) => {
                console.log('Auth state changed:', event, session?.user?.email);
                if (mounted) {
                    console.log('Mounted is true, processing auth change');
                    setUser(session?.user ?? null);
                    if (session?.user) {
                        console.log('Fetching profile in auth change listener');
                        // Don't await fetchProfile - let it run in background
                        fetchProfile(session.user.id).catch(error => {
                            console.error('Profile fetch failed:', error);
                        });
                    } else {
                        setProfile(null);
                    }
                    console.log('Setting loading to false in auth change listener');
                    setLoading(false);
                    clearTimeout(loadingTimeout); // Clear the fallback timeout
                } else {
                    console.log('Mounted is false, skipping auth change processing');
                }
            }
        )

        return () => {
            mounted = false;
            clearTimeout(loadingTimeout);
            subscription.unsubscribe();
        }
    }, [])

    const fetchProfile = async (userId) => {
        try {
            const { data, error } = await supabase
                .from('all_users')
                .select('*')
                .eq('id', userId)
                .single()

            if (error) throw error
            setProfile(data)
        } catch (error) {
            console.error('Error fetching profile:', error)
        }
    }

    const signUp = async (email, password, fullName) => {
        const { data, error } = await supabase.auth.signUp({
            email,
            password,
            options: {
                data: {
                    full_name: fullName
                }
            }
        })
        return { data, error }
    }

    const signIn = async (email, password) => {
        const { data, error } = await supabase.auth.signInWithPassword({
            email,
            password
        })
        return { data, error }
    }

    const signOut = async () => {
        const { error } = await supabase.auth.signOut()
        return { error }
    }

    const resetPassword = async (email) => {
        const { data, error } = await supabase.auth.resetPasswordForEmail(email, {
            redirectTo: `${window.location.origin}/reset-password`
        })
        return { data, error }
    }

    const value = {
        user,
        profile,
        loading,
        signUp,
        signIn,
        signOut,
        resetPassword
    }

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    )
}

export function useAuth() {
    const context = useContext(AuthContext)
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider')
    }
    return context
}

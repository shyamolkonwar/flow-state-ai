"""
Authentication Service for FlowFacilitator
Handles all Supabase authentication operations
"""

import logging
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
from supabase import create_client, Client
from gotrue.errors import AuthApiError

# Disable problematic keyring backends to prevent segfault with PyObjC
import keyring
try:
    from keyring.backends.macOS import Keyring as MacOSKeyring
    keyring.set_keyring(MacOSKeyring())
except ImportError:
    # Fallback - just use default but disable the problematic ones
    pass


class AuthService:
    """Manages user authentication with Supabase"""
    
    KEYRING_SERVICE = "FlowFacilitator"
    ACCESS_TOKEN_KEY = "access_token"
    REFRESH_TOKEN_KEY = "refresh_token"
    
    def __init__(self, config: Dict):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.client: Optional[Client] = None
        self.current_user = None
        self.session = None
        
        # Initialize Supabase client
        self._initialize_client()
        
        # Try to restore session from keychain
        self._restore_session()
    
    def _initialize_client(self):
        """Initialize Supabase client"""
        try:
            url = self.config['supabase']['url']
            # Use anon key for client-side auth
            anon_key = self.config['supabase'].get('anon_key') or self.config['supabase']['service_key']
            
            self.client = create_client(url, anon_key)
            self.logger.info(f"Initialized Supabase client at {url}")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Supabase client: {e}")
            raise
    
    def _restore_session(self):
        """Restore session from keychain"""
        try:
            access_token = keyring.get_password(self.KEYRING_SERVICE, self.ACCESS_TOKEN_KEY)
            refresh_token = keyring.get_password(self.KEYRING_SERVICE, self.REFRESH_TOKEN_KEY)
            
            if access_token and refresh_token:
                # Try to restore session
                result = self.client.auth.set_session(access_token, refresh_token)
                
                if result.user:
                    self.current_user = result.user
                    self.session = result.session
                    self.logger.info(f"Restored session for user: {self.current_user.email}")
                    return True
                    
        except Exception as e:
            self.logger.warning(f"Could not restore session: {e}")
            self._clear_stored_credentials()
        
        return False
    
    def _store_credentials(self, access_token: str, refresh_token: str):
        """Store credentials in keychain"""
        try:
            keyring.set_password(self.KEYRING_SERVICE, self.ACCESS_TOKEN_KEY, access_token)
            keyring.set_password(self.KEYRING_SERVICE, self.REFRESH_TOKEN_KEY, refresh_token)
            self.logger.info("Stored credentials in keychain")
        except Exception as e:
            self.logger.error(f"Failed to store credentials: {e}")
    
    def _clear_stored_credentials(self):
        """Clear credentials from keychain"""
        try:
            keyring.delete_password(self.KEYRING_SERVICE, self.ACCESS_TOKEN_KEY)
            keyring.delete_password(self.KEYRING_SERVICE, self.REFRESH_TOKEN_KEY)
            self.logger.info("Cleared stored credentials")
        except Exception as e:
            self.logger.warning(f"Could not clear credentials: {e}")
    
    def sign_up(self, email: str, password: str, full_name: str = "") -> Tuple[bool, Optional[str]]:
        """
        Sign up a new user

        Returns:
            (success: bool, error_message: Optional[str])
        """
        self.logger.info(f"🔐 [DEBUG] Starting signup for email: {email}, full_name: {full_name}")
        try:
            # Sign up with Supabase Auth
            signup_data = {
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "full_name": full_name
                    }
                }
            }
            self.logger.info(f"🔐 [DEBUG] Signup request data: {signup_data}")

            result = self.client.auth.sign_up(signup_data)
            self.logger.info(f"🔐 [DEBUG] Signup result received: user={result.user is not None}, session={result.session is not None}")

            if result.user:
                self.logger.info(f"🔐 [DEBUG] Signup successful - user ID: {result.user.id}, email: {result.user.email}")
                self.current_user = result.user
                self.session = result.session

                # Store credentials
                if result.session:
                    self.logger.info("🔐 [DEBUG] Storing session credentials")
                    self._store_credentials(
                        result.session.access_token,
                        result.session.refresh_token
                    )

                self.logger.info(f"User signed up: {email}")
                return True, None
            else:
                self.logger.warning("🔐 [DEBUG] Signup failed - no user returned")
                return False, "Signup failed"

        except AuthApiError as e:
            self.logger.error(f"🔐 [DEBUG] Signup AuthApiError: {e}")
            return False, str(e)
        except Exception as e:
            self.logger.error(f"🔐 [DEBUG] Unexpected signup error: {e}")
            return False, "An unexpected error occurred"
    
    def sign_in(self, email: str, password: str) -> Tuple[bool, Optional[str]]:
        """
        Sign in an existing user

        Returns:
            (success: bool, error_message: Optional[str])
        """
        self.logger.info(f"🔐 [DEBUG] Starting signin for email: {email}")
        try:
            signin_data = {
                "email": email,
                "password": password
            }
            self.logger.info(f"🔐 [DEBUG] Signin request data: {signin_data}")

            result = self.client.auth.sign_in_with_password(signin_data)
            self.logger.info(f"🔐 [DEBUG] Signin result received: user={result.user is not None}, session={result.session is not None}")

            if result.user:
                self.logger.info(f"🔐 [DEBUG] Signin successful - user ID: {result.user.id}, email: {result.user.email}")
                self.current_user = result.user
                self.session = result.session

                # Store credentials
                if result.session:
                    self.logger.info("🔐 [DEBUG] Storing session credentials")
                    self._store_credentials(
                        result.session.access_token,
                        result.session.refresh_token
                    )

                self.logger.info(f"User signed in: {email}")
                return True, None
            else:
                self.logger.warning("🔐 [DEBUG] Signin failed - no user returned")
                return False, "Sign in failed"

        except AuthApiError as e:
            self.logger.error(f"🔐 [DEBUG] Signin AuthApiError: {e}")
            error_msg = "Invalid email or password"
            if "Email not confirmed" in str(e):
                error_msg = "Please verify your email address"
            return False, error_msg
        except Exception as e:
            self.logger.error(f"🔐 [DEBUG] Unexpected signin error: {e}")
            return False, "An unexpected error occurred"
    
    def sign_out(self) -> Tuple[bool, Optional[str]]:
        """
        Sign out the current user
        
        Returns:
            (success: bool, error_message: Optional[str])
        """
        try:
            self.client.auth.sign_out()
            
            # Clear stored credentials
            self._clear_stored_credentials()
            
            self.current_user = None
            self.session = None
            
            self.logger.info("User signed out")
            return True, None
            
        except Exception as e:
            self.logger.error(f"Sign out error: {e}")
            return False, str(e)
    
    def reset_password(self, email: str) -> Tuple[bool, Optional[str]]:
        """
        Send password reset email
        
        Returns:
            (success: bool, error_message: Optional[str])
        """
        try:
            self.client.auth.reset_password_email(email)
            self.logger.info(f"Password reset email sent to: {email}")
            return True, None
            
        except AuthApiError as e:
            self.logger.error(f"Password reset error: {e}")
            return False, str(e)
        except Exception as e:
            self.logger.error(f"Unexpected password reset error: {e}")
            return False, "An unexpected error occurred"
    
    def update_password(self, new_password: str) -> Tuple[bool, Optional[str]]:
        """
        Update user password
        
        Returns:
            (success: bool, error_message: Optional[str])
        """
        try:
            if not self.is_authenticated():
                return False, "User not authenticated"
            
            self.client.auth.update_user({
                "password": new_password
            })
            
            self.logger.info("Password updated")
            return True, None
            
        except AuthApiError as e:
            self.logger.error(f"Password update error: {e}")
            return False, str(e)
        except Exception as e:
            self.logger.error(f"Unexpected password update error: {e}")
            return False, "An unexpected error occurred"
    
    def get_session(self):
        """Get current session"""
        return self.session
    
    def refresh_session(self) -> Tuple[bool, Optional[str]]:
        """
        Refresh the current session
        
        Returns:
            (success: bool, error_message: Optional[str])
        """
        try:
            if not self.session or not self.session.refresh_token:
                return False, "No session to refresh"
            
            result = self.client.auth.refresh_session(self.session.refresh_token)
            
            if result.session:
                self.session = result.session
                self.current_user = result.user
                
                # Update stored credentials
                self._store_credentials(
                    result.session.access_token,
                    result.session.refresh_token
                )
                
                self.logger.info("Session refreshed")
                return True, None
            else:
                return False, "Session refresh failed"
                
        except Exception as e:
            self.logger.error(f"Session refresh error: {e}")
            return False, str(e)
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.current_user is not None and self.session is not None
    
    def get_user_profile(self) -> Optional[Dict]:
        """
        Get user profile from all_users table
        
        Returns:
            User profile dict or None
        """
        try:
            if not self.is_authenticated():
                return None
            
            result = self.client.rpc('get_user_profile').execute()
            
            if result.data and len(result.data) > 0:
                return result.data[0]
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting user profile: {e}")
            return None
    
    def update_user_profile(self, data: Dict) -> Tuple[bool, Optional[str]]:
        """
        Update user profile
        
        Args:
            data: Dict with fields to update (full_name, etc.)
        
        Returns:
            (success: bool, error_message: Optional[str])
        """
        try:
            if not self.is_authenticated():
                return False, "User not authenticated"
            
            # Update auth user metadata
            if 'full_name' in data:
                self.client.auth.update_user({
                    "data": {
                        "full_name": data['full_name']
                    }
                })
            
            # Update all_users table
            self.client.table('all_users').update(data).eq('id', self.current_user.id).execute()
            
            self.logger.info("User profile updated")
            return True, None
            
        except Exception as e:
            self.logger.error(f"Error updating user profile: {e}")
            return False, str(e)
    
    def mark_onboarding_complete(self) -> Tuple[bool, Optional[str]]:
        """
        Mark onboarding as complete
        
        Returns:
            (success: bool, error_message: Optional[str])
        """
        try:
            if not self.is_authenticated():
                return False, "User not authenticated"
            
            self.client.rpc('complete_onboarding').execute()
            
            self.logger.info("Onboarding marked complete")
            return True, None
            
        except Exception as e:
            self.logger.error(f"Error marking onboarding complete: {e}")
            return False, str(e)
    
    def get_onboarding_status(self) -> Tuple[bool, int]:
        """
        Get onboarding status
        
        Returns:
            (complete: bool, step: int)
        """
        try:
            profile = self.get_user_profile()
            
            if profile:
                return profile.get('onboarding_complete', False), profile.get('onboarding_step', 0)
            
            return False, 0
            
        except Exception as e:
            self.logger.error(f"Error getting onboarding status: {e}")
            return False, 0

class AuthorizationService:

    def authorize_session(self, session):
        """
        Checks if the session is valid and the user has credits.
        Returns (True, None) if authorized, (False, error_message) if not.
        """
        if not session or 'user' not in session:
            return False, "Session is invalid or expired."
        if not session['user'].get('has_credits', False):
            return False, "User doesn't have credits."
        return True, None

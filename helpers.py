from firebase_admin import auth

def verify_firebase_token(id_token):
    """
    Verifies a Firebase ID token.

    Args:
        id_token (str): Firebase ID token sent by the client.

    Returns:
        dict: Decoded token info if valid.
        None: If token is invalid or expired.
    """
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception:
        return None

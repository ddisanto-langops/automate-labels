import os
import logging
import secrets
from functools import wraps
from flask import request, jsonify

logger = logging.getLogger(__name__)

def require_x_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        provided_key = request.headers.get('X-Auth')
        secret_key = os.environ.get('X_AUTH')

        if not secret_key:
            return jsonify({'error':'Server configuration error'}), 500
        
        if provided_key and secrets.compare_digest(provided_key, secret_key):
            logger.info(f"X-Auth validated for path: {request.path}")
            return f(*args, **kwargs)
        
        # 3. Handle Failure
        logger.critical(f"Invalid or missing X-Auth key")
        return jsonify({"error": "Unauthorized"}), 401
        
    return decorated_function
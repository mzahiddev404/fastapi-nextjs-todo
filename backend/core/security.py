# =============================================================================
# SECURITY UTILITIES
# =============================================================================
# Handles password hashing and JWT token management
# Provides authentication and authorization functions

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
import re
import secrets

# Password hashing configuration - using pbkdf2_sha256 for better Python 3.13 compatibility
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# JWT configuration
SECRET_KEY = os.getenv("JWT_SECRET")
if not SECRET_KEY:
    raise ValueError("JWT_SECRET environment variable is required for production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("JWT_REFRESH_EXPIRE_DAYS", "7"))

# =============================================================================
# PASSWORD FUNCTIONS
# =============================================================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password using pbkdf2_sha256"""
    return pwd_context.hash(password)

def validate_password_strength(password: str) -> tuple[bool, str]:
    """Validate password strength and return (is_valid, error_message)"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    
    return True, ""

def generate_secure_token(length: int = 32) -> str:
    """Generate a cryptographically secure random token"""
    return secrets.token_urlsafe(length)

# =============================================================================
# JWT TOKEN FUNCTIONS
# =============================================================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    
    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """Create a JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[str]:
    """Verify JWT token and return user_id if valid"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return user_id
    except JWTError:
        return None

def get_token_expiration(token: str) -> Optional[datetime]:
    """Get token expiration time"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get("exp")
        if exp:
            return datetime.fromtimestamp(exp)
        return None
    except JWTError:
        return None

def is_token_expired(token: str) -> bool:
    """Check if token is expired"""
    exp_time = get_token_expiration(token)
    if exp_time is None:
        return True
    return datetime.utcnow() > exp_time
"""
Authentication API endpoints
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user
)
from app.models import User
from app.schemas import (
    Token,
    LoginRequest,
    RefreshRequest,
    UserCreate,
    UserResponse,
    UserProfile
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT tokens.
    
    - **username**: User email
    - **password**: User password
    """
    # Find user by email
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Compte désactivé. Contactez l'administrateur."
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create tokens
    token_data = {"sub": user.email, "role": user.role}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    request: RefreshRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    """
    try:
        payload = decode_token(request.refresh_token)
        
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de rafraîchissement invalide"
            )
        
        email = payload.get("sub")
        user = db.query(User).filter(User.email == email).first()
        
        if not user or not user.active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Utilisateur non trouvé ou désactivé"
            )
        
        # Create new tokens
        token_data = {"sub": user.email, "role": user.role}
        new_access_token = create_access_token(token_data)
        new_refresh_token = create_refresh_token(token_data)
        
        return Token(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de rafraîchissement invalide ou expiré"
        )


@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user profile.
    """
    return UserProfile(
        id=current_user.id,
        email=current_user.email,
        nom=current_user.nom,
        prenom=current_user.prenom,
        role=current_user.role,
        nom_complet=current_user.nom_complet
    )


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Register a new user (admin only).
    """
    # Only directors and administrators can create users
    if current_user.role not in ["director", "administrator"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seuls les directeurs et administrateurs peuvent créer des utilisateurs"
        )
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un utilisateur avec cet email existe déjà"
        )
    
    # Create new user
    new_user = User(
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        role=user_data.role.value,
        nom=user_data.nom,
        prenom=user_data.prenom,
        ref_id=user_data.ref_id,
        active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout current user (client-side token invalidation).
    """
    # In a stateless JWT system, logout is handled client-side
    # Here we just return a success message
    return {"message": "Déconnexion réussie"}


@router.put("/change-password")
async def change_password(
    old_password: str,
    new_password: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Change current user password.
    """
    # Verify old password
    if not verify_password(old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mot de passe actuel incorrect"
        )
    
    # Validate new password
    if len(new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le nouveau mot de passe doit contenir au moins 6 caractères"
        )
    
    # Update password
    current_user.password_hash = get_password_hash(new_password)
    db.commit()
    
    return {"message": "Mot de passe modifié avec succès"}


from pydantic import BaseModel, EmailStr
import random

# In-memory store for reset codes (in production, use Redis with expiry)
reset_codes: dict[str, str] = {}

class RequestResetRequest(BaseModel):
    email: EmailStr

@router.post("/request-reset")
async def request_reset(
    request: RequestResetRequest,
    db: Session = Depends(get_db)
):
    """
    Request a password reset - generates a 6-digit verification code.
    In production, this code would be sent via email.
    """
    # Check if user exists
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucun compte trouvé avec cet email"
        )
    
    # Generate 6-digit code
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    # Store the code (in production, add expiry time)
    reset_codes[request.email] = code
    
    # In production: send email with code
    # For demo: return code in response
    return {
        "message": "Code de vérification envoyé",
        "code": code  # Remove this in production!
    }

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    new_password: str
    verification_code: str = None  # Optional for backwards compatibility

@router.post("/reset-password")
async def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Reset user password with verification code.
    """
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucun compte trouvé avec cet email"
        )
    
    # Verify the code if provided
    if request.verification_code:
        stored_code = reset_codes.get(request.email)
        if not stored_code or stored_code != request.verification_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Code de vérification invalide ou expiré"
            )
        # Remove the used code
        del reset_codes[request.email]
    
    # Validate new password
    if len(request.new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le mot de passe doit contenir au moins 6 caractères"
        )
    
    # Update password
    user.password_hash = get_password_hash(request.new_password)
    db.commit()
    
    return {"message": "Mot de passe réinitialisé avec succès"}


class ChangeEmailRequest(BaseModel):
    new_email: EmailStr
    password: str

@router.put("/change-email")
async def change_email(
    request: ChangeEmailRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Change current user email.
    """
    # Verify password
    if not verify_password(request.password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mot de passe incorrect"
        )
    
    # Check if new email already exists
    existing_user = db.query(User).filter(User.email == request.new_email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cet email est déjà utilisé par un autre compte"
        )
    
    # Update email
    current_user.email = request.new_email
    db.commit()
    
    return {"message": "Email modifié avec succès"}

from fastapi import Depends, HTTPException, status
from .auth.action import get_current_user
from .models import Role

def role_required(*roles):
    def role_checker(current_user=Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )
        return current_user
    return role_checker
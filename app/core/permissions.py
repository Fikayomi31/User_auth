
from fastapi import Depends, HTTPException, status

from app.dependencies import get_current_user
from app.model.user import User, UserRole


def require_role(*allowed_roles: UserRole):
    async def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this page.",
            )

        return current_user

    return role_checker

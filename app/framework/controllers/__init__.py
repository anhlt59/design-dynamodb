from fastapi import APIRouter, Depends

from app.framework.controllers import v1
from app.framework.security import api_key_required

router = APIRouter(prefix="/api", dependencies=[Depends(api_key_required)])
# Attach v1,... routers to the main router
router.include_router(v1.router)


@router.route("/health")
def health():
    return {"status": True}


__all__ = ["router"]

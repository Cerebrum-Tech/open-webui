import logging
from fastapi import APIRouter, Depends, HTTPException, status

from open_webui.models.agreements import (
    UserAgreements,
    AgreementAcceptForm,
    AgreementStatusResponse,
    AllAgreementsResponse,
)
from open_webui.utils.auth import get_current_user, get_verified_user, get_admin_user
from open_webui.env import SRC_LOG_LEVELS

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

router = APIRouter()


############################
# Get Agreement Status
############################


@router.get("/status", response_model=AgreementStatusResponse)
async def get_agreement_status(user=Depends(get_current_user)):
    """
    Get the current user's EULA and GDPR acceptance status
    """
    try:
        return UserAgreements.get_agreement_status(user.id)
    except Exception as e:
        log.error(f"Error getting agreement status: {e}")
        # Return needs_acceptance=True if there's an error (e.g., table doesn't exist)
        return AgreementStatusResponse(
            eula_accepted=False,
            eula_accepted_at=None,
            gdpr_accepted=False,
            gdpr_accepted_at=None,
            needs_acceptance=True
        )


############################
# Accept Agreement
############################


@router.post("/accept", response_model=AgreementStatusResponse)
async def accept_agreement(
    form_data: AgreementAcceptForm,
    user=Depends(get_current_user)
):
    """
    Accept EULA and/or GDPR agreement
    """
    if not form_data.eula_accepted and not form_data.gdpr_accepted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one agreement must be accepted"
        )
    
    result = UserAgreements.accept_agreement(
        user_id=user.id,
        eula_accepted=form_data.eula_accepted,
        gdpr_accepted=form_data.gdpr_accepted
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to accept agreement"
        )
    
    return UserAgreements.get_agreement_status(user.id)


############################
# Check if User Needs to Accept Agreement
############################


@router.get("/needs-acceptance")
async def needs_acceptance(user=Depends(get_current_user)):
    """
    Check if the user needs to accept EULA and GDPR
    """
    return {"needs_acceptance": UserAgreements.check_needs_acceptance(user.id)}


############################
# Admin: Get All Agreements Report
############################


@router.get("/admin/report", response_model=AllAgreementsResponse)
async def get_all_agreements_report(user=Depends(get_admin_user)):
    """
    Get all user agreements for admin report.
    Only accessible by admin users.
    """
    return UserAgreements.get_all_agreements_with_users()


############################
# Admin: Reset Own EULA (for testing)
############################


@router.post("/admin/reset-own")
async def reset_own_agreement(user=Depends(get_admin_user)):
    """
    Reset the admin's own EULA acceptance for testing purposes.
    Only accessible by admin users.
    """
    result = UserAgreements.reset_agreement(user.id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reset agreement"
        )
    return {"success": True, "message": "Your EULA acceptance has been reset. Refresh the page to see the EULA modal."}


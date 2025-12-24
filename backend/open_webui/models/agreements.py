import time
from typing import Optional

from open_webui.internal.db import Base, get_db

from pydantic import BaseModel, ConfigDict
from sqlalchemy import BigInteger, Column, String, Boolean, Text


####################
# UserAgreement DB Schema
####################


class UserAgreement(Base):
    __tablename__ = "user_agreement"

    id = Column(String, primary_key=True)  # Same as user ID
    eula_accepted = Column(Boolean, default=False)
    eula_accepted_at = Column(BigInteger, nullable=True)
    gdpr_accepted = Column(Boolean, default=False)
    gdpr_accepted_at = Column(BigInteger, nullable=True)
    
    created_at = Column(BigInteger)
    updated_at = Column(BigInteger)


class UserAgreementModel(BaseModel):
    id: str
    eula_accepted: bool = False
    eula_accepted_at: Optional[int] = None
    gdpr_accepted: bool = False
    gdpr_accepted_at: Optional[int] = None
    
    created_at: int
    updated_at: int

    model_config = ConfigDict(from_attributes=True)


####################
# Forms
####################


class AgreementAcceptForm(BaseModel):
    eula_accepted: bool = False
    gdpr_accepted: bool = False


class AgreementStatusResponse(BaseModel):
    eula_accepted: bool = False
    eula_accepted_at: Optional[int] = None
    gdpr_accepted: bool = False
    gdpr_accepted_at: Optional[int] = None
    needs_acceptance: bool = True


####################
# UserAgreementsTable
####################


class UserAgreementWithUser(BaseModel):
    id: str
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    eula_accepted: bool = False
    eula_accepted_at: Optional[int] = None
    gdpr_accepted: bool = False
    gdpr_accepted_at: Optional[int] = None
    created_at: int
    updated_at: int


class AllAgreementsResponse(BaseModel):
    agreements: list[UserAgreementWithUser]
    total: int
    accepted_count: int
    pending_count: int


class UserAgreementsTable:
    def get_user_agreement(self, user_id: str) -> Optional[UserAgreementModel]:
        try:
            with get_db() as db:
                agreement = db.query(UserAgreement).filter_by(id=user_id).first()
                if agreement:
                    return UserAgreementModel.model_validate(agreement)
                return None
        except Exception as e:
            print(f"Error getting user agreement: {e}")
            return None

    def create_user_agreement(self, user_id: str) -> Optional[UserAgreementModel]:
        try:
            with get_db() as db:
                current_time = int(time.time())
                agreement = UserAgreement(
                    id=user_id,
                    eula_accepted=False,
                    eula_accepted_at=None,
                    gdpr_accepted=False,
                    gdpr_accepted_at=None,
                    created_at=current_time,
                    updated_at=current_time,
                )
                db.add(agreement)
                db.commit()
                db.refresh(agreement)
                return UserAgreementModel.model_validate(agreement)
        except Exception:
            return None

    def get_or_create_user_agreement(self, user_id: str) -> Optional[UserAgreementModel]:
        agreement = self.get_user_agreement(user_id)
        if agreement:
            return agreement
        return self.create_user_agreement(user_id)

    def accept_agreement(
        self, 
        user_id: str, 
        eula_accepted: bool = False, 
        gdpr_accepted: bool = False
    ) -> Optional[UserAgreementModel]:
        try:
            with get_db() as db:
                current_time = int(time.time())
                
                # Get or create agreement
                agreement = db.query(UserAgreement).filter_by(id=user_id).first()
                
                if not agreement:
                    agreement = UserAgreement(
                        id=user_id,
                        eula_accepted=False,
                        eula_accepted_at=None,
                        gdpr_accepted=False,
                        gdpr_accepted_at=None,
                        created_at=current_time,
                        updated_at=current_time,
                    )
                    db.add(agreement)
                    db.flush()

                # Update agreement
                update_data = {"updated_at": current_time}
                
                if eula_accepted and not agreement.eula_accepted:
                    update_data["eula_accepted"] = True
                    update_data["eula_accepted_at"] = current_time
                
                if gdpr_accepted and not agreement.gdpr_accepted:
                    update_data["gdpr_accepted"] = True
                    update_data["gdpr_accepted_at"] = current_time

                db.query(UserAgreement).filter_by(id=user_id).update(update_data)
                db.commit()
                
                agreement = db.query(UserAgreement).filter_by(id=user_id).first()
                return UserAgreementModel.model_validate(agreement)
        except Exception as e:
            print(f"Error accepting agreement: {e}")
            return None

    def check_needs_acceptance(self, user_id: str) -> bool:
        """
        Returns True if user needs to accept EULA (Terms of Use).
        Note: GDPR/Privacy Notice does NOT require consent per KVKK regulations.
        """
        try:
            agreement = self.get_user_agreement(user_id)
            if not agreement:
                return True
            return not agreement.eula_accepted
        except Exception as e:
            print(f"Error checking needs_acceptance: {e}")
            # If there's an error (e.g., table doesn't exist), return True to show the modal
            return True

    def get_agreement_status(self, user_id: str) -> AgreementStatusResponse:
        print(f"[EULA] Checking agreement status for user: {user_id}")
        agreement = self.get_user_agreement(user_id)
        
        if not agreement:
            print(f"[EULA] No agreement record found for user {user_id}, needs_acceptance=True")
            return AgreementStatusResponse(
                eula_accepted=False,
                eula_accepted_at=None,
                gdpr_accepted=False,
                gdpr_accepted_at=None,
                needs_acceptance=True
            )
        
        # Only EULA acceptance is required, not GDPR (Privacy Notice)
        # GDPR/Privacy Notice is informational only per KVKK regulations
        needs_acceptance = not agreement.eula_accepted
        print(f"[EULA] User {user_id}: eula_accepted={agreement.eula_accepted}, needs_acceptance={needs_acceptance}")
        
        return AgreementStatusResponse(
            eula_accepted=agreement.eula_accepted,
            eula_accepted_at=agreement.eula_accepted_at,
            gdpr_accepted=agreement.gdpr_accepted,
            gdpr_accepted_at=agreement.gdpr_accepted_at,
            needs_acceptance=needs_acceptance
        )


    def reset_agreement(self, user_id: str) -> bool:
        """
        Reset a user's EULA acceptance (for testing purposes).
        """
        try:
            with get_db() as db:
                agreement = db.query(UserAgreement).filter_by(id=user_id).first()
                if agreement:
                    agreement.eula_accepted = False
                    agreement.eula_accepted_at = None
                    agreement.updated_at = int(time.time())
                    db.commit()
                return True
        except Exception as e:
            print(f"Error resetting agreement: {e}")
            return False

    def get_all_agreements_with_users(self) -> AllAgreementsResponse:
        """
        Get all user agreements with user information for admin report
        """
        from open_webui.models.users import User
        
        try:
            with get_db() as db:
                # Get all users
                users = db.query(User).all()
                
                agreements_list = []
                accepted_count = 0
                pending_count = 0
                
                for user in users:
                    # Get agreement for this user
                    agreement = db.query(UserAgreement).filter_by(id=user.id).first()
                    
                    if agreement and agreement.eula_accepted:
                        accepted_count += 1
                        agreements_list.append(UserAgreementWithUser(
                            id=user.id,
                            user_name=user.name,
                            user_email=user.email,
                            eula_accepted=agreement.eula_accepted,
                            eula_accepted_at=agreement.eula_accepted_at,
                            gdpr_accepted=agreement.gdpr_accepted,
                            gdpr_accepted_at=agreement.gdpr_accepted_at,
                            created_at=agreement.created_at,
                            updated_at=agreement.updated_at,
                        ))
                    else:
                        pending_count += 1
                        agreements_list.append(UserAgreementWithUser(
                            id=user.id,
                            user_name=user.name,
                            user_email=user.email,
                            eula_accepted=False,
                            eula_accepted_at=None,
                            gdpr_accepted=False,
                            gdpr_accepted_at=None,
                            created_at=int(time.time()),
                            updated_at=int(time.time()),
                        ))
                
                return AllAgreementsResponse(
                    agreements=agreements_list,
                    total=len(agreements_list),
                    accepted_count=accepted_count,
                    pending_count=pending_count
                )
        except Exception as e:
            print(f"Error getting all agreements: {e}")
            return AllAgreementsResponse(
                agreements=[],
                total=0,
                accepted_count=0,
                pending_count=0
            )


UserAgreements = UserAgreementsTable()


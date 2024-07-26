from typing import List

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import OperationalError, IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.sql.models import Feedback, User
from app.sql.dtos import FeedbackCreateDTO, FeedbackReadDTO

class FeedbackController:
    def __init__(self, db: Session):
        self.db = db

    def create_feedback(self, feedback: FeedbackCreateDTO) -> dict:
        user_id = feedback.user_id
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )
        
        user_name = user.name
        
        feedback_instance = Feedback(
            user_name=user_name,
            user_id=user_id,
            rating=feedback.rating,
            description=feedback.description
        )
        try:
            self.db.add(feedback_instance)
            self.db.commit()
            self.db.refresh(feedback_instance)
            return {
                "message": "Feedback created successfully",
                "status_code": status.HTTP_201_CREATED,
            }
        except OperationalError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Database table not found'
            )
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Feedback already exists'
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    def get_feedback(self) -> dict:
        subquery = (
            self.db.query(
                Feedback.user_id,
                func.max(Feedback.rating).label('max_rating')
            )
            .group_by(Feedback.user_id)
            .subquery()
        )

        feedback_list = (
            self.db.query(Feedback)
            .join(subquery, (Feedback.user_id == subquery.c.user_id) & (Feedback.rating == subquery.c.max_rating))
            .options(joinedload(Feedback.user))
            .all()
        )

        if not feedback_list:
            raise HTTPException(status_code=404, detail="No feedback found")

        result = []
        for feedback in feedback_list:
            feedback_read = FeedbackReadDTO(
                user_name=feedback.user.name,
                url_img_user=feedback.user.url_image,  
                rating=feedback.rating,
                description=feedback.description
            )
            result.append(feedback_read)

        return {
            "message": "Feedback retrieved successfully",
            "status_code": status.HTTP_200_OK,
            "data": result
        }
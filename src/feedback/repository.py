from . import models
from db import DatabaseSession


def create_feedback(feedback, conflict_id, account_id) -> models.Feedback:
    with DatabaseSession() as db:
        fb_dict = feedback.dict()
        fb_dict.update({'conflict_id': conflict_id, 'account_id': account_id})
        db_feedback = models.Feedback.model_validate(fb_dict)
        db.add(db_feedback)
        db.commit()
        db.refresh(db_feedback)
        return db_feedback

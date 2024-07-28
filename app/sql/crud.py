from sqlalchemy import inspect

from .models import ActiveStocks


class Crud:
    def __init__(self, db_session=None):
        self.db_session = db_session

    def fill_active_stocks(self, json_data: dict) -> dict:
        inspector = inspect(self.db_session.bind)
        if inspector.has_table("active_stocks"):
            self.db_session.query(ActiveStocks).delete()
            self.db_session.commit()

        active_stocks_objects = [ActiveStocks(ticker=index) for index in json_data]
        self.db_session.bulk_save_objects(active_stocks_objects)
        self.db_session.commit()

        return {
            "message": "Active stocks updated"
        }

    def get_all_ative_stocks(self) -> dict:
        return self.db_session.query(ActiveStocks).all()

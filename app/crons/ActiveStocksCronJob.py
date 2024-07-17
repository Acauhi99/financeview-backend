import requests
from requests.exceptions import RequestException
from app.sql.crud import Crud
from requests.exceptions import JSONDecodeError
from sqlalchemy.exc import SQLAlchemyError
from app.sql.database import SessionLocal

class ActiveStocksCronJob: 
    @staticmethod
    def get_updated_stocks():
        url = "https://brapi.dev/api/available"
        try:
            response = requests.get(url)
            response.raise_for_status()
            json_data = response.json()

        except JSONDecodeError as json_exception:
            print(f"JSON decode error: {json_exception}")
            return

        except RequestException as req_exception:
            print(f"Request exception: {req_exception}")
            return
        
        db_session = SessionLocal()

        try:
            crud = Crud(db_session)
            crud.fill_active_stocks(json_data['stocks'])

        except SQLAlchemyError as sql_exception:
            print(f"SQLAlchemy error: {sql_exception}")
            return
        
        finally:
            db_session.close()

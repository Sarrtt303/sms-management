from datetime import datetime
from app import mongo

class SMS:
    @staticmethod
    def create_sms(phone_number, country_code, operator=None, status='pending'):
        sms_data = {
            "phone_number": phone_number,
            "country_code": country_code,
            "operator": operator,
            "status": status,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        result = mongo.db.sms_messages.insert_one(sms_data)
        return str(result.inserted_id)  # Return the ID of the inserted document

    @staticmethod
    def update_sms_status(sms_id, status):
        query = {"_id": sms_id}
        update = {
            "$set": {
                "status": status,
                "updated_at": datetime.utcnow()
            }
        }
        result = mongo.db.sms_messages.update_one(query, update)
        return result.modified_count > 0  # Return True if the update was successful

    @staticmethod
    def get_sms_by_id(sms_id):
        return mongo.db.sms_messages.find_one({"_id": sms_id})

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.services.sms_service import SMSService
from app.services.process_manager import ProcessManager
from app.models.sms import SMS  # Import your SMS model, if needed
from app import mongo  # Import mongo from your app setup
import datetime

api_bp = Blueprint('api', __name__)

@api_bp.route('/send-sms', methods=['POST'])
@jwt_required()
def send_sms():
    data = request.get_json()
    
    if not data or 'phone_number' not in data:
        return jsonify({"error": "Phone number required"}), 400
    
    sms_service = SMSService(data['phone_number'], data.get('proxy'))
    result = sms_service.send_otp()
    
    if result['success']:
        # Save SMS to MongoDB if needed
        sms_record = {
            "phone_number": data['phone_number'],
            "status": result['message'],  # Assuming result has a message field
            "created_at": datetime.utcnow()
        }
        mongo.db.sms_messages.insert_one(sms_record)  # Insert into MongoDB collection

        return jsonify(result), 200
    return jsonify(result), 500

@api_bp.route('/sessions', methods=['POST'])
@jwt_required()
def create_session():
    data = request.get_json()
    country = data.get('country')
    operator = data.get('operator')
    
    if not country or not operator:
        return jsonify({"error": "Country and operator required"}), 400
    
    session_name = ProcessManager.start_session(country, operator)
    return jsonify({"message": "Session started", "session": session_name}), 201

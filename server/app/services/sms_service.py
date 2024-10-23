class SMSService:
    def __init__(self, phone_number, proxy=None):
        self.phone_number = phone_number
        self.proxy = proxy

    def send_otp(self):
        try:
            # Your SMS sending logic here
            return {"success": True, "message": "SMS sent successfully"}
        except Exception as e:
            return {"success": False, "error": str(e)}


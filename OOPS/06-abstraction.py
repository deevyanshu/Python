class EmailService:

    def _connect(self):
        print("Connecting to email server...")
    
    def _authenticate(self):
        print("Authenticating user...")
    
    def send_email(self):
        self._connect()
        self._authenticate()
        print(f"Sending email")
        self._disconnect()
    
    def _disconnect(self):
        print("Disconnecting from email server...")

email=EmailService()
email.send_email()
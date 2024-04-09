from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Se quitó unique=True
    paid = db.Column(db.Boolean, default=False)
    payment_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<User {self.name}, {'Paid' if self.paid else 'Not Paid'}, {self.payment_date if self.paid else 'N/A'}>"
    
class FinancialEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(50), nullable=False)  # Por ejemplo, 'intereses', 'pago', etc.
    amount = db.Column(db.Integer, nullable=False)  # Puede ser positivo o negativo
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    description = db.Column(db.String(200))  # Descripción opcional del evento

    def __repr__(self):
        return f"<FinancialEvent {self.event_type}, Amount: {self.amount}, Date: {self.date}>"

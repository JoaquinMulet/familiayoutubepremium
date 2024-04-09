from flask import Blueprint, render_template, request, redirect, url_for
from flask import request, redirect, url_for, flash
from .models import User, FinancialEvent, db
from datetime import datetime, timedelta


bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    today = datetime.now()
    
    # Obtener la lista de usuarios y contar cuántos han pagado
    users = User.query.order_by(User.name).all()
    users_paid = User.query.filter_by(paid=True).count()

    # Calcular el total de la caja basado en el número de usuarios que han pagado
    total_caja = users_paid * 24000
    
    # Obtener todos los eventos financieros relacionados con intereses
    interests = FinancialEvent.query.filter_by(event_type='intereses').all()
    
    # Calcular el total de intereses ganados
    total_interests = sum(event.amount for event in interests)

    # Calcular descuentos desde Abril 2024 hasta hoy, cada 5 de mes
    start_date = datetime(2024, 4, 5)
    discount_amount = 0
    while start_date <= today:
        if start_date.day == 5:
            discount_amount += 12000
        start_date += timedelta(days=1)
    
    # Restar los descuentos y sumar los intereses al total de la caja
    total_caja -= discount_amount
    total_caja += total_interests

    return render_template('index.html', users=users, total_caja=total_caja)


@bp.route('/mark-payment', methods=['POST'])
def mark_payment():
    user_id = request.form.get('user_id')
    paid = 'paid' in request.form

    user = User.query.get(user_id)
    if user:
        user.paid = paid
        if paid:
            user.payment_date = datetime.utcnow()
        db.session.commit()
    
    return redirect(url_for('main.index'))

@bp.route('/admin')
def admin():
    financial_events = FinancialEvent.query.filter_by(event_type='intereses').order_by(FinancialEvent.date.desc()).all()
    users = User.query.all()
    return render_template('admin.html', users=users, financial_events=financial_events)

@bp.route('/add-user', methods=['POST'])
def add_user():
    name = request.form['name']
    if name:
        new_user = User(name=name, paid=False, payment_date=None)
        db.session.add(new_user)
        db.session.commit()
        flash('New member added successfully!', 'success')
    else:
        flash('Failed to add new member. Name is required.', 'danger')
    return redirect(url_for('main.admin'))

@bp.route('/delete-user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Member deleted successfully!', 'success')
    return redirect(url_for('main.admin'))

@bp.route('/reset-payment/<int:user_id>', methods=['POST'])
def reset_payment(user_id):
    user = User.query.get_or_404(user_id)
    user.paid = False
    user.payment_date = None
    db.session.commit()
    flash('Payment status reset successfully!', 'success')
    return redirect(url_for('main.admin'))

@bp.route('/add-interests', methods=['POST'])
def add_interests():
    amount = request.form.get('amount', type=int)
    if amount:
        new_event = FinancialEvent(event_type='intereses', amount=amount, date=datetime.utcnow())
        db.session.add(new_event)
        db.session.commit()
        flash('Intereses añadidos exitosamente.', 'success')
    else:
        flash('Error al añadir intereses. Por favor, verifica el monto ingresado.', 'danger')
    return redirect(url_for('main.admin'))

@bp.route('/delete-interest/<int:event_id>', methods=['POST'])
def delete_interest(event_id):
    event = FinancialEvent.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Interés eliminado exitosamente.', 'success')
    return redirect(url_for('main.admin'))

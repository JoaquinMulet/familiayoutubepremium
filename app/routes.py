from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta
from .models import add_user, get_users, delete_user, get_financial_events, add_financial_event, delete_financial_event, update_payment_status, reset_payment_status

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    today = datetime.now()
    users = get_users()
    users_paid = sum(1 for user in users if user['paid'])
    total_caja = users_paid * 24000
    
    interests = get_financial_events()
    total_interests = sum(event['amount'] for event in interests)

    # Calculating discounts
    start_date = datetime(2024, 4, 5)
    discount_amount = 0
    while start_date <= today:
        if start_date.day == 5:
            discount_amount += 12000
        start_date += timedelta(days=1)

    total_caja = total_caja - discount_amount + total_interests

    return render_template('index.html', users=users, total_caja=total_caja)

@bp.route('/admin')
def admin():
    financial_events = get_financial_events()
    users = get_users()
    return render_template('admin.html', users=users, financial_events=financial_events)

@bp.route('/add-user', methods=['POST'])
def add_user_route():
    name = request.form['name']
    if name:
        add_user(name)
        flash('New member added successfully!', 'success')
    else:
        flash('Failed to add new member. Name is required.', 'danger')
    return redirect(url_for('main.admin'))

@bp.route('/delete-user/<int:user_id>', methods=['POST'])
def delete_user_route(user_id):
    delete_user(user_id)
    flash('Member deleted successfully!', 'success')
    return redirect(url_for('main.admin'))

@bp.route('/mark-payment', methods=['POST'])
def mark_payment():
    user_id = request.form.get('user_id')
    paid = 'paid' in request.form
    update_payment_status(user_id, paid)
    flash('Payment status updated successfully!', 'success')
    return redirect(url_for('main.index'))

@bp.route('/add-interests', methods=['POST'])
def add_interests():
    amount = request.form.get('amount', type=int)
    if amount:
        add_financial_event(amount)
        flash('Interests added successfully.', 'success')
    else:
        flash('Error adding interests. Please verify the amount entered.', 'danger')
    return redirect(url_for('main.admin'))

@bp.route('/delete-interest/<int:event_id>', methods=['POST'])
def delete_interest(event_id):
    delete_financial_event(event_id)
    flash('Interest deleted successfully.', 'success')
    return redirect(url_for('main.admin'))

@bp.route('/reset-payment/<int:user_id>', methods=['POST'])
def reset_payment(user_id):
    reset_payment_status(user_id)
    flash('Payment status reset successfully!', 'success')
    return redirect(url_for('main.admin'))

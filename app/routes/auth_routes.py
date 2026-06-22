from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # If already logged in, redirect to dashboard
    if session.get('logged_in'):
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check against configured credentials
        if username == current_app.config['ADMIN_USERNAME'] and password == current_app.config['ADMIN_PASSWORD']:
            session['logged_in'] = True
            session['username'] = username
            flash('Login berhasil! Selamat datang.', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Username atau password salah.', 'danger')
            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('Anda telah berhasil logout.', 'info')
    return redirect(url_for('auth.login'))

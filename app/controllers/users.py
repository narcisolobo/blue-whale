from app.models.user import User
from app import app, render_template, redirect, request, session, flash, bcrypt

# redirect user to /login_reg
@app.get('/')
def redirect_user():
    return redirect('/users/login_reg')

# display forms for login/reg
@app.get('/users/login_reg')
def login_reg():
    return render_template('login_reg.html')

@app.post('/users/register')
def register_user():
    # check if form is valid
    if not User.validate_registration(request.form):
        return redirect('/users/login_reg')

    # if the form is valid, check to see if
    # they already registered
    found_user = User.find_by_email(request.form)
    if found_user:
        flash('Email already in database. Please login.', 'email')
        return redirect('/users/login_reg')

    # hash password (encrypt with bcrypt)
    hashed = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': hashed
    }

    # register (save) the user
    user_id = User.save(data)

    # log the user in and save user's id in session
    session['user_id'] = user_id
    return redirect('/magazines')

@app.post('/users/login')
def login_user():
    # check if form is valid
    if not User.validate_login(request.form):
        return redirect('/users/login_reg')

    # if the form is valid, check to see if
    # they are registered
    found_user = User.find_by_email(request.form)
    if not found_user:
        flash('Email not found, please register.', 'log_email')
        return redirect('/users/login_reg')

    # if they did register, check if the
    # password is correct
    if not bcrypt.check_password_hash(found_user.password, request.form['password']):
        flash('Invalid credentials. Please check your password.', 'log_password')
        return redirect('/users/login_reg')

    # if the password is correct,
    # log them in
    session['user_id'] = found_user.id
    return redirect('/magazines')

@app.get('/users/account')
def one_user():
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    logged_data = {
        'id': session['user_id'],
    }
    logged_user = User.find_by_id(logged_data)
    user_data = {
        'id': session['user_id'],
        'logged_user': logged_user
    }
    user = User.find_by_id_with_magazines(user_data)
    return render_template('one_user.html', user = user)

@app.post('/users/<int:user_id>/update')
def update_user(user_id):
    if not User.validate_update(request.form):
        return redirect('/users/account')
    User.find_by_id_and_update(request.form)
    return redirect('/users/account')

@app.get('/users/logout')
def logout():
    session.clear()
    return redirect('/users/login_reg')
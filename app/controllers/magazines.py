from pprint import pprint
from app import app, render_template, redirect, request, session
from app.models.magazine import Magazine
from app.models.user import User

# display all magazines
@app.get('/magazines')
def all_magazines():
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    user_data = {
        'id': session['user_id']
    }
    user = User.find_by_id(user_data)
    data = {
        'logged_user': user
    }
    magazines = Magazine.find_all_with_subscribers(data)
    print(f'**** FOUND - ALL MAGAZINES: ****')
    pprint(magazines)
    return render_template('all_magazines.html', magazines = magazines, user = user)

# display one magazine by id
@app.get('/magazines/<int:magazine_id>')
def one_magazine(magazine_id):
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    user_data = {
        'id': session['user_id']
    }
    user = User.find_by_id(user_data)
    data = {
        'id': magazine_id,
        'logged_user': user
    }
    magazine = Magazine.find_by_id_with_subscribers(data)
    print(f'**** FOUND - MAGAZINE ID: {magazine.id} ****')
    return render_template('one_magazine.html', magazine = magazine, user = user)

# display form to create a magazine
@app.get('/magazines/new')
def new_magazine():
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    user_data = {
        'id': session['user_id']
    }
    user = User.find_by_id(user_data)
    return render_template('new_magazine.html', user = user)

# process form and create a magazine
@app.post('/magazines')
def create_magazine():
    if not Magazine.validate_magazine(request.form):
        return redirect('/magazines/new')
    magazine_id = Magazine.save(request.form)
    print(f'**** CREATED - MAGAZINE ID: {magazine_id} ****')
    return redirect('/magazines')

# display form to edit a magazine by id
@app.get('/magazines/<int:magazine_id>/edit')
def edit_magazine(magazine_id):
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    user_data = {
        'id': session['user_id']
    }
    user = User.find_by_id(user_data)
    data = {
        'id': magazine_id
    }
    magazine = Magazine.find_by_id(data)
    print(f'**** FOUND - MAGAZINE ID: {magazine.id} ****')
    return render_template('edit_magazine.html', magazine = magazine, user = user)

# process form and update a magazine by id
@app.post('/magazines/<int:magazine_id>/update')
def update_magazine(magazine_id):
    if not Magazine.validate_magazine(request.form):
        return redirect(f'/magazines/{magazine_id}')
    Magazine.find_by_id_and_update(request.form)
    print(f'**** UPDATED - MAGAZINE ID: {magazine_id} ****')
    return redirect(f'/magazines/{magazine_id}')

# delete one magazine by id
@app.get('/magazines/<int:magazine_id>/delete')
def delete_magazine(magazine_id):
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    data = {
        'id': magazine_id
    }
    Magazine.find_by_id_and_delete(data)
    print(f'**** DELETED - MAGAZINE ID: {magazine_id} ****')
    return redirect('/users/account')
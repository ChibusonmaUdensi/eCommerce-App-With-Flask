@auth.route('/login', method = ['POST', 'GET'])
def login():
    data = request.form
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            flash('Login successful!', category = 'success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        else:
            flash('Invalid email or password', category = 'error')
    return render_template("login.html", text="testing", user = current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@auth.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
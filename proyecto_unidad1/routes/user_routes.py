from flask import Blueprint, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User, Post
from forms.user_forms import RegisterForm, LoginForm, EditProfileForm, PostForm
from extensions import db
from utils.decorators import login_required

user_bp = Blueprint('user', __name__)

# FEED
@user_bp.route('/', methods=['GET', 'POST'])
@login_required
def home():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(content=form.content.data, user_id=session['user_id'])
        db.session.add(post)
        db.session.commit()
        flash('Post publicado', 'success')
        return redirect(url_for('user.home'))

    posts = Post.query.order_by(Post.date_created.desc()).all()
    return render_template('user_list.html', posts=posts, form=form)


# REGISTER
@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Usuario registrado correctamente', 'success')
        return redirect(url_for('user.login'))

    return render_template('register.html', form=form)


# LOGIN
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash('Bienvenido', 'success')
            return redirect(url_for('user.home'))
        else:
            flash('Correo o contraseña incorrectos', 'danger')

    return render_template('login.html', form=form)


# LOGOUT
@user_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('user.login'))


# PROFILE
@user_bp.route('/profile/<int:id>')
@login_required
def profile(id):
    user = User.query.get_or_404(id)
    return render_template('profile.html', user=user)


# EDIT PROFILE
@user_bp.route('/profile/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    user = User.query.get_or_404(id)
    form = EditProfileForm(obj=user)

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
        flash('Perfil actualizado', 'success')
        return redirect(url_for('user.profile', id=user.id))

    return render_template('edit_profile.html', form=form)


# DELETE USER
@user_bp.route('/profile/<int:id>/delete', methods=['POST'])
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    session.clear()
    flash('Cuenta eliminada', 'warning')
    return redirect(url_for('user.register'))
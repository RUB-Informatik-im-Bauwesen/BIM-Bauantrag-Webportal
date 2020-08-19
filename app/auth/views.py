from flask import render_template, redirect, request, flash, url_for, abort
from . import auth
from .forms import LoginForm, ResetRequestForm, ResetPasswordForm
from ..models import User, Role
from flask_login import login_user, logout_user, login_required, current_user
from app import db

from .security import ts


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            site = request.args.get('next')
            if site is not None:
                return redirect(site)
            else:
                return redirect(url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route("/activateRole/<roleId>", methods=["GET"])
@login_required
def activateRole(roleId):

    role = Role.query.filter_by(id=roleId).first()

    if role is None:
        abort(404)

    if role in current_user.assignedRoles:
        current_user.activeRole = role.name
        db.session.add(current_user)
        db.session.commit()

    return redirect(url_for('main.index'))


@auth.route('/reset', methods=["GET", "POST"])
def reset():
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()

        subject = "Zurücksetzen des Passworts angefordert"

        # Here we use the URLSafeTimedSerializer we created in `util` at the
        # beginning of the chapter
        token = ts.dumps(user.email, salt='recover-key')

        recover_url = url_for(
            'auth.reset_with_token',
            token=token,
            _external=True)


        # html = render_template('email/recover.html', recover_url=recover_url)

        from flask_mail import Message
        from app import mail

        msg = Message(subject, sender="bimbau@rub.de", recipients=[user.email])
        msg.html = '<a href='+recover_url+'>Hier klicken, um ihr Passwort zurückzusetzen</a>'
        mail.send(msg)

        return redirect(url_for('main.index'))
    return render_template('auth/reset.html', form=form)


@auth.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        abort(404)

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()

        user.password = form.password.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('auth/reset_with_token.html', form=form, token=token)
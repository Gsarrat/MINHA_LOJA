from flask import render_template, session, request, redirect, url_for, flash
from loja.produtos.models import Addproduto, Marca, Categoria
from loja import app, db, bcrypt
from .forms import RegistrationForm, LoginFormulario
from .models import User
import os


@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Favor realizar seu login primeiro!!!')
        return redirect(url_for('login'))
    produtos = Addproduto.query.all()
    return render_template('admin/index.html', title='pagina administrativa', produtos=produtos)

@app.route('/marcas')
def marcas():
    if 'email' not in session:
        flash(f'Favor realizar seu login primeiro!!!')
        return redirect(url_for('login'))
    marcas = Marca.query.order_by(Marca.id.desc()).all()
    return render_template('admin/marca.html', title='Pagina Marcas', marcas=marcas)

@app.route('/categoria')
def categoria():
    if 'email' not in session:
        flash(f'Favor realizar seu login primeiro!!!')
        return redirect(url_for('login'))
    categorias = Categoria.query.order_by(Categoria.id.desc()).all()
    return render_template('admin/marca.html', title='Pagina Categorias', categorias=categorias)

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Obrigado{form.name.data} por se Registar', 'success')

        return redirect(url_for('login'))
    return render_template('ADMIN/registrar.html', form=form, title="Pagina de registros")


@app.route('/login', methods=['GET','POST'])
def login():
    form=LoginFormulario(request.form)
    if request.method == "POST" and form.validate():
        user= User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Olá {form.email.data} voce está logado', 'success')
            return redirect(request.args.get('next')or url_for('admin'))
        else:
            flash('NAO FOI POSSIVEL LOGAR')
    return render_template('ADMIN/login.html', form=form, title='Pagina Login')
from flask import redirect, render_template, url_for, flash, request, session, current_app
from loja import db, app, photos
from .forms import CadastroClienteForm
import secrets, os


@app.route('/cliente/cadastrar', methods=['GET', 'POST'])
def cadastrar_clientes():
    form = CadastroClienteForm(request.form)
    return render_template('/cliente/cliente.html', form=form)
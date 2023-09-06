from flask import redirect, render_template, url_for, flash, request, session, current_app
from .forms import Addprodutos
from loja import db, app, photos
from .models import Marca, Categoria, Addproduto
import secrets, os


@app.route('/addmarca', methods=['GET', 'POST'])
def addmarca():
    if 'email' not in session:
        flash(f'Favor realizar seu login primeiro!!!')
        return redirect(url_for('login'))

    if request.method == "POST":
        getmarca = request.form.get('marca')
        marca = Marca(name=getmarca)
        db.session.add(marca)
        flash(f'A Marca {getmarca}foi adiciona com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('addmarca'))
    return render_template('/produtos/addmarca.html', marcas='marcas')



@app.route('/updatemarca/<int:id>', methods=['GET', 'POST'])
def updatemarca(id):
    if 'email' not in session:
        flash(f'Favor realizar seu login primeiro!!!')
        return redirect(url_for('login'))
    updatemarca = Marca.query.get_or_404(id)
    marca = request.form.get('marca')
    if request.method=='POST':
        updatemarca.name = marca
        flash('Sua Marca foi Atualizada com Sucesso')
        db.session.commit()
        return redirect(url_for('marcas'))
    
    
    return render_template('/produtos/updatemarca.html', title='Atualizar Fabricantes', updatemarca=updatemarca)

###################################
@app.route('/deletemarca/<int:id>', methods=['POST'])
def deletemarca(id):

    marca = Marca.query.get_or_404(id)
    if request.method=='POST':
        db.session.delete(marca)
        db.session.commit()
        flash(f'A Marca {marca.name} foi Deletada com Sucesso', 'success')
        return redirect(url_for('admin'))
    flash(f'A Marca {marca.name} NAO foi Deletada', 'warning')
    return redirect(url_for('admin'))
    
###################################



@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def updatecat(id):
    if 'email' not in session:
        flash(f'Favor realizar seu login primeiro!!!')
        return redirect(url_for('login'))
    updatecat = Categoria.query.get_or_404(id)
    categoria = request.form.get('categoria')
    if request.method=='POST':
        updatecat.name = categoria
        flash('Sua Categoria foi Atualizada com Sucesso')
        db.session.commit()
        return redirect(url_for('categoria'))
    
    
    return render_template('/produtos/updatemarca.html', title='Atualizar Categoria', updatecat=updatecat)



@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if 'email' not in session:
        flash(f'Favor realizar seu login primeiro!!!')
        return redirect(url_for('login'))

    if request.method == "POST":
        getcat = request.form.get('categoria')
        cat = Categoria(name=getcat)
        db.session.add(cat)
        flash(f'A Categoria {getcat}foi adiciona com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('/produtos/addmarca.html')

@app.route('/deletecategoria/<int:id>', methods=['POST'])
def deletecategoria(id):

    categoria = Categoria.query.get_or_404(id)
    if request.method=='POST':
        db.session.delete(categoria)
        db.session.commit()
        flash(f'A Categoria {categoria.name} foi Deletada com Sucesso', 'success')
        return redirect(url_for('admin'))
    flash(f'A Categoria {categoria.name} NAO foi Deletada', 'warning')
    return redirect(url_for('admin'))
    


@app.route('/updateproduto/<int:id>', methods=['GET', 'POST'])
def updateproduto(id):

    marcas = Marca.query.all()
    categorias = Categoria.query.all()
    produto = Addproduto.query.get_or_404(id)
    marca = request.form.get('marca')
    categoria = request.form.get('categoria')
    form = Addprodutos(request.form)
    if request.method=="POST":

        produto.name = form.name.data
        produto.price = form.price.data
        produto.discount = form.discount.data
        produto.stock = form.stock.data
        produto.colors = form.colors.data
        produto.desc = form.discription.data

        produto.marca_id = marca
        produto.categoria_id = categoria

        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "'static/images/" + produto.image_1))
                produto.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+".")
            except:
                produto.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+".")
        
        if request.files.get('image_2'): 
            try:
                os.unlink(os.path.join(current_app.root_path, "'static/images/" + produto.image_2))
                produto.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+".")
            except:
                produto.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+".")
        
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "'static/images/" + produto.image_3))
                produto.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+".")
            except:
                produto.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+".")

 

        db.session.commit()
        flash('Produto foi Atualizado com Successo', 'success')

        return redirect(url_for('admin'))


    form.name.data = produto.name
    form.price.data = produto.price
    form.discount.data = produto.discount
    form.stock.data = produto.stock
    form.colors.data = produto.colors
    form.discription.data = produto.desc
      
    return render_template('/produtos/updateproduto.html', title='Atualizar Produtos', form=form, marcas=marcas, categorias=categorias, produto=produto)









@app.route('/addproduto', methods=['GET', 'POST'])
def addproduto():
    if 'email' not in session:
        flash(f'Favor realizar seu login primeiro!!!')
        return redirect(url_for('login'))
    marcas = Marca.query.all()
    categorias = Categoria.query.all()
    form = Addprodutos(request.form)
    if request.method == "POST":


        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.discription.data
        marca = request.form.get('marca')
        categoria = request.form.get('categoria')

        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+".")

        addpro = Addproduto(name=name,price=price,discount=discount,stock=stock,colors=colors,desc=desc, marca_id=marca, categoria_id=categoria, image_1=image_1, image_2=image_2, image_3=image_3)
        db.session.add(addpro)

        flash(f'O Produto {name} foi cadastrado com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('produtos/addproduto.html', title="Cadastrar Produtos", form=form, marcas=marcas, categorias=categorias)


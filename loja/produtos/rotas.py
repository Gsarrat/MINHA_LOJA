from flask import redirect, render_template, url_for, flash, request, session, current_app
from .forms import Addprodutos
from loja import db, app, photos
from .models import Marca, Categoria, Addproduto
import secrets, os


def marcas():
    marcas = marcas = Marca.query.join(Addproduto, (Marca.id == Addproduto.marca_id)).all()
    return marcas

def categorias():
    categorias = Categoria.query.join(Addproduto, (Categoria.id == Addproduto.categoria_id)).all()
    return categorias

@app.route('/')
def home():
    pagina = request.args.get('pagina',1, type=int)
    produtos = Addproduto.query.filter(Addproduto.stock > 0).order_by(Addproduto.id.desc()).paginate(page=pagina, per_page=8)
    return render_template('produtos/index.html', produtos=produtos, marcas=marcas(), categorias=categorias())

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method=='POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        produtos = Addproduto.query.filter(Addproduto.name.like(search)).all()
        return render_template('pesquisar.html', produtos=produtos, marcas=marcas(), categorias=categorias())
    else:
        return redirect('/')


@app.route('/marca/<int:id>')
def get_marca(id):
    get_m = Marca.query.filter_by(id=id).first_or_404()
    pagina = request.args.get('pagina',1, type=int)
    marca = Addproduto.query.filter_by(marca=get_m).paginate(page=pagina, per_page=8)
    return render_template('/produtos/index.html', marca=marca, marcas=marcas(), categorias=categorias(), get_m=get_m)

@app.route('/produto/<int:id>')
def pagina_unica(id):
    produto = Addproduto.query.get_or_404(id)
    return render_template('/produtos/pagina_unica.html', produto=produto, marcas=marcas(), categorias=categorias())

@app.route('/categorias/<int:id>')
def get_categoria(id):
    pagina = request.args.get('pagina',1, type=int)
    get_cat = Categoria.query.filter_by(id=id).first_or_404()
    get_cat_prod = Addproduto.query.filter_by(categoria=get_cat).paginate(page=pagina, per_page=8)
    return render_template('/produtos/index.html', get_cat_prod=get_cat_prod, categorias=categorias(), marcas=marcas(), get_cat=get_cat)



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




@app.route('/deleteproduto/<int:id>', methods=['POST'])
def deleteproduto(id):

    produto = Addproduto.query.get_or_404(id)
    if request.method=='POST':

        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "'static/images/" + produto.image_1))
                os.unlink(os.path.join(current_app.root_path, "'static/images/" + produto.image_2))
                os.unlink(os.path.join(current_app.root_path, "'static/images/" + produto.image_3))
            except Exception as e:
                print(e)

        db.session.delete(produto)
        db.session.commit()
        return redirect(url_for('admin'))
    flash(f'O Produto {produto.name} foi cadastrado com sucesso', 'success')

    return redirect(url_for('admin'))
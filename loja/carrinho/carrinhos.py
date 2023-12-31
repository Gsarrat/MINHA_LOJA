from flask import render_template, session, request, redirect, url_for, flash, current_app
from loja import db, app
from loja.produtos.models import Addproduto
from loja.produtos.rotas import marcas, categorias
import json
import mercadopago


def M_Dicionarios(dic1, dic2):
    if isinstance(dic1, list) and isinstance(dic2, list):
        return dic1 + dic2
    elif isinstance(dic1, dict) and isinstance(dic2, dict):
        return dict(list(dic1.items()) + list(dic2.items()))
    return False

@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        produto_id = request.form.get('produto_id')
        quantity = int(request.form.get('quantity'))
        colors = request.form.get('colors')
        produto = Addproduto.query.filter_by(id=produto_id).first()

        if produto_id and quantity and colors and request.method == "POST":
            DicItems = {produto_id: {
                'name': produto.name,
                'price': produto.price,
                'discount': produto.discount,
                'colors': produto.colors,
                'quantity': int(quantity),
                'image_1': produto.image_1
            }}
            if 'LojainCarrinho' in session:
                print(session['LojainCarrinho'])
                if produto_id in session['LojainCarrinho']:
                    if produto_id in session['LojainCarrinho']:
                        for key, item in session['LojainCarrinho'].items():
                            if int(key) == int(produto_id):
                                session.modified = True
                                item['quantity'] += 1
                else:
                    session['LojainCarrinho'] = M_Dicionarios(session['LojainCarrinho'], DicItems)
                    return redirect(request.referrer)
            else:
                session['LojainCarrinho'] = DicItems
                return redirect(request.referrer)
    
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@app.route('/carros')
def getCart():
    if 'LojainCarrinho' not in session or len(session['LojainCarrinho']) <=0:
        return redirect(url_for('home'))
    subtotal = 0
    valorpagar = 0
    for key, produto in session['LojainCarrinho'].items():
        discount = (produto['discount']/100) * float(produto['price'])
        subtotal += float(produto['price']) * int(produto['quantity'])
        subtotal -= discount 
        imposto = ("%.2f"% (.00 * float(subtotal))) # <----- aqui altera a aliquota de imposto a ser calculado no .00
        valorpagar = float("%.2f" %(1.06 * subtotal))
    return render_template('produtos/carros.html' , imposto=imposto, valorpagar=valorpagar, marcas=marcas(), categorias=categorias())

@app.route('/updateCarro/<int:code>', methods=['POST'])
def updateCarro(code):
    if 'LojainCarrinho' not in session or len(session['LojainCarrinho'])<= 0:
        return redirect(url_for('home'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key, item in session['LojainCarrinho'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash('Item foi atualizado com sucesso!')
                    return redirect(url_for('getCart'))

        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))
        



@app.route('/deleteiten/<int:id>')
def deleteiten(id):
    if 'LojainCarrinho' not in session or len(session['LojainCarrinho'])<= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['LojainCarrinho'].items():
            if int(key) == id:
                session['LojainCarrinho'].pop(key,None)
                flash('Item foi Deletado com sucesso!')
                return redirect(url_for('getCart'))

    except Exception as e:
            print(e)
            return redirect(url_for('getCart'))




@app.route('/limparcarro')
def limparcarro():
    try:
        session.pop('LojainCarrinho',None)
        return redirect(url_for('home'))
    
    except Exception as e:
            print(e)

###############################################################################################################################



@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    AccessToken = "APP_USR-6790317510701094-091914-b61e81dbfbd07b1d28b23ca375636511-136080481"
    sdk = mercadopago.SDK(AccessToken)

    # Lista do carrinho
    items = []
    for key, item in session.get('LojainCarrinho', {}).items():
        items.append({
            "id": key,
            "title": item['name'],
            "quantity": item['quantity'],
            "unit_price": float(item['price']),  # Certifique-se de que o preço seja um número
            "currency_id": "BRL",  # Defina a moeda apropriada
            "picture_url": item['image_1'],
        })
    # Criar a preferência
    preference_data = {
        "items": items,
    }
    print(items)
    try:
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        # Redirecionamento para o link de pagamento
        return redirect(preference["sandbox_init_point"])# Ou use a URL correta para produção
    except Exception as e:
        print(e)


###############################################################################################################################
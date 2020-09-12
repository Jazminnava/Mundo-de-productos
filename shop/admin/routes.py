from flask import render_template,session,request,redirect,url_for,flash,current_app
from shop import app, db,bcrypt
from .forms import RegistrationForm,LoginForm
from shop.products.models import Addproduct,Brand,Category,Vendedor,Dueño,Administrador,Cliente,Venta
from flask_login import login_required,current_user, logout_user,login_user
from .models import User
from shop.customers.model import CustomerOrder

import secrets
import os
import json



@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Porfavor Ingesar Al Sistema','danger')
        return redirect(url_for('login'))
    products =Addproduct.query.all()
    return render_template('admin/index.html',title="Administrador",products=products)


@app.route('/brands')
def brands():
    if 'email' not in session:
        flash(f'Porfavor Ingesar Al Sistema','danger')
        return redirect(url_for('login'))
    brands=Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html',title="Pagina de marca",brands=brands)




@app.route('/category')
def categories():
    if 'email' not in session:
        flash(f'Porfavor Ingesar Al Sistema','danger')
        return redirect(url_for('login'))
    categories=Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html',title="Pagina de categoria",categories=categories)


@app.route('/vendedor')
def vendedores():
    if 'email' not in session:
        flash(f'Porfavor Ingesar Al Sistema','danger')
        return redirect(url_for('login'))
    vendedores=Vendedor.query.order_by(Vendedor.id.desc()).all()
    return render_template('admin/vendedor.html',title="Pagina del vendedor",vendedores=vendedores)


@app.route('/dueño')
def dueños():
    if 'email' not in session:
        flash(f'Porfavor Ingesar Al Sistema','danger')
        return redirect(url_for('login'))
    dueños=Dueño.query.order_by(Dueño.id.desc()).all()
    return render_template('admin/dueño.html',title="Pagina dueño",dueños=dueños)



@app.route('/administrador')
def administradores():
    if 'email' not in session:
        flash(f'Porfavor Ingesar Al Sistema','danger')
        return redirect(url_for('login'))
    administradores=Administrador.query.order_by(Administrador.id.desc()).all()
    return render_template('admin/administrador.html',title="Pagina administrador",administradores=administradores)

@app.route('/cliente')
def clientes():
    if 'email' not in session:
        flash(f'Porfavor Ingesar Al Sistema','danger')
        return redirect(url_for('login'))
    clientes=Cliente.query.order_by(Cliente.id.desc()).all()
    return render_template('admin/cliente.html',title="Pagina del cliente",clientes=clientes)


@app.route('/venta')
def ventas():
    if 'email' not in session:
        flash(f'Porfavor Ingesar Al Sistema','danger')
        return redirect(url_for('login'))
    ventas=Venta.query.order_by(Venta.id.desc()).all()
    return render_template('admin/venta.html',title="Pagina de venta",ventas=ventas)


@app.route('/user')
def users():
    if 'email' not in session:
        flash(f'Porfavor Ingesar Al Sistema','danger')
        return redirect(url_for('login'))
    users=User.query.order_by(User.id.desc()).all()
    return render_template('admin/user.html',title="Pagina usuario",users=users)

@app.route('/CustomerOrder')
def CustomerOrders():
    if 'email' not in session:
        flash(f'Porfavor Ingesar Al Sistema','danger')
        return redirect(url_for('login'))
    CustomerOrders=CustomerOrder.query.order_by(CustomerOrder.id.desc()).all()
    return render_template('admin/CustomerOrders.html',title="Pagina Orden del cliente",CustomerOrders=CustomerOrders)

#Registrar

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
    	hash_password=bcrypt.generate_password_hash(form.password.data)
    	user=User(username=form.username.data,name=form.name.data,email=form.email.data,password=hash_password)
    	db.session.add(user)
    	db.session.commit()
    	flash(f'{form.name.data} Gracias Por Registrarte','success')
    	return redirect(url_for('login'))
    return render_template('admin/register.html',form=form,title='Pagina de registro')



@app.route('/login',methods=['GET','POST'])
def login():
    form =LoginForm(request.form)
    if request.method=="POST" and form.validate():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            session['email']=form.email.data
            flash(f'Bienvenido{form.email.data} ya estas registrado','success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash(f'Intentar de nuevo','danger')
    return render_template('admin/login.html',form=form,title="Pagina de Login")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
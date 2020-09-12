from flask import redirect,render_template,url_for,flash,request,session,current_app
from shop import db,app,photos
from .models import Brand,Category,Vendedor,Addproduct,Dueño,Administrador,Cliente,Venta
from .forms import Addproducts,Vendedores,Vendedores,Dueños,Administradores,Clientes,Ventas
import secrets
import os

def brands():
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return brands

def categories():
    categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return categories


@app.route('/')
def home():
	page=request.args.get('page',1,type=int)
	products=Addproduct.query.filter(Addproduct.stock>0).order_by(Addproduct.id.desc()).paginate(page=page,per_page=6)
	return render_template('products/index.html', products=products,title="Pagina",brands=brands(),categories=categories())


@app.route('/product/<int:id>')
def single_page(id):
	product=Addproduct.query.get_or_404(id)

	return render_template('products/single_page.html',product=product,brands=brands(),categories=categories())


@app.route('/brand/<int:id>')
def get_brand(id):
	page=request.args.get('page',1,type=int)
	get_b=Brand.query.filter_by(id=id).first_or_404()
	brand=Addproduct.query.filter_by(brand=get_b).paginate(page=page,per_page=4)
	return render_template('products/index.html',get_b=get_b,title="Pagina",brand=brand,brands=brands(),categories=categories())

@app.route('/categories/<int:id>')
def get_category(id):
	page=request.args.get('page',1,type=int)
	get_cat=Category.query.filter_by(id=id).first_or_404()
	get_cat_prod=Addproduct.query.filter_by(category=get_cat).paginate(page=page,per_page=4)

	return render_template('products/index.html',get_cat=get_cat, title="Pagina",get_cat_prod=get_cat_prod,categories=categories(),brands=brands())



@app.route('/addbrand',methods=['GET','POST'])
def addbrand():
	if 'email' not in session:
		flash(f'Porfavor Ingesar Al Sistema','danger')
		return redirect(url_for('login'))
	if request.method=="POST":
		getbrand = request.form.get('brand')
		brand=Brand (name=getbrand)
		db.session.add(brand)
		flash(f'La marca {getbrand} fue agregada correctamente','success')
		db.session.commit()
		return redirect(url_for('addbrand'))
	return render_template('products/addbrand.html',title="Marca",brands='brands')


@app.route('/updatebrand/<int:id>', methods=['GET','POST'])
def updatebrand(id):
	if  'email' not in  session:
		flash(f'Porfavor Ingesar Al Sistema','danger')
	updatebrand=Brand.query.get_or_404(id)
	brand=request.form.get('brand')
	if request.method=="POST":
		updatebrand.name=brand
		flash(f'La marca ha sido Actualizada','success')
		db.session.commit()
		return redirect(url_for('brands'))
	return render_template('products/updatebrand.html',title='Actualizar Marca',updatebrand=updatebrand)

@app.route('/deletebrand/<int:id>', methods=['POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(brand)
        flash(f"La Marca {brand.name} Se elimino correctamente","success")
        db.session.commit()
        return redirect(url_for('admin'))
    flash(f"La Marca {brand.name} No Pudo Borrarse correctamente","warning")
    return redirect(url_for('admin'))




@app.route('/addcategory',methods=['GET','POST'])
def addcategory():
	if 'email' not in session:
		flash(f'Porfavor Ingesar Al Sistema','danger')
		return redirect(url_for('login'))
	if request.method=="POST":
		getbrand = request.form.get('category')
		category=Category(name=getbrand)
		db.session.add(category)
		flash(f'La marca {getbrand} fue agregada correctamente','success')
		db.session.commit()
		return redirect(url_for('addcategory'))
	return render_template('products/addbrand.html',title="Categorias")



@app.route('/updatecategory/<int:id>', methods=['GET','POST'])
def updatecategory(id):
	if  'email' not in  session:
		flash(f'Porfavor Ingesar Al Sistema','danger')
	updatecategory=Category.query.get_or_404(id)
	category=request.form.get('category')
	if request.method=="POST":
		updatecategory.name=category
		flash(f'La categoria ha sido actualizada correctamente','success')
		db.session.commit()
		return redirect(url_for('categories'))
	return render_template('products/updatebrand.html',title='Actualizar categoria',updatecategory=updatecategory)

@app.route('/deletecategory/<int:id>', methods=['POST'])
def deletecategory(id):
    category = Category.query.get_or_404(id)
    if request.method=="POST":

        db.session.delete(category)
        flash(f"The categoria {category.name} ha sido elimiada correctamente","success")
        db.session.commit()
        return redirect(url_for('admin'))
    flash(f"The categoria {category.name} no se pudo eliminar","warning")
    return redirect(url_for('admin'))

#Crear productos

@app.route('/addproduct',methods=['GET','POST'])
def addproduct():
	if 'email' not in session:
		flash(f'Porfavor Ingesar Al Sistema','danger')
		return redirect(url_for('login'))
	brands= Brand.query.all()
	categories = Category.query.all()
	form=Addproducts(request.form)
	if request.method =="POST":
		name=form.name.data
		price=form.price.data
		discount=form.discount.data
		stock=form.stock.data
		colors=form.color.data
		desc=form.discription.data
		brand=request.form.get('brand')
		category=request.form.get('category')
		
		image_1=photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+ ".")
		image_2=photos.save(request.files.get('image_2'),name=secrets.token_hex(10)+ ".")
		image_3=photos.save(request.files.get('image_3'),name=secrets.token_hex(10)+ ".")
		addpro=Addproduct(name=name,price=price,discount=discount,stock=stock,colors=colors,desc=desc,
		brand_id=brand,category_id=category,image_1=image_1,image_2=image_2,image_3=image_3)
		db.session.add(addpro)
		flash(f'El producto {name} ha sido registrado ','success')
		db.session.commit()
		#db.session.commit()
		return redirect(url_for('admin'))
	return render_template('products/addproduct.html',title="Agregar producto",form=form, brands=brands,categories=categories)



@app.route('/updateproduct/<int:id>',methods=['GET','POST'])
def updateproduct(id):
	brands=Brand.query.all()
	categories=Category.query.all()
	product=Addproduct.query.get_or_404(id)
	brand=request.form.get('brand')
	category=request.form.get('category')
	form=Addproducts(request.form)
	if request.method=='POST':
		product.name=form.name.data
		product.price=form.price.data
		product.discount=form.discount.data
		product.brand_id=brand
		product.category_id=category
		product.colors=form.color.data
		product.stock=form.stock.data
		product.desc=form.discription.data
		if request.files.get('image_1'):
			try:
				os.unlink(os.path.join(current_app.root_path,"static/images/"+product.image_1))
				product.image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")
			except:
				product.image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")

		if request.files.get('image_2'):
			try:
				os.unlink(os.path.join(current_app.root_path,"static/images/"+ product.image_2))
				product.image_2=photos.save(request.files.get('image_2'),name=secrets.token_hex(10)+".")
			except:  
				product.image_2 = photos.save(request.files.get('image_2'),name=secrets.token_hex(10)+".")
		if request.files.get('image_3'):
			try:
				os.unlink(os.path.join(current_app.root_path,"static/images/"+ product.image_3))
				product.image_3=photos.save(request.files.get('image_3'),name=secrets.token_hex(10)+".")
			except:
				product.image_3=photos.save(request.files.get('image_3'),name=secrets.token_hex(10)+".")
		db.session.commit()
		flash(f'you product has been updated','success')
		return redirect(url_for('admin'))


	form.name.data=product.name
	form.price.data=product.price 
	form.discount.data=product.discount 
	form.stock.data=product.stock 
	form.color.data=product.colors
	form.discription.data=product.desc 
	

	
	return render_template('products/updateproduct.html',title="Actualizar Productos",form=form,brands=brands,categories=categories,product=product)


@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
           
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'El producto {product.name} esta eliminado','success')
        return redirect(url_for('admin'))
    flash(f'No lo puedes eliminar','success')
    return redirect(url_for('admin'))







@app.route('/addvendedor',methods=['GET','POST'])
def addvendedor():
	if 'email' not in session:
		flash(f'Porfavor Ingesar Al Sistema','danger')
		return redirect(url_for('login'))
	form=Vendedores(request.form)
	if request.method =="POST":
		name=form.name.data
		apellidop=form.apellidop.data
		apellidom=form.apellidom.data
		edad=form.edad.data
		telefono=form.telefono.data
		calle=form.calle.data
		colonia=form.colonia.data
		numdire=form.numdire.data
		image_1=photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+ ".")
		addven=Vendedor(name=name,apellidop=apellidop,apellidom=apellidom,edad=edad,telefono=telefono,calle=calle,
		colonia=colonia,numdire=numdire,image_1=image_1)
		db.session.add(addven)
		flash(f'El Vendedor {name} ha sido registrado ','success')
		db.session.commit()
		#db.session.commit()
		return redirect(url_for('admin'))
	return render_template('products/addvendedor.html',title="pagina del vendedor",form=form)



@app.route('/updatevendedor/<int:id>',methods=['GET','POST'])
def updatevendedor(id):
	vendedor=Vendedor.query.get_or_404(id)
	form=Vendedores(request.form)
	if request.method=='POST':
		vendedor.name=form.name.data
		vendedor.apellidop=form.apellidop.data
		vendedor.apellidom=form.apellidom.data
		vendedor.edad=form.edad.data
		vendedor.telefono=form.telefono.data
		vendedor.calle=form.calle.data
		vendedor.colonia=form.colonia.data
		vendedor.numdire=form.numdire.data
		if request.files.get('image_1'):
			try:
				os.unlink(os.path.join(current_app.root_path,"static/images/"+vendedor.image_1))
				vendedor.image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")
			except:
				vendedor.image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")

		db.session.commit()
		flash(f'you product has been updated','success')
		return redirect(url_for('admin'))


	form.name.data=vendedor.name
	form.apellidop.data=vendedor.apellidop 
	form.apellidom.data=vendedor.apellidom 
	form.edad.data=vendedor.edad 
	form.telefono.data=vendedor.telefono
	form.calle.data=vendedor.calle 
	form.colonia.data=vendedor.colonia 
	form.numdire.data=vendedor.numdire 
	form.calle.data=vendedor.calle 



	return render_template('products/updatevendedor.html',title="Actualizar Vendedor",form=form)




@app.route('/deletevendedor/<int:id>', methods=['POST'])
def deletevendedor(id):
    vendedor = Vendedor.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + vendedor.image_1))
           
        except Exception as e:
            print(e)
        db.session.delete(vendedor)
        db.session.commit()
        flash(f'The product {vendedor.name} was delete from your record','success')
        return redirect(url_for('admin'))
    flash(f'Can not delete the product','success')
    return redirect(url_for('admin'))




@app.route('/adddueño',methods=['GET','POST'])
def adddueño():
	if 'email' not in session:
		flash(f'Porfavor Ingesar Al Sistema','danger')
		return redirect(url_for('login'))
	form=Dueños(request.form)
	if request.method =="POST":
		name=form.name.data
		apellidop=form.apellidop.data
		apellidom=form.apellidom.data
		edad=form.edad.data
		telefono=form.telefono.data
		calle=form.calle.data
		colonia=form.colonia.data
		numdire=form.numdire.data
		image_1=photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+ ".")
		adddue=Vendedor(name=name,apellidop=apellidop,apellidom=apellidom,edad=edad,telefono=telefono,calle=calle,
		colonia=colonia,numdire=numdire,image_1=image_1)
		db.session.add(adddue)
		flash(f'El Dueño {name} ha sido registrado ','success')
		db.session.commit()
		return redirect(url_for('admin'))
	return render_template('products/adddueño.html',title="pagina del Dueño",form=form)





@app.route('/addcliente',methods=['GET','POST'])
def addcliente():
	if 'email' not in session:
		flash(f'Porfavor Ingesar Al Sistema','danger')
		return redirect(url_for('login'))
	form=Clientes(request.form)
	if request.method =="POST":
		name=form.name.data
		apellidop=form.apellidop.data
		apellidom=form.apellidom.data
		edad=form.edad.data
		telefono=form.telefono.data
		calle=form.calle.data
		colonia=form.colonia.data
		numdire=form.numdire.data
		image_1=photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+ ".")
		addclie=Cliente(name=name,apellidop=apellidop,apellidom=apellidom,edad=edad,telefono=telefono,calle=calle,
		colonia=colonia,numdire=numdire,image_1=image_1)
		db.session.add(addclie)
		flash(f'El Cliente {name} ha sido registrado ','success')
		db.session.commit()
		#db.session.commit()
		return redirect(url_for('admin'))
	return render_template('products/addcliente.html',title="pagina del cliente",form=form)


@app.route('/updatecliente/<int:id>',methods=['GET','POST'])
def updatecliente(id):
	cliente=Cliente.query.get_or_404(id)
	form=Clientes(request.form)
	if request.method=='POST':
		cliente.name=form.name.data
		cliente.apellidop=form.apellidop.data
		cliente.apellidom=form.apellidom.data
		cliente.edad=form.edad.data
		cliente.telefono=form.telefono.data
		cliente.calle=form.calle.data
		cliente.colonia=form.colonia.data
		cliente.numdire=form.numdire.data
		if request.files.get('image_1'):
			try:
				os.unlink(os.path.join(current_app.root_path,"static/images/"+cliente.image_1))
				cliente.image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")
			except:
				cliente.image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")

		db.session.commit()
		flash(f'El cliente se actualizo','success')
		return redirect(url_for('admin'))


	form.name.data=cliente.name
	form.apellidop.data=cliente.apellidop 
	form.apellidom.data=cliente.apellidom 
	form.edad.data=cliente.edad 
	form.telefono.data=cliente.telefono
	form.calle.data=cliente.calle 
	form.colonia.data=cliente.colonia 
	form.numdire.data=cliente.numdire 
	form.calle.data=cliente.calle 



	return render_template('products/updatecliente.html',title="Actualizar cliente",form=form)


@app.route('/deletecliente/<int:id>', methods=['POST'])
def deletecliente(id):
    cliente = Cliente.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + cliente.image_1))
           
        except Exception as e:
            print(e)
        db.session.delete(cliente)
        db.session.commit()
        flash(f'El producto {cliente.name} ha sido eliminado','success')
        return redirect(url_for('admin'))
    flash(f'No se peude eliminar','success')
    return redirect(url_for('admin'))






@app.route('/addadministrador',methods=['GET','POST'])
def addadministrador():
	if 'email' not in session:
		flash(f'Porfavor Ingesar Al Sistema','danger')
		return redirect(url_for('login'))
	form=Administradores(request.form)
	if request.method =="POST":
		name=form.name.data
		apellidop=form.apellidop.data
		apellidom=form.apellidom.data
		edad=form.edad.data
		telefono=form.telefono.data
		calle=form.calle.data
		colonia=form.colonia.data
		numdire=form.numdire.data
		image_1=photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+ ".")
		addadm=Administrador(name=name,apellidop=apellidop,apellidom=apellidom,edad=edad,telefono=telefono,calle=calle,
		colonia=colonia,numdire=numdire,image_1=image_1)
		db.session.add(addadm)
		flash(f'El Administrador {name} ha sido registrado ','success')
		db.session.commit()
		#db.session.commit()
		return redirect(url_for('admin'))
	return render_template('products/addadministrador.html',title="pagina del Administrador",form=form)


@app.route('/updateadministrador/<int:id>',methods=['GET','POST'])
def updateadministrador(id):
	administrador=Administrador.query.get_or_404(id)
	form=Administradores(request.form)
	if request.method=='POST':
		administrador.name=form.name.data
		administrador.apellidop=form.apellidop.data
		administrador.apellidom=form.apellidom.data
		administrador.edad=form.edad.data
		administrador.telefono=form.telefono.data
		administrador.calle=form.calle.data
		administrador.colonia=form.colonia.data
		administrador.numdire=form.numdire.data
		if request.files.get('image_1'):
			try:
				os.unlink(os.path.join(current_app.root_path,"static/images/"+administrador.image_1))
				administrador.image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")
			except:
				administrador.image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")

		db.session.commit()
		flash(f'El cliente se actualizo','success')
		return redirect(url_for('admin'))


	form.name.data=administrador.name
	form.apellidop.data=administrador.apellidop 
	form.apellidom.data=administrador.apellidom 
	form.edad.data=administrador.edad 
	form.telefono.data=administrador.telefono
	form.calle.data=administrador.calle 
	form.colonia.data=administrador.colonia 
	form.numdire.data=administrador.numdire 
	form.calle.data=administrador.calle 



	return render_template('products/updateadministrador.html',title="Actualizar administrador",form=form)


@app.route('/deleteadministrador/<int:id>', methods=['POST'])
def deleteadministrador(id):
    administrador = Administrador.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + administrador.image_1))
           
        except Exception as e:
            print(e)
        db.session.delete(administrador)
        db.session.commit()
        flash(f'EL producto {administrador.name} ha sido eliminado','success')
        return redirect(url_for('admin'))
    flash(f'No se puedo eliminar','success')
    return redirect(url_for('admin'))



@app.route('/addventa',methods=['GET','POST'])
def addventa():
	if 'email' not in session:
		flash(f'Porfavor Ingesar Al Sistema','danger')
		return redirect(url_for('login'))
	clientes= Cliente.query.all()
	vendedores= Vendedor.query.all()
	addproducts= Addproduct.query.all()
	form=Ventas(request.form)
	if request.method =="POST":
		name=form.name.data
		precio=form.precio.data
		total=form.total.data
		cliente=request.form.get('cliente')
		vendedor=request.form.get('vendedor')
		addproduct=request.form.get('addproduct')
		addven=Venta(name=name,precio=precio,total=total,cliente_id=cliente,vendedor_id=vendedor,addproduct_id=addproduct)
		db.session.add(addven)
		flash(f'La venta ha sido reregistrada ','success')
		db.session.commit()
		return redirect(url_for('admin'))



	return render_template('products/addventa.html',title="producto pagina",form=form,clientes=clientes,vendedores=vendedores,addproducts=addproducts)


@app.route('/updateventa/<int:id>',methods=['GET','POST'])
def updateventa(id):
	clientes=Cliente.query.all()
	vendedores=Vendedor.query.all()
	addproducts=Addproduct.query.all()
	venta=Venta.query.get_or_404(id)
	cliente=request.form.get('cliente')
	vendedor=request.form.get('vendedor')
	addproduct=request.form.get('addproduct')
	form=Ventas(request.form)
	if request.method=='POST':
		venta.name=form.name.data
		venta.precio=form.precio.data
		venta.total=form.total.data	
		venta.cliente_id=cliente
		venta.vendedor_id=vendedor
		venta.addproduct_id=addproduct
		db.session.commit()
		flash(f'La venta se actualizo','success')
		return redirect(url_for('admin'))
	form.name.data=venta.name
	form.precio.data=venta.precio 
	form.total.data=venta.total 

	return render_template('products/updateventa.html',title="Actualizar Productos",form=form,clientes=clientes,vendedores=vendedores,addproducts=addproducts,venta=venta)


@app.route('/deleteventa/<int:id>', methods=['POST'])
def deleteventa(id):
    venta = Venta.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + venta.image_1))
           
        except Exception as e:
            print(e)
        db.session.delete(venta)
        db.session.commit()
        flash(f'La venta {venta.name} ha sido eliminada  ','success')
        return redirect(url_for('admin'))
    flash(f'No se pudo eliminar','success')
    return redirect(url_for('admin'))








from wtforms import Form, BooleanField, StringField, PasswordField, validators

class RegistrationForm(Form):
    username = StringField('Nombre de Usuario:', [validators.Length(min=4, max=25)])
    name = StringField('Nombre Completo:', [validators.Length(min=4, max=25)])
    email = StringField('Dirección De Correo Electrónico:', [validators.Length(min=6, max=35),validators.Email()])
    password = PasswordField('Nueva Contraseña:', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repetir Contraseña:')



class LoginForm(Form):
	email = StringField('Correo Electrónico:', [validators.Length(min=6, max=35),validators.Email()])
	password = PasswordField('Contraseña:', [validators.DataRequired()])

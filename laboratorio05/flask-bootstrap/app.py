from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Link
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

SECRET_KEY = 'aula de BCD - string aleatória'

app = Flask(__name__)
app.secret_key = SECRET_KEY

bootstrap = Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exemplo-02.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

nav = Nav()
nav.init_app(app)   # menu no topo da página

@nav.navigation()
def menunav():
    menu = Navbar('Minha app web')
    menu.items = [View('Home',hello_world),View('Login','autenticar')]
    menu.items.append(Subgroup('Pessoa',View('Aluno','hello_world')))
    menu.items.append(Link('Pessoa','https://www.google.com.'))
    return menu


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key= True, autoincrement= True)
    username = db.Column(db.String(40))
    password = db.Column(db.String(130))
    email = db.Column(db.String(130))

    # def __init__(self,**kwargs):
    #     super.__init__(kwargs)
    #     self.username = kwargs.pop('username')
    #     self.email = kwargs.pop('email')
    #     self.password = generate_password_hash(kwargs.pop('password'))

    def set_password(self,password):
        self.password = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)

class LoginForm(FlaskForm):
    username = StringField('Nome do usuário',validators=[DataRequired()])
    password = PasswordField('Senha',validators=[DataRequired()])
    submit = SubmitField('Entrar')



@app.route('/login',methods=['GET','Post'])
def autenticar():
    formulario = LoginForm()
    if formulario.validate_on_submit():
         # fazer autenticação
        usuario = Usuario.query.filter_by(username=formulario.username.data).first_or_404()
        senha = formulario.password.data
        if(usuario.check_password(senha)):
            session['loged_in'] = True
            session['usuario'] = usuario.username
            return render_template('autenticado.html')
        return render_template('login.html',form=formulario)
    return render_template('login.html',form=formulario)

@app.route('/painel')
def painel():
    if session.get('logged_in'):
        usuario = Usuario.query.filter_by(username=session.get('usuario')).first_or_404()
        return render_template('dados.html',title="Usuário Autenticado", user=usuario)

    return redirect(url_for('hello_word'))

@app.route('/logout')
def sair():
    session['loged_in'] = False
    return redirect(url_for('autenticar'))


@app.route('/index')
@app.route('/')
def hello_world():

    return render_template('index.html')

if __name__ == '__main__':
    app.run()

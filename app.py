from flask import Flask, request, render_template, redirect, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, InputRequired, EqualTo, Email

app = Flask(__name__) 
app.config['SECRET_KEY'] = 'teste'

class CriarConta(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    nome_usuario = StringField('Nome de usuário')
    cpf = StringField('CPF')
    telefone = StringField('Telefone')
    email = StringField('E-mail', validators=[Email(message='E-mail inválido')])
    senha = PasswordField('Senha', validators=[InputRequired(), EqualTo('confirma_senha')])
    confirma_senha = PasswordField('Confirme sua Senha')
    
    enviar = SubmitField ('Criar Conta')

@app.route('/')
def inicio():
    return render_template("index.html")

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CriarConta()

    if form.validate_on_submit():
        return redirect('/')
    return render_template("cadastro.html", form = form )

@app.route('/entrar')
def entrar():
    return render_template("entrar.html")

if __name__ == '__main__':
    app.run(debug=True, port=5152)
#!flask/bin/python
from flask.views import View
from flask import Flask, abort, jsonify, request, make_response, url_for
from flask import render_template, redirect

app = Flask(__name__)

class ClassifyFormView(View):
    def dispatch_request(self):
        # templates located in templates directory by default
        return render_template('classificador.html')

#Convert that class into an actual view function by using the as_view() class method. 
#The string you pass to that function is the name of the endpoint that view will then have
app.add_url_rule('/classifier/api/v1.0/classifyForm/', view_func=ClassifyFormView.as_view('classifyForm'))

categories = [
    {
        'id': 1,
        'name': u'Centrais Telefonicas',
        
    },
    {
        'id': 2,
        'name': u'Computadores Mac',
        
    },
    {
        'id': 3,
        'name': u'Processadores',
        
    },
]

import lm_email_classifier as classifier

   #SEGURANCA
# from flask.ext.httpauth import HTTPBasicAuth
# auth = HTTPBasicAuth()

# @auth.get_password
# def get_password(username):
#     if username == 'santiago':
#         return 'python'
#     return None

# @auth.error_handler
# def unauthorized():
#     return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.route('/')
def index():
    #redirect to the about page
    return redirect('/classifier/api/v1.0/classifyForm')
    #return "Serviço de Classificação de email - CRM"


@app.route('/classifier/api/v1.0/categories', methods=['GET'])
def get_tasks():
    return jsonify({'categories': categories})


@app.route('/classifier/api/v1.0/classify/<string:email_content>', methods=['GET'])
def get_task(email_content):
    if len(email_content) == 0:
        abort(404)
    return jsonify({'category': str(classifier.predict_winner_email(email_content))})
    # return jsonify({'category': categories[0]})f



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)


 
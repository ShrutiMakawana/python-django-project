from flask import Flask,jsonify
app=Flask(__name__)

item=[
    {
       "name":"kurkure",
       "price":10,
    },
    {
        "name":"gopal",
        "price":20
    }
]
@app.route('/')
@app.route('/getitem')

def getitem():
    return {"items":item}

if __name__=="__main__" :
         app.run(debug=True)



# from flask import Flask,jsonify
# app = Flask(__name__)



# @app.route('/')
# def hello_world():
#     return 'Hello, World!'
# @app.route('/sum/<int:a>')
# def sum(a):
#     sum=   {
#       "a" : a
#     }
#     return jsonify(sum)


# if __name__=="__main__" :
#     app.run(debug=True)
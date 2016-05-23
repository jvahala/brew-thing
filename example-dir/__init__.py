from flask import Flask,render_template,request,json,url_for,redirect
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Testing123!'
app.config['MYSQL_DATABASE_DB'] = 'vahalalaland'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


'''
/ main page = vahalabout
/about/
/cv/
/blog/
/blog/post_name/
'''

#homepage related 
@app.route('/')
def index():
	return render_template('index.html')




#sign up / registration related
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp',methods=['GET','POST']) #says this routing will use the POST method, where import request is needed
def signUp():
	try: 
		# read the posted values from the UI
	    _name = request.form['inputName']
	    _email = request.form['inputEmail']
	    _password = request.form['inputPassword']
	    # validate the received values, requred import json, will see in javascript console: in chrome, cmd+option+j to open
	    if _name and _email and _password:

	    	conn = mysql.connect()
	        cursor = conn.cursor()
	        _hashed_password = generate_password_hash(_password)
	        cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
	        data = cursor.fetchall()

	        if len(data) is 0:
	        	conn.commit()
	        	return json.dumps({'status':'ok','message':'User created successfully !','redirect':url_for('about')})
	           	
	      	else:
	            return json.dumps({'error':str(data[0])})

	    else:
	        return json.dumps({'html':'<span>Enter the required fields</span>'})

	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cursor.close() 
		conn.close()


#about related
@app.route('/about/')
def about():
	return render_template('about.html')





#projects related
#examples for input expressions, int, float, and path types are allowed
@app.route('/projects/')
def show_cv():
    # show the user profile for that user
    return 'User %s' % username.title() #.title() makes it a captial first letter

@app.route('/squiggle/')
def squiggle(): 
	return render_template('squiggle_pad.html')

#blog related
@app.route('/blog/')
def blog():
	return 'blog goes here'

@app.route('/blog/<post_name>/')
def show_post(post_name):
    return 'post_name - maybe have date in the title'


#error related
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404  #flask automatically looks in the templates directory for this file




if __name__ == '__main__':
	#app.host = '0.0.0.0'
	app.run(debug = True)			#can pass 'host='0.0.0.0' to allow public access, never use debug on production machines


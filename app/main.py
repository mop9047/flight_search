from flask import Blueprint, render_template, request, session, redirect, url_for, current_app

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

# @main.route('/home')
# def home():
    
#     username = session['username']
#     cursor = current_app.config['db'].cursor();
#     query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
#     cursor.execute(query, (username))
#     data1 = cursor.fetchall() 
#     for each in data1:
#         print(each['blog_post'])
#     cursor.close()
#     return render_template('home.html', username=username, posts=data1)

@main.route('/home')
def home():
    
    username = session['username']
    cursor = current_app.config['db'].cursor();
    query = 'SELECT name,email FROM Customer WHERE email = %s'
    cursor.execute(query, (username))
    data1 = cursor.fetchall() 
    for each in data1:
        name = each['name']
        print(each['email'])
    cursor.close()
    return render_template('home.html', username=name, posts=data1)

		
@main.route('/post', methods=['GET', 'POST'])
def post():
	username = session['username']
	cursor = current_app.config['db'].cursor();
	blog = request.form['blog']
	query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
	cursor.execute(query, (blog, username))
	current_app.config['db'].commit()
	cursor.close()
	return redirect(url_for('main.home'))

@main.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')
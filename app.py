from flask import Flask, render_template, request, session, redirect, url_for, g
import sqlite3
import module

app = Flask(__name__)

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method=="GET":
		return render_template("login.html")
	else:
		#login form submission
		button = request.form['button']
		uname = request.form['username']
		pword = request.form['password']
		#cancel back to home page (can't see anything since no logged in)
		if button == "Cancel":
			return redirect(url_for('home'))
		#if credentials valid, log them in with session
		if module.authenticate(uname,pword):
			if 'n' not in session:
				session['n'] = 0
			return redirect(url_for('home'))
		#else renders login w/ error message
		else:
			return render_template("login.html",error="Invalid Username or Password")


@app.route('/logout', methods=['GET','POST'])
def logoff():
	#remove the username from the session if it's there
	session.pop('n', None)
	return redirect(url_for('login'))


@app.route("/home")
@app.route("/home/")
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/newStory", methods=['GET','POST'])
def nStory():
        if request.method=="GET":
                return render_template("new.html")
        else:
                username='test'
                button=request.form['button']
                title=request.form['sTitle']
                line=request.form['entry']
                if button=="Submit":
                        module.makePost(username, title, line)
                        return redirect('/story/%s' %title)
                else:
                        return render_template("new.html")
        return render_template("new.html")

@app.route("/story/<title>")
def story(title=""):
        return render_template("story.html", title=title, line=module.getPost(title))

if __name__ == "__main__":
	app.debug = True
	app.secret_key="c720minusboying"
	app.run(host='0.0.0.0', port=5000)








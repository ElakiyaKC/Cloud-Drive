from flask import Flask,render_template,session,request,redirect,url_for
import MySQLdb
import uuid
import os
from werkzeug.utils import secure_filename

host='####'
user='####'
password='####'
database='dbname'
basePath='/home/ubuntu/flaskapp/static'

db=MySQLdb.connect(host,user,password,database)


app = Flask(__name__)
app.secret_key = 'Sectet'
@app.route('/')
@app.route('/login',methods=['GET','POST'])
def login():
	if 'username' in session:
		return redirect(url_for('home'))
	if request.method == 'POST':
		username=request.form['username']
		password=request.form['password']
		sql="select userid from userdetails where username= %s and password=%s"
		cursor=db.cursor()
		args = (username,password)
		cursor.execute(sql,args)
		#print cursor.rowcount
		if int(cursor.rowcount) == 1 :
			row=cursor.fetchone()
			print row
			print row[0]
			session['username']=username
			session['userid']=row[0]
			return redirect(url_for('home'))
		else:
			return "Invalid Username/password"			
	return render_template("login.html")


@app.route('/register',methods=['GET','POST'])
def register():
	if 'username' in session:
		return redirect(url_for('home'))
	if request.method == 'POST':
		uuidValue=str(uuid.uuid1())
		username=request.form['username']
		password=request.form['password']
		sql="select 1 from userdetails where username= %s"
		cursor=db.cursor()
		args = (username,)
		cursor.execute(sql,args)
		#print cursor.rowcount
		if int(cursor.rowcount) > 0 :
			return "Username already exists"
		sql="insert into userdetails (userid,username,password) values ( %s,%s,%s)"
		args = (uuidValue,username,password,)
		
		cursor.execute(sql,args)
		db.commit()
		return redirect(url_for('home'))
	return render_template("register.html")

@app.route('/home',methods=['GET','POST'])
def home():
	if 'username' in session:
		path=os.path.join(basePath,session["userid"])
		sql="select photoId,photoName,image,title from photos where userId=%s"
		args=(session['userid'])
		cursor=db.cursor()
		cursor.execute(sql,args)
		output=[]
		numrows = cursor.rowcount
		for x in xrange(0,numrows):
			row = cursor.fetchone()
			outputrow=[]
			photoName=row[1]
			extension=photoName.rsplit('.',1)
			photoName=
		return render_template('home.html')
	return redirect(url_for('login'))

@app.route('/upload',methods=['GET','POST'])
def upload():
	print 'uploading...'
	if 'username' in session and request.method == 'POST':
		print 'fetching values'
		title=request.form['title']
		print title
		userid=session['userid']
		print userid
		file = request.files['photo']
		print file
		file_contents = file.read()
		filelen=len(file_contents)
		print filelen
		uuidValue=str(uuid.uuid1())
		print uuidValue
		fileName=secure_filename(file.filename)
		print fileName
		sql="insert into photos (photoId,photoName,Title,userId,image,imagesize) values ( %s,%s,%s,%s,%s,%s)"
		print sql
		cursor=db.cursor()
		args = (uuidValue,fileName,title,userid,file_contents,filelen,)
		cursor.execute(sql,args)
		db.commit()

		return redirect(url_for('login'))
		
	return render_template('upload.html')


@app.route('/comment/<photoid>',methods=['GET','POST'])
def comment(photoid):
	print photoid
	if 'username' in session:
		if request.method=='POST':
			sql="insert into comments(photoId,comment,userId) values ( %s,%s,%s)"
			cursor=db.cursor()
			comment=request.form['comment']
			print comment;
			
			userId=session['userid']
			args=(photoid,comment,userId,)
			print "args "+str(args)
			cursor.execute(sql,args)
			db.commit()
			return redirect(url_for('home'))		
		else:
			return render_template('view.html',photoid=photoid)
	return redirect(url_for('home'))
	

@app.route('/logout')
def logout():
	session.pop('username', None)
	session.pop('userid', None)
	return redirect(url_for('login'))

if __name__ == '__main__':
  app.run()
 
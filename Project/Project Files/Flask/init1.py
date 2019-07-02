#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

import hashlib
import datetime

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       port = 3306,
                       user='root',
                       password='',
                       db='PriCoSha',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
    cursor = conn.cursor();
    query = 'SELECT * FROM contentitem WHERE is_pub = 1 \
   AND post_time >= now() - INTERVAL 1 DAY ORDER BY post_time DESC'
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return render_template('index.html', posts=data)

#Define route for login
@app.route('/login')
def login():
    return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
    return render_template('register.html')

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    #grabs information from the forms
    email = request.form['email']
    password = request.form['password']
    hash_pass = hashlib.md5(password.encode('utf_8')).hexdigest()

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM Person WHERE email = %s and password = %s'
    cursor.execute(query, (email, hash_pass))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        session['email'] = email
        return redirect(url_for('home'))
    else:
        #returns an error message to the html page
        error = 'Invalid login or email'
        return render_template('login.html', error=error)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    #grabs information from the forms
    email = request.form['email']
    password = request.form['password']
    fname = request.form['first_name']
    lname = request.form['last_name']
    hash_pass = hashlib.md5(password.encode('utf_8')).hexdigest()

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM Person WHERE email = %s'
    cursor.execute(query, (email))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register.html', error = error)
    else:
        ins = 'INSERT INTO person(email, password, fname, lname) VALUES(%s, %s, %s, %s)'
        cursor.execute(ins, (email, hash_pass, fname, lname))
        conn.commit()
        cursor.close()
        return render_template('index.html')


@app.route('/home')
def home():
    user = session['email']
    cursor = conn.cursor();
    query = 'SELECT * FROM contentitem\
   LEFT JOIN tag ON contentitem.item_id = tag.item_id\
   LEFT JOIN emoji ON contentitem.item_id = emoji.post_id\
    WHERE (contentitem.email = %s OR is_pub = 1 OR email_tagged = %s  OR email_tagger = %s)\
    AND post_time >= now() - INTERVAL 1 DAY\
    ORDER BY post_time DESC'
    cursor.execute(query, (user, user, user))
    data = cursor.fetchall()
    query = 'SELECT fname FROM Person WHERE email = %s'
    cursor.execute(query, (user))
    data2 = cursor.fetchone()
    cursor.close()
    return render_template('home.html', name=data2['fname'], posts=data)

@app.route('/post', methods=['GET', 'POST'])
def post():
    email = session['email']
    cursor = conn.cursor();
    blog = request.form['blog']
    postime = datetime.datetime.now();
    is_public = request.form.get('is_pub')
    is_pub = 0
    if(is_public):
        is_pub = 1
    query = 'INSERT INTO contentitem (item_name, email, post_time, is_pub) VALUES(%s, %s, %s, %s)'
    cursor.execute(query, (blog, email, postime, int(is_pub)))
    conn.commit()
    cursor.close()
    return redirect(url_for('home'))

@app.route('/select_blogger')
def select_blogger():
    #check that user is logged in
    #username = session['username']
    #should throw exception if username not found
    
    user = session['email']
    cursor = conn.cursor();
    query = 'SELECT DISTINCT email FROM contentitem WHERE email != %s'
    cursor.execute(query, (user))
    data = cursor.fetchall()
    cursor.close()
    return render_template('select_blogger.html', user_list=data)

@app.route('/show_posts', methods=["GET", "POST"])
def show_posts():
    poster = request.args['poster']
    cursor = conn.cursor();
    query = 'SELECT post_time, item_name, item_id, tot_votes FROM contentitem WHERE email = %s ORDER BY post_time DESC'
    cursor.execute(query, poster)
    data = cursor.fetchall()
    cursor.close()
    return render_template('show_posts.html', poster_name=poster, posts=data)

## Comments
@app.route('/comments', methods=["GET", "POST"])
def comments():
    item_id = request.form['post_id']
    return redirect(url_for('show_comments', postid = item_id))

@app.route('/show_comments', methods=["GET", "POST"])
def show_comments():
    item_id = request.args['postid']
    cursor = conn.cursor();
    query = 'SELECT post_time, item_name, email, tot_votes FROM contentitem WHERE item_id = %s'
    cursor.execute(query, item_id)
    data = cursor.fetchone()
    query = 'SELECT post_time, item_name, email, item_id, tot_votes FROM contentitem WHERE comment_on_item = %s'
    cursor.execute(query, item_id)
    data2 = cursor.fetchall()
    cursor.close()
    return render_template('comments.html', orig_postid=item_id, orig_post=data, posts=data2)

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    email = session['email']
    cursor = conn.cursor();
    blog = request.form['blog']
    item_id = request.form['itemid']
    postime = datetime.datetime.now();
    is_public = request.form.get('is_pub')
    is_pub = 0
    if(is_public):
        is_pub = 1
    query = 'INSERT INTO contentitem (item_name, email, post_time, is_pub, comment_on_item)\
   VALUES(%s, %s, %s, %s, %s)'
    cursor.execute(query, (blog, email, postime, int(is_pub), item_id))
    conn.commit()
    cursor.close()
    return redirect(url_for('show_comments', postid = item_id))

##Tagging
@app.route('/tags', methods=["GET", "POST"])
def tags():
    item_id = request.form['post_id']
    return render_template('tag.html', orig_postid = item_id )

@app.route('/managetags', methods=['GET', 'POST'])
def managetags():
    email = session['email']
    cursor = conn.cursor();
    query = '''SELECT * FROM tag JOIN contentitem ON contentitem.item_id = tag.item_id\
   WHERE email_tagged = %s AND status = 0'''
    cursor.execute(query, (email))
    pendingtags = cursor.fetchall()
    
    query = '''SELECT * FROM grouptag JOIN Member ON Member.fg_name = grouptag.fg_name\
        WHERE email_creator = %s AND status = 0'''
    cursor.execute(query,(email))
    grouptag = cursor.fetchall()

    query = '''SELECT * FROM tag JOIN contentitem ON contentitem.item_id = tag.item_id\
        WHERE email_tagged = %s AND status = 1''' #include grouptags
    cursor.execute(query,(email))
    tagged = cursor.fetchall()
    return render_template('managetags.html', tagRequests = pendingtags,grouptag = grouptag, taggedIn = tagged)

@app.route('/addTag', methods=['GET', 'POST'])
def addTag():
    tagger = session['email']
    cursor = conn.cursor();
    email_taggee = request.form['name']
    item_id = request.form['itemid']
    tagtime = datetime.datetime.now();
    status = 0
    query = '''SELECT email_tagged FROM tag WHERE email_tagger = %s AND item_id = %s'''
    cursor.execute(query, (tagger, item_id))
    data = cursor.fetchall()
    if(data):
        send = "Person has already been tagged"
        return render_template('managetags.html', error = send)

    else:
        query = '''INSERT INTO tag VALUES( %s, %s, %s, %s, %s)'''
        cursor.execute(query, (email_taggee, tagger, item_id, int(status), tagtime))
        conn.commit()

    cursor.close()
    return redirect(url_for('managetags'))

@app.route('/addGroupTag', methods=['GET', 'POST'])
def addGroupTag():
    tagger = session['email']
    cursor = conn.cursor();
    fg_name = request.form['group']
    item_id = request.form['itemid']
    tagtime = datetime.datetime.now();
    status = 0
    query = '''SELECT email_tagger FROM grouptag WHERE email_tagger = %s
        AND item_id = %s'''
    cursor.execute(query, (tagger, item_id))
    data = cursor.fetchall()
    if(data):
        send = "Group has already been tagged"
        return render_template('managetags.html', error = send)

    else:
        query = '''INSERT INTO grouptag VALUES( %s, %s, %s, %s, %s)'''
        cursor.execute(query, (tagger, fg_name, item_id, int(status), tagtime))
        conn.commit()

    cursor.close()
    return redirect(url_for('managetags'))

@app.route('/approveTag', methods=['GET', 'POST'])
def approveTag():
    tagged = session['email']
    cursor = conn.cursor();
    item_id = request.form['itemid']
    approval = request.form.get('approve')
    tagger = request.form['tagger']
    # Set status to 1 or -1 if approval denied or accepted
    status = 0
    if(approval == '1'):
        status = 1
    if(approval == '-1'):
        status = -1
    query = 'UPDATE tag SET status = %s WHERE email_tagger = %s AND email_tagged = %s AND item_id = %s'
    cursor.execute(query, (int(status), tagger, tagged, item_id))
    return redirect(url_for('managetags'))

@app.route('/approveGroupTag', methods=['GET', 'POST'])
def approveGroupTag():
    owner = session['email']
    cursor = conn.cursor();
    item_id = request.form['itemid']
    fg_name = request.form['group']
    approval = request.form.get('approve')
    tagger = request.form['tagger']
    # Set status to 1 or -1 if approval denied or accepted
    status = 0
    if(approval == '1'):
        status = 1
    if(approval == '-1'):
        status = -1
    query = '''UPDATE grouptag SET status = %s WHERE email_tagger = %s AND fg_name = %s  AND item_id = %s'''
    cursor.execute(query, (int(status), tagger, fg_name, item_id))
    return redirect(url_for('managetags'))

## Rating
@app.route('/rate_h', methods=['GET', 'POST'])
def rate_h():
    email = session['email']
    cursor = conn.cursor();
    item_id = request.form['itemid']
    postime = datetime.datetime.now();
    getvote = request.form.get('like')
    vote = 0
    if(getvote == '1'):
        vote = 1
    if(getvote == '-1'):
        vote = -1
    query = 'SELECT email, item_id FROM rate WHERE email = %s AND item_id = %s'
    cursor.execute(query, (email, item_id))
    data = cursor.fetchall()
    if(data):
        query = 'UPDATE rate SET vote = %s, rate_time = %s  WHERE email = %s AND item_id = %s'
        cursor.execute(query, (int(vote), postime, email, item_id))
        conn.commit()
    else:
        query = 'INSERT INTO rate (email, item_id, vote, rate_time)  VALUES(%s, %s, %s, %s)'
        cursor.execute(query, (email, item_id, int(vote), postime))
        conn.commit()
    query = 'UPDATE contentitem SET tot_votes = (\
    SELECT SUM(vote) FROM rate WHERE contentitem.item_id = item_id)'
    cursor.execute(query)
    cursor.close()
    return redirect(url_for('home'))

@app.route('/rate_p', methods=['GET', 'POST'])
def rate_p():
    email = session['email']
    cursor = conn.cursor();
    item_id = request.form['itemid']
    poster_email = request.form['poster']
    postime = datetime.datetime.now();
    getvote = request.form.get('like')
    vote = 0
    if(getvote == '1'):
        vote = 1
    if(getvote == '-1'):
        vote = -1
    query = 'SELECT email, item_id FROM rate WHERE email = %s AND item_id = %s'
    cursor.execute(query, (email, item_id))
    data = cursor.fetchall()
    if(data):
        query = 'UPDATE rate SET vote = %s, rate_time = %s  WHERE email = %s AND item_id = %s'
        cursor.execute(query, (int(vote), postime, email, item_id))
        conn.commit()
    else:
        query = 'INSERT INTO rate (email, item_id, vote, rate_time)  VALUES(%s, %s, %s, %s)'
        cursor.execute(query, (email, item_id, int(vote), postime))
        conn.commit()
    query = 'UPDATE contentitem SET tot_votes = (\
    SELECT SUM(vote) FROM rate WHERE contentitem.item_id = item_id)'
    cursor.execute(query)
    cursor.close()
    return redirect(url_for('show_posts', poster = poster_email))

@app.route('/rate_c', methods=['GET', 'POST'])
def rate_c():
    email = session['email']
    cursor = conn.cursor();
    item_id = request.form['itemid']
    post_id = request.form['orig_post']
    postime = datetime.datetime.now();
    getvote = request.form.get('like')
    vote = 0
    if(getvote == '1'):
        vote = 1
    if(getvote == '-1'):
        vote = -1
    query = 'SELECT email, item_id FROM rate WHERE email = %s AND item_id = %s'
    cursor.execute(query, (email, item_id))
    data = cursor.fetchall()
    if(data):
        query = 'UPDATE rate SET vote = %s, rate_time = %s  WHERE email = %s AND item_id = %s'
        cursor.execute(query, (int(vote), postime, email, item_id))
        conn.commit()
    else:
        query = 'INSERT INTO rate (email, item_id, vote, rate_time)  VALUES(%s, %s, %s, %s)'
        cursor.execute(query, (email, item_id, int(vote), postime))
        conn.commit()
    query = 'UPDATE contentitem SET tot_votes = (\
    SELECT SUM(vote) FROM rate WHERE contentitem.item_id = item_id)'
    cursor.execute(query)
    cursor.close()
    return redirect(url_for('show_comments', postid = post_id))


## Friend Group
@app.route('/createFG', methods=['GET', 'POST'])
def createFG():
	email = session['email']
	cursor = conn.cursor();
	gname = request.form["fg_name"]
	gname = gname.replace(" ", "")
	description = request.form["description"]
	query = '''INSERT into friendgroup values (%s, %s, %s)'''
	cursor.execute(query,(email,gname,description))
	query2 = '''INSERT into member values (%s, %s, %s)'''
	cursor.execute(query2,(email,gname,email))
	conn.commit()
	cursor.close()
	return redirect(url_for('friendgroup'))

@app.route('/friendgroup')
def friendgroup():
	email = session['email']
	cursor = conn.cursor();
	query = '''SELECT fg_name, description FROM person Natural Join friendgroup
	WHERE person.email = %s'''
	cursor.execute(query,email)
	ownedFG = cursor.fetchall()
	query = '''SELECT fg_name, owner_email, description FROM member Natural Join friendgroup WHERE owner_email = %s'''
	cursor.execute(query,email)
	memberFG = cursor.fetchall()
	cursor.close()
	return render_template('friendgroup.html', ownFG = ownedFG, memFG = memberFG)

@app.route('/friends')
def friends():
    email = session['email']
    cursor = conn.cursor();
    query = '''SELECT DISTINCT email_creator FROM member
                WHERE email_creator != %s '''
    cursor.execute(query, (email))
    yourFriends = cursor.fetchall()
    return render_template('friends.html', urFriends = yourFriends)

@app.route('/add_friend', methods=['GET', 'POST'])
def addFriend():
	email = session['email']
	cursor = conn.cursor()
	fname = request.form['fname']
	lname = request.form['lname']
	friendgroup = request.form['friendgroup']
	query = '''SELECT fg_name FROM friendgroup WHERE fg_name = %s'''
	cursor.execute(query, (friendgroup))
	data = cursor.fetchone()
	if(data):
		query2 = '''SELECT member.email_creator FROM member WHERE member.email_creator IN
		(SELECT person.email FROM person WHERE fname = %s AND lname = %s) AND
		 fg_name = %s '''
		cursor.execute(query2, (fname, lname, friendgroup))
		data2 = cursor.fetchone()
		if(data2):
			error = "This person is already in this friendgroup!"
			return render_template('friends.html', error = error)
		else:
			query3 = '''SELECT email FROM person WHERE fname = %s AND
			lname = %s
			'''
			cursor.execute(query3, (fname, lname))
			data3 = cursor.fetchall();
			if(len(data3) > 1):
				error = "There are multiple people with that name!"
				return render_template('friends.html', error = error)
			elif(len(data3) == 0):
				error = "This person does not exist!"
				return render_template('friends.html', error = error)
			else:
				ins = '''INSERT into member values (%s, %s, %s)'''
				cursor.execute(ins, (email, friendgroup, data3[0]["email"]))
				conn.commit()
				cursor.close()
				return redirect(url_for('friends'))
	else:
		error = "This friendgroup does not exist!"
		return render_template('friends.html', error = error)

@app.route('/deletefriend', methods=['GET','POST'])
def delete_friend():
    email = session['email']
    group_name = request.form['friendgroup']
    friend = request.form['email']
    cursor = conn.cursor()
    query = "SELECT owner_email FROM Member WHERE owner_email = %s"
    cursor.execute(query, (email))
    data = cursor.fetchone()
    if (data):        
        query2 = "DELETE FROM Member WHERE owner_email = %s AND fg_name = %s AND email_creator = %s"
        cursor.execute(query2, (email, group_name, friend))
        conn.commit()
        cursor.close()
        return redirect(url_for('friends'))
    else:
        return redirect(url_for('friends'))

## User Profile
@app.route('/mypost')
def mypost():
    email = session['email']
    cursor = conn.cursor();
    query = '''SELECT * FROM contentitem WHERE email = %s'''
    cursor.execute(query, email)
    yourPosts = cursor.fetchall()
    query = '''SELECT about_me FROM person WHERE email = %s'''
    cursor.execute(query, email)
    data=cursor.fetchone()
    cursor.close()
    return render_template('mypost.html',about=data["about_me"], posts = yourPosts)

@app.route('/users')
def users():
	cursor = conn.cursor()
	query = '''SELECT email, fname, lname FROM person'''
	cursor.execute(query)
	users = cursor.fetchall()
	cursor.close()
	return render_template('users.html', users = users)

@app.route('/about_me', methods=['GET', 'POST'])
def about_me():
    email = session['email']
    cursor = conn.cursor();
    about = request.form['about']
    query = 'UPDATE person SET about_me = %s WHERE email = %s'
    cursor.execute(query, (about, email))
    conn.commit()
    cursor.close()
    return redirect(url_for('mypost'))

## Emojis
@app.route('/emoji', methods = ['GET', 'POST'])
def emoji():
    item_id = request.form['post_id']
    testid = request.form['crying_emoji']
    return redirect(url_for('add_emoji', postid = item_id, test = testid ))
    

@app.route('/add_emoji', methods = ['GET', 'POST'])
def add_emoji():
    email = session['email']
    item_id = request.form['post_id']
    emoji = request.form['emoji']
    posttime = datetime.datetime.now();
    cursor = conn.cursor();
    query = 'SELECT emoji FROM emoji WHERE email = %s AND post_id = %s'
    data = cursor.execute(query,(email, item_id))
    if (data):
        query = 'UPDATE emoji SET emoji = %s WHERE email = %s AND post_id = %s'
        cursor.execute(query,(str(emoji), email, item_id))
    else:
        query = 'INSERT INTO emoji VALUES(%s,%s, %s)'
        cursor.execute(query,(item_id, str(emoji), email))
    #getemoji = request.form.get(' ') #get the emoji they chose
    cursor.close()
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('email')
    return redirect('/')
        
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)

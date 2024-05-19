from flask import Flask , render_template , request , redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///bloglite.sqlite3"
db = SQLAlchemy(app)
# app.app_context().push()

class User(db.Model):
    user_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    user_name = db.Column(db.String,unique=True,nullable=False)
    password = db.Column(db.String,nullable=False)
    profile_pic = db.Column(db.String,nullable=False)
    blogs = db.relationship('Blog',backref='owner')

class Blog(db.Model):
    blog_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    title = db.Column(db.String,nullable=False)
    description = db.Column(db.String,nullable=False)
    content = db.Column(db.String,nullable=False)
    image = db.Column(db.String,nullable=False)
    ref_user_id = db.Column(db.Integer,db.ForeignKey("user.user_id"),nullable=False)

class Follwer(db.Model):
    network_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    network_x = db.Column(db.Integer,db.ForeignKey("user.user_id"),nullable=False)
    network_y = db.Column(db.Integer,db.ForeignKey("user.user_id"),nullable=False)

class Comments(db.Model):
    comment_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    ref_blog_id = db.Column(db.Integer,db.ForeignKey("blog.blog_id"),nullable=False)
    ref_user_id = db.Column(db.Integer,db.ForeignKey("user.user_id"),nullable=False)
    comment = db.Column(db.String,nullable=False)

class Likes(db.Model):
    like_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    ref_blog_id = db.Column(db.Integer,db.ForeignKey("blog.blog_id"),nullable=False)
    ref_user_id = db.Column(db.Integer,db.ForeignKey("user.user_id"),nullable=False)

#-----------------------------------------------------------------------------------------------
#SIGN IN

@app.route('/',methods=["GET","POST"])
def signin():
    if request.method == "GET":
        return render_template('signin.html')
    else:
        var_user_name = request.form['username']
        user_obj = User.query.filter_by(user_name=var_user_name).first()
        if user_obj != None:
            if user_obj.password == request.form['acc_password']:
                return redirect(url_for('profile',user_name = user_obj.user_name))
            else:
                return """<h1>Invalid Password</h1>
                          <a href='/'>Back</a>"""
        else:
            return """<h1>Invalid Username</h1>
                      <a href='/'>Back</a>"""

#-----------------------------------------------------------------------------------------------
#SIGN UP 

@app.route('/signup',methods=["GET","POST"])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
    elif request.method == "POST":
        try:
            user_name = request.form['new_username']
            password = request.form['new_password']

            file = request.files["image"]
            var_img = 'static/profile_pic/'+file.filename
            file.save(var_img)

            user_obj = User(user_name=user_name,password=password,profile_pic=var_img)
            db.session.add(user_obj)
            db.session.commit()
            return redirect(url_for('signin'))
        except:
            return """<h1>User Already Exist</h1>
                      <a href='/signup'>Back</a>"""


#-----------------------------------------------------------------------------------------------
#USER PROFILE

@app.route('/profile/<user_name>')
def profile(user_name):
    user_obj = User.query.filter_by(user_name=user_name).first()
    blogs = user_obj.blogs
    followers = Follwer.query.filter_by(network_y=user_obj.user_id).all()
    following = Follwer.query.filter_by(network_x=user_obj.user_id).all()

    return render_template('profile.html',user_name=user_name,
                                         profile_pic = user_obj.profile_pic,
                                         blogs_list=blogs[::-1],
                                         followers=followers,
                                         following=following)

#-----------------------------------------------------------------------------------------------
#EDIT USER PROFILE

@app.route('/edit_profile/<user_name>',methods=["GET","POST"])
def edit_profile(user_name):
    user_obj = User.query.filter_by(user_name=user_name).first()
    if request.method == "GET":
        return render_template('edit_profile.html',user_name=user_name,user_obj=user_obj,profile_pic=user_obj.profile_pic)
    elif request.method == "POST":
        var_old_pass = request.form["old_password"]
        if var_old_pass == user_obj.password:
            
            var_new_pass = request.form["new_password"]
            file = request.files["image"]

            if var_new_pass != '':
                user_obj.password = var_new_pass
            if file.filename != '':
                os.remove(user_obj.profile_pic)
                var_img = 'static/profile_pic/'+file.filename
                file.save(var_img)
                user_obj.profile_pic = var_img
            db.session.commit()
            return redirect(url_for('profile',user_name = user_name))
        else:
            return f"""<br><br>
                       <h1>Enter Correct Password For Updating Your Profile</h1>
                       <a href='/edit_profile/{user_name}'>Back</a>"""
#-----------------------------------------------------------------------------------------------
#ADD BLOG

@app.route('/addblog/<user_name>',methods=["GET","POST"])
def addblog(user_name):
    user_obj = User.query.filter_by(user_name = user_name).first()
    if request.method == "GET":
        return render_template("addblog.html",user_name = user_name,profile_pic=user_obj.profile_pic)
    else:
        var_title = request.form["title"]
        var_des = request.form["des"]
        var_content = request.form["content"]
        file = request.files["image"]
        var_img = 'static/blog_images/'+file.filename
        file.save(var_img)
        blog_obj = Blog(title=var_title,description=var_des,content=var_content,image=var_img,owner=user_obj)
        db.session.add(blog_obj)
        db.session.commit()
        return redirect(url_for('profile',user_name = user_obj.user_name))

#-----------------------------------------------------------------------------------------------
#READ BLOG

@app.route('/readblog/<user_name>/<blog_id>',methods=["GET"])
def readblog(user_name,blog_id):
    user_obj = User.query.filter_by(user_name = user_name).first()
    blog_obj = Blog.query.filter_by(blog_id=blog_id).first()
    likes_obj = Likes.query.filter_by(ref_blog_id = blog_id).all()

    comment_obj = Comments.query.filter_by(ref_blog_id = blog_id).all()
    user_comment_list = []
    for obj in comment_obj:
        temp_user_name = User.query.filter_by(user_id=obj.ref_user_id).first().user_name
        user_comment_list.append((temp_user_name,obj))

    curr_like_obj = Likes.query.filter_by(ref_blog_id = blog_id,ref_user_id=user_obj.user_id).first()

    return render_template('readblog.html',user_name = user_name,
                                            blog=blog_obj,
                                            profile_pic = user_obj.profile_pic,
                                            likes=len(likes_obj),
                                            already_liked=curr_like_obj,
                                            already_commented = user_comment_list)

#-----------------------------------------------------------------------------------------------
#EDIT BLOG

@app.route('/editblog/<user_name>/<blog_id>',methods=["GET","POST"])
def editblog(user_name,blog_id):
    blog_obj = Blog.query.filter_by(blog_id=blog_id).first()
    user_obj = User.query.filter_by(user_name = user_name).first()
    if request.method == "GET":
        return render_template("editblog.html",user_name = user_name,blog = blog_obj,profile_pic=user_obj.profile_pic)
    elif request.method == "POST":
        blog_obj.content = request.form["content"]
        blog_obj.description = request.form["des"]
        db.session.commit()
        return redirect(url_for('profile',user_name = user_name))

#-----------------------------------------------------------------------------------------------
#DELETE BLOG

@app.route('/deleteblog/<user_name>/<blog_id>')
def deleteblog(user_name,blog_id):
    blog_obj=Blog.query.filter_by(blog_id=blog_id).first()
    if os.path.exists(blog_obj.image):
        os.remove(blog_obj.image)
    likes_ = Likes.query.filter_by(ref_blog_id = blog_id).all()
    comments_ = Comments.query.filter_by(ref_blog_id = blog_id).all()
    if len(likes_) != 0:
        Likes.query.filter_by(ref_blog_id = blog_id).delete()  
    if len(comments_) != 0:
        Comments.query.filter_by(ref_blog_id = blog_id).delete() 
    db.session.delete(blog_obj)
    db.session.commit()
    return redirect(url_for('profile',user_name = user_name))

@app.route('/delete_confirmation/<user_name>/<blog_id>')
def delete_confirmation(user_name,blog_id):
    user_obj = User.query.filter_by(user_name = user_name).first()
    blog_obj = Blog.query.filter_by(blog_id=blog_id).first()
    return render_template('deletion_confirmation.html',user_name = user_name,obj=blog_obj,profile_pic=user_obj.profile_pic)

#-----------------------------------------------------------------------------------------------
#LIKES BLOG

@app.route('/likes/<user_name>/<blog_id>',methods=["GET"])
def likes(user_name,blog_id):
    if request.method == "GET":
        like_req = request.args.get('like')
        user_obj = User.query.filter_by(user_name=user_name).first()
        if like_req == '1':
            like_obj = Likes(ref_blog_id=blog_id,ref_user_id=user_obj.user_id)
            db.session.add(like_obj)
            db.session.commit()
        elif like_req == '0':
            like_obj = Likes.query.filter_by(ref_blog_id=blog_id,ref_user_id=user_obj.user_id).delete()
            db.session.commit()
        return redirect(url_for('readblog',user_name = user_name,blog_id=blog_id))

#-----------------------------------------------------------------------------------------------
#COMMENT BLOG

@app.route('/comments/<user_name>/<blog_id>',methods=["POST"])
def comments(user_name,blog_id):
    user_obj = User.query.filter_by(user_name=user_name).first()
    if request.method == "POST":
        var_comment = request.form['comment']
        if var_comment != '':
            comment_obj = Comments(ref_blog_id=blog_id,ref_user_id=user_obj.user_id,comment=var_comment)
            db.session.add(comment_obj)
            db.session.commit()
    return redirect(url_for('readblog',user_name = user_name,blog_id=blog_id))

#-----------------------------------------------------------------------------------------------
#FRIENDS PROFILE

@app.route('/friend_profile/<curr_username>/<friend_username>')
def friend_profile(curr_username,friend_username):
    curr_user_obj = User.query.filter_by(user_name=curr_username).first()
    friend_user_obj = User.query.filter_by(user_name=friend_username).first()

    temp1 = Follwer.query.filter_by(network_x=curr_user_obj.user_id,network_y=friend_user_obj.user_id).first()
    var_req = request.args.get('req','None')
    if  var_req == '1' and temp1==None:
        follow_obj = Follwer(network_x = curr_user_obj.user_id,network_y = friend_user_obj.user_id)
        db.session.add(follow_obj)
        db.session.commit()
    elif var_req == '0':
        Follwer.query.filter_by(network_x = curr_user_obj.user_id,network_y = friend_user_obj.user_id).delete()
        db.session.commit()        

    temp = Follwer.query.filter_by(network_x=curr_user_obj.user_id,network_y=friend_user_obj.user_id).first()        
    if temp != None:
        i = (friend_user_obj,1)
    else:
        i = (friend_user_obj,0)

    temp = Follwer.query.filter_by(network_x=friend_user_obj.user_id,network_y=curr_user_obj.user_id).first()        
    if temp != None:
        j = (friend_user_obj,1)
    else:
        j = (friend_user_obj,0)        

    blogs = Blog.query.filter_by(ref_user_id=friend_user_obj.user_id).all()
    followers = Follwer.query.filter_by(network_y=friend_user_obj.user_id).all()
    following = Follwer.query.filter_by(network_x=friend_user_obj.user_id).all()
    return render_template('friend_profile.html',user_name=curr_username,
                                                blogs_list=blogs,
                                                followers=followers,
                                                following=following,
                                                i = i,
                                                j = j,
                                                profile_pic = curr_user_obj.profile_pic,
                                                friend_profile_pic = friend_user_obj.profile_pic)    

#-----------------------------------------------------------------------------------------------
#FOLLOWERS

@app.route('/followers/<username>')
def followers(username):
    curr_user_obj = User.query.filter_by(user_name=username).first()
    followers_list = Follwer.query.filter_by(network_y=curr_user_obj.user_id).all()

    var_req = request.args.get('req','None')
    if var_req != 'None':
        var_Y = request.args.get('friend','None')
        X = User.query.filter_by(user_name=username).first()
        Y = User.query.filter_by(user_name=var_Y).first()
        temp = Follwer.query.filter_by(network_x = X.user_id,network_y = Y.user_id).first()
        if var_req == '1' and temp == None:
            follow_obj = Follwer(network_x = X.user_id,network_y = Y.user_id)
            db.session.add(follow_obj)
            db.session.commit()
        elif var_req == '0':
            Follwer.query.filter_by(network_x = X.user_id,network_y = Y.user_id).delete()
            db.session.commit()

    res = []
    for obj in followers_list:
        temp = Follwer.query.filter_by(network_x=curr_user_obj.user_id,network_y=obj.network_x).first()
        friend_obj = User.query.filter_by(user_id=obj.network_x).first()
        if temp != None:
            res.append((friend_obj,1))
        else:
            res.append((friend_obj,0))

    return render_template('follwers.html',user_name=username,user_list=res,profile_pic = curr_user_obj.profile_pic)

#-----------------------------------------------------------------------------------------------
#FOLLOWING

@app.route('/following/<username>')
def following(username):
    curr_user_obj = User.query.filter_by(user_name=username).first()
    following_list = Follwer.query.filter_by(network_x=curr_user_obj.user_id).all()

    var_req = request.args.get('req','None')
    if var_req != 'None':
        var_Y = request.args.get('friend','None')
        X = User.query.filter_by(user_name=username).first()
        Y = User.query.filter_by(user_name=var_Y).first()
        temp = Follwer.query.filter_by(network_x = X.user_id,network_y = Y.user_id).first()
        if var_req == '1' and temp == None:
            follow_obj = Follwer(network_x = X.user_id,network_y = Y.user_id)
            db.session.add(follow_obj)
            db.session.commit()
        elif var_req == '0':
            Follwer.query.filter_by(network_x = X.user_id,network_y = Y.user_id).delete()
            db.session.commit()

    res = []
    for obj in following_list:
        temp = Follwer.query.filter_by(network_x=curr_user_obj.user_id,network_y=obj.network_y).first()
        friend_obj = User.query.filter_by(user_id=obj.network_y).first()
        if temp != None:
            res.append((friend_obj,1))
        else:
            res.append((friend_obj,0))

    return render_template('following.html',user_name=username,user_list=res,profile_pic = curr_user_obj.profile_pic)

#-----------------------------------------------------------------------------------------------
#MY FEED

@app.route('/myfeed/<user_name>')
def myfeed(user_name):
    user_obj = User.query.filter_by(user_name=user_name).first()
    temp = Follwer.query.filter_by(network_x = user_obj.user_id).all()
    following_list = []
    for obj in temp:
        Y = Blog.query.filter_by(ref_user_id=obj.network_y).all()
        temp_obj = User.query.filter_by(user_id=obj.network_y).first()
        for y in Y:
            if y != None:
                following_list.append((temp_obj,y))
    return render_template('myfeed.html',user_name=user_name,following_list = following_list,profile_pic = user_obj.profile_pic)

#-----------------------------------------------------------------------------------------------
#SEARCH

@app.route('/search/<user_name>',methods=["GET","POST"])
def search(user_name):
    curr_user_obj = User.query.filter_by(user_name=user_name).first()
    if request.method=="GET":
        value = request.args.get('search_val','None')
        if value == 'None':
            return render_template('search.html',user_name=user_name,profile_pic=curr_user_obj.profile_pic)
        else:
            var_search = value
            var_req = request.args.get('req','None')
            if var_req != 'None':
                var_Y = request.args.get('friend','None')
                X = User.query.filter_by(user_name=user_name).first()
                Y = User.query.filter_by(user_name=var_Y).first()
                temp = Follwer.query.filter_by(network_x = X.user_id,network_y = Y.user_id).first()
                if var_req == '1' and temp == None:
                    follow_obj = Follwer(network_x = X.user_id,network_y = Y.user_id)
                    db.session.add(follow_obj)
                    db.session.commit()
                elif var_req == '0':
                    Follwer.query.filter_by(network_x = X.user_id,network_y = Y.user_id).delete()
                    db.session.commit()
            user_list = User.query.all()
            search_result = []
            for obj in user_list:
                if var_search in obj.user_name and user_name != obj.user_name:
                    temp = Follwer.query.filter_by(network_x=curr_user_obj.user_id,network_y=obj.user_id).first()
                    if temp != None:
                        search_result.append((obj,1))
                    else:
                        search_result.append((obj,0))
            return render_template('search.html',user_name=user_name,user_list=search_result,search_val=var_search,profile_pic = curr_user_obj.profile_pic)

    else:
        var_search = request.form["search"]
        search_result = []
        if var_search != '':
            user_list = User.query.all()
            for obj in user_list:
                if var_search in obj.user_name and user_name != obj.user_name:
                    temp = Follwer.query.filter_by(network_x=curr_user_obj.user_id,network_y=obj.user_id).first()
                    if temp != None:
                        search_result.append((obj,1))
                    else:
                        search_result.append((obj,0))
        return render_template('search.html',user_name=user_name,user_list=search_result,search_val=var_search,profile_pic = curr_user_obj.profile_pic)


if __name__ == '__main__':
    app.run(debug=True)
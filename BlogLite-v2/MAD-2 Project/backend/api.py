from models import *
from flask_restful import Resource,Api
from flask_cors import CORS
from flask_security import Security,SQLAlchemyUserDatastore,auth_required
from flask_security.utils import hash_password,verify_password
from flask import jsonify,send_file
from celery import Celery
from celery.schedules import crontab
import datetime
from httplib2 import Http
import json
from jinja2 import Template
from flask_caching import Cache

datastore = SQLAlchemyUserDatastore(db,User,Role)
security = Security(app,datastore)

api = Api(app)
CORS(app)
cache = Cache(app)

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379',
    CELERY_ENABLE_UTC = False,
    CELERY_TIMEZONE = 'Asia/Kolkata'
)
celery = make_celery(app)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=0,minute=0,day_of_month='1'), report.s(), name='Report for Users')
    sender.add_periodic_task(crontab(hour=18,minute=30), reminder.s(), name='Reminder for Users')

@celery.task(name="api.report")
def report():
    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    email_sender = '21f1002171@ds.study.iitm.ac.in'
    email_password = 'ssciyhbuoqjktsps'
    subject = "Blog Lite Report"

    for user in User.query.all():
        email_receiver = user.email
        em = MIMEMultipart()

        data = {'name' : user.user_name,
                'followers' : len(Follwer.query.filter_by(network_y=user.id).all()),
                'following' : len(Follwer.query.filter_by(network_x=user.id).all()),
                'posts' : Blog.query.filter_by(ref_user_id=user.id).all(),
                }      
        
        em['From'] = email_sender
        em['To'] = email_receiver
        em['subject'] = subject
        body = MIMEText(get_HTML(data),'html')
        
        em.attach(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
            smtp.login(email_sender,email_password)
            smtp.sendmail(email_sender,email_receiver,em.as_string())
        
        return "Mail Sent"

def get_HTML(data):
    with open('report.html') as file:
        template = Template(file.read())
        return template.render(data=data)

@celery.task(name="api.reminder")
def reminder():
    for user in User.query.all():
        t = datetime.datetime.now() - datetime.datetime.strptime(user.last_visited , '%Y-%m-%d %H:%M:%S.%f')
        diff = t.total_seconds() #/ (60*60)
        if diff > 10:
            data = {'text' : f"Hi {user.user_name},\n\tIt appears that you haven't visited Blog Lite V2 today.\nThank You."}
            message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
            http_obj = Http()
            http_obj.request(
                uri='https://chat.googleapis.com/v1/spaces/AAAAIqb9vrA/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=8GEtLkbVkfsXc0NbiB64YveYIAiow-pp-950mPcJ-_A%3D',
                method='POST',
                headers=message_headers,
                body=json.dumps(data),
            )
    return "Reminder Sent"

@celery.task(name="api.generate_csv")
def generate_csv(username):
    print(username)
    import csv
    user_obj = User.query.filter_by(user_name=username).first()
    res = []
    for blog in Blog.query.filter_by(ref_user_id = user_obj.id).all():
        res.append([
            blog.title,
            blog.description,
            blog.content,
            blog.time_stamp,
        ])

    filename = 'export.csv'
    with open(filename, 'w') as csvfile:        
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Title','Description','Content','Time_stamp'])
        csvwriter.writerows(res)
    return "Job Starting..."

@app.route('/trigger-generate_csv/<username>')
@auth_required('token')
def trigger_generate_csv(username):
    print("Hello")
    a = generate_csv.delay(username)
    return {
        'Id' : a.id,
        'State' : a.state,
        'Result' : a.result
    }

@app.route('/download_file/<username>')
def download_file(username):
    return send_file('export.csv')

class LOGINAPI(Resource):
    def post(self):
        data = request.get_json()
        user = datastore.find_user(email = data['email'])
        user.last_visited = datetime.datetime.now()
        db.session.commit()
        if user and  verify_password(data['password'],user.password):
            return jsonify({'token':user.get_auth_token(), 'active':True})
        else:
            return jsonify({'active':False})
        
class GetAllBlogs(Resource):
    @auth_required('token')
    @cache.memoize(60)
    def get(self,usr_name):
        user_obj = User.query.filter_by(user_name=usr_name).first()
        res,temp = [],[]
        for i in Blog.query.filter_by(ref_user_id=user_obj.id).all():
            temp.append((i.time_stamp,i))
        temp.sort()
        for i in temp:
            res.append({
                "Blog_id":i[1].blog_id,
                "Blog_Title":i[1].title,
                "Blog_Description":i[1].description,
                "Blog_Content":i[1].content,
                "Blog_image":i[1].image,
                "owner" : user_obj.user_name
            })
        
        return {"blogs" : res}

class MyFeed(Resource):
    @auth_required('token')
    @cache.memoize(60)
    def get(self,usr_name):
        curr_user = User.query.filter_by(user_name=usr_name).first()
        res,temp = [],[]
        for j in Follwer.query.filter_by(network_x=curr_user.id).all():
            for i in Blog.query.filter_by(ref_user_id=j.network_y).all():
                temp.append((i.time_stamp,i,j))
        temp.sort()
        for i in temp:
            res.append({
                    "Blog_id":i[1].blog_id,
                    "Blog_Title":i[1].title,
                    "Blog_Description":i[1].description,
                    "Blog_Content":i[1].content,
                    "Blog_image":i[1].image,
                    "owner" : User.query.filter_by(id=i[2].network_y).first().user_name
                })
        return {"blogs" : res}

class GetAllFollowers(Resource):
    @auth_required('token')
    def get(self,username):
        user_obj = User.query.filter_by(user_name=username).first()

        followers = []
        for i in Follwer.query.filter_by(network_y = user_obj.id).all():
            followers.append({
                "friend_name" : User.query.filter_by(id=i.network_x).first().user_name
            })

        following = []
        for i in Follwer.query.filter_by(network_x = user_obj.id).all():
            following.append({
                "friend_name" : User.query.filter_by(id=i.network_y).first().user_name
            })

        res = {
            "Followers" : followers,
            "Following" : following,
        }
        return {"result" : res}

class SearchAllUsers(Resource):
    @auth_required('token')
    def get(self,user_searching,search_val):
        res = []
        user_obj = User.query.filter_by(user_name = user_searching).first()
        for user in User.query.all():
            if search_val in user.user_name:
                follow_obj = Follwer.query.filter_by(network_x=user_obj.id,network_y=user.id).first()
                if follow_obj:
                    follow_val = 1
                else:
                    follow_val = 0
                res.append({
                    'friend_name' : user.user_name,
                    'follow_val' : follow_val
                })
        return {'search_list' : res}

class Follow(Resource):
    @auth_required('token')
    def get(self,username,friendname,val):
        user_obj = User.query.filter_by(user_name=username).first()
        frnd_obj = User.query.filter_by(user_name=friendname).first()
        if val == '1':
            obj = Follwer(network_x = user_obj.id,network_y=frnd_obj.id)
            db.session.add(obj)
            db.session.commit()
            return "Followed"
        else:
            Follwer.query.filter_by(network_x=user_obj.id,network_y=frnd_obj.id).delete()
            db.session.commit()
            return "UnFollowed"
    
class BLOGAPI(Resource):
    @auth_required('token')
    @cache.memoize(60)
    def get(self,blog_id):
        blog_obj = Blog.query.filter_by(blog_id=blog_id).first()
        if blog_obj != None:
            result = {
                    "Blog_id":blog_id,
                    "Blog_Title":blog_obj.title,
                    "Blog_Description":blog_obj.description,
                    "Blog_Content":blog_obj.content,
                    "Blog_image":blog_obj.image,
                    "owner" : User.query.filter_by(id=blog_obj.ref_user_id).first().user_name
                    }

            return result,200
        else:
            return "Invalid Blog_ID",404
    
    @auth_required('token')
    def post(self,usr_name):
        title = request.form['blog_title']
        des = request.form['blog_description']
        content = request.form['blog_content']
        image = request.files['blog_image']
        if usr_name != '':
            user_obj = User.query.filter_by(user_name=usr_name).first()
            if user_obj:
                var_img = '../frontend/static/blog_images/'+ f'{usr_name}-{title}.png'
                image.save(var_img)
                # print(title,des,content,image)
                blog_obj = Blog(title=title,description=des,content=content,image=var_img,time_stamp=datetime.datetime.now(),ref_user_id=user_obj.id)
                db.session.add(blog_obj)
                db.session.commit()
                return "Successfully created the Blog"
            else:
                "User Doesn't Exist",404
        else:
            "Please specify User ID",404
    
    @auth_required('token')
    def put(self,blog_id):
        des = request.form['blog_description']
        content = request.form['blog_content']
        blog_obj = Blog.query.filter_by(blog_id=blog_id).first()
        if blog_obj != None:
            blog_obj.description = des
            blog_obj.content = content
            db.session.commit()
            result = {
                    "Blog_id":blog_id,
                    "Blog_Title":blog_obj.title,
                    "Blog_Description":blog_obj.description,
                    "Blog_Content":blog_obj.content
                    }
            return result,200
        else:
            return "Invalid Blog_ID",404
    
    @auth_required('token')
    def delete(self,blog_id):
        blog_obj = Blog.query.filter_by(blog_id=blog_id)
        if blog_obj.first():
            blog_obj.delete()
            db.session.commit()
            return "Successfully Deleted",200
        else:
            return "Invalid Blog_ID",404

class USERAPI(Resource):
    @auth_required('token')
    @cache.memoize(60)
    def get(self,user_id):
        user_obj = User.query.filter_by(id=user_id).first()
        if user_obj:
            res = jsonify({
                "user_id" : user_obj.id,
                "user_name" : user_obj.user_name,
                "profile_pic" : user_obj.profile_pic,
                "fs_uniquifier" : user_obj.fs_uniquifier,
            })
            print(res)
            return res
        else:
            return "Invalid User",404
         
    def post(self):
        user_name = request.form['user_name']
        password = request.form['password']
        email = request.form['email']
        file = request.files["profile_pic"]
        var_img = '../frontend/static/profile_pic/'+f'{user_name}.png'
        file.save(var_img)
        if user_name:
            if password:
                datastore.create_user(
                    user_name = user_name,
                    password = hash_password(password),
                    email=email,
                    profile_pic = var_img,
                )
                db.session.commit()
                return "Successfully created the User"
            else:
                return "Enter Valid Password",404
        else:
            return "Enter Failed User Name",404
    
    @auth_required('token')
    def put(self,user_name):
        print(user_name)
        curr_password = request.form['old_pass']
        
        # print(request.form['curr_password'],request.form['new_password'],request.files["new_profile_pic"])

        user_obj = User.query.filter_by(user_name=user_name).first()
        print(user_obj)
        if user_obj and  verify_password(curr_password,user_obj.password):
            print(curr_password)
            new_password = request.form['new_pass']
            print(new_password)
            try :
                file = request.files["new_profile_pic"]
                var_img = '../frontend/static/profile_pic/'+f'{user_name}.png'
                file.save(var_img)
                user_obj.profile_pic = var_img                
            finally:
                if new_password != 'null':
                    user_obj.password = hash_password(new_password)
                db.session.commit()

                return "Successfully updated the User Profile"                
        else:
            return "Enter Valid User Name or Password",404                  
    
    @auth_required('token')
    def delete(self,user_id):
        user_obj = User.query.filter_by(user_id=user_id)
        if user_obj.first():
            user_obj.delete()
            db.session.commit()
            return "Successfully Deleted",200
        else:
            return "Invalid Blog_ID",404          

cache.delete_memoized(USERAPI.get)

api.add_resource(BLOGAPI,'/api/create_blog/<usr_name>','/api/blog/<blog_id>')
api.add_resource(USERAPI,'/api/create_user','/api/user/<user_id>','/api/edit_user/<user_name>')
api.add_resource(LOGINAPI,'/api/login')
api.add_resource(GetAllBlogs,'/api/getAllBlogs/<usr_name>')
api.add_resource(MyFeed,'/api/Myfeed/<usr_name>')
api.add_resource(SearchAllUsers,'/api/search/<user_searching>/<search_val>')
api.add_resource(Follow,'/api/frnd_req/<username>/<friendname>/<val>')
api.add_resource(GetAllFollowers,'/api/followStat/<username>')

if __name__ == '__main__':
    app.run(debug=True,port=5050)       
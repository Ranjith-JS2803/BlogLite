from app import *
from flask_restful import Resource,Api,reqparse
from flask_cors import CORS

api = Api(app)
CORS(app)

blog_parser_PUT = reqparse.RequestParser()
blog_parser_PUT.add_argument('blog_description')
blog_parser_PUT.add_argument('blog_content')

class BLOGAPI(Resource):
    def get(self,blog_id):
        blog_obj = Blog.query.filter_by(blog_id=blog_id).first()
        if blog_obj != None:
            likes_obj = Likes.query.filter_by(ref_blog_id = blog_id).all()
            result = {
                    "Blog_id":blog_id,
                    "Blog_Title":blog_obj.title,
                    "Blog_Description":blog_obj.description,
                    "Blog_Content":blog_obj.content,
                    "Blog_image":blog_obj.image,
                    "Blog_Likes":len(likes_obj)
                    }
            return result,200
        else:
            return "Invalid Blog_ID",404
    
    def post(self):
        title = request.form['blog_title']
        des = request.form['blog_description']
        content = request.form['blog_content']
        image = request.files['blog_image']
        owner = request.form['blog_owner_id']
        if owner != '':
            user_obj = User.query.filter_by(user_id=owner).first()
            if user_obj:
                var_img = 'static/blog_images/'+image.filename
                image.save(var_img)
                blog_obj = Blog(title=title,description=des,content=content,image=var_img,ref_user_id=int(owner))
                db.session.add(blog_obj)
                db.session.commit()
                return "Successfully created the Blog"
            else:
                "User Doesn't Exist",404
        else:
            "Please specify User ID",404
    
    def put(self,blog_id):
        args = blog_parser_PUT.parse_args()
        des = args.get("blog_description",None)
        content = args.get("blog_content",None)
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
    
    def delete(self,blog_id):
        blog_obj = Blog.query.filter_by(blog_id=blog_id)
        if blog_obj.first():
            blog_obj.delete()
            Likes.query.filter_by(ref_blog_id=blog_id).delete()
            Comments.query.filter_by(ref_blog_id=blog_id).delete()
            db.session.commit()
            return "Successfully Deleted",200
        else:
            return "Invalid Blog_ID",404

api.add_resource(BLOGAPI,'/api/create_blog','/api/blog/<blog_id>')

if __name__ == '__main__':
    app.run(debug=True,port=5050)        
export default{
    template : `
    <div>
    <div class="container-fluid">
    <div class="row">
        <nav id="left" class="col-2">
            <div class="heading">
                <h2>Blog Lite</h2>
            </div>
            <div>
                <img :src="'../static/profile_pic/' + name + '.png'"/>
            </div>
            <router-link to="/profile" class="active"><i class="bi bi-person-lines-fill">&nbsp;&nbsp;Profile</i></router-link>
            <router-link to="/myfeed"><i class="bi bi-house-fill">&nbsp;&nbsp;Home</i></router-link>
            <router-link to="/search"><i class="bi bi-search">&nbsp;&nbsp;Search</i></router-link>
            <router-link to="/logout"><i class="bi bi-box-arrow-left">&nbsp;&nbsp;Logout</i></router-link>
        </nav>
        <div id="right" class="col-10">
            <div class="temp">
                <h2>Add a Blog/Post</h2>
            </div>            
            <form :action="'/addblog/'+name" method="POST" enctype="multipart/form-data">
                <div class="form-group">
                    <label for="title"><strong>Title :</strong> </label>
                    <textarea class="form-control" id="title" name="title" rows="1" v-model="title" required></textarea>
                </div>
                <br>
                <div class="form-group">
                    <label for="des"><strong>Description :</strong> </label>
                    <textarea class="form-control" id="des" name="des" rows="1" v-model="description" required></textarea>
                </div>
                <br>
                <div class="form-group">
                    <label for="content"><strong>Content :</strong> </label>
                    <textarea class="form-control" id="content" name="content" v-model="content" rows="10" required></textarea>
                </div>
                <br>
                <div class="form-group">
                    <label for="image"><strong>Image :</strong> </label>
                    <input type="file" class="form-control-file" id="image" name="image" required/>
                </div>
                <div class="temp">
                    <button @click="addPost" type="submit" class="btn btn-primary">Add Post</button>
                </div>
            </form>
        </div>
    </div>
</div>    
    </div>
    `,
    data(){
        return{
            title : null,
            description : null,
            content : null,
            name : localStorage.getItem("name")
        }
    },
    methods : {
        addPost(e){
            e.preventDefault();
            let url = 'http://localhost:5050/api/create_blog/' + this.name
            console.log(url)
            const formData = new FormData();
            formData.append('blog_title',this.title)
            formData.append('blog_description',this.description)
            formData.append('blog_content',this.content)
            formData.append('blog_image',document.getElementById('image').files[0])            
            fetch(url,{
                headers:{
                    'Authentication-Token' : localStorage.getItem('auth-token')
                },      
                method : 'POST',
                body:formData,
            }).then((res)=>{
                if(res.ok){
                    return res.json()
                }
            })
            .then((data)=>{
                console.log(data)
                this.$router.push('/profile');
            })
        }
    }
}
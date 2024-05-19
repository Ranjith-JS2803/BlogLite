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
                <div class="welcome-user"><h5>Welcome <em>{{name}}</em></h5></div>
                <div class="add-blog"><button class="btn btn-primary"><router-link to="/editprofile" class="add-blog">EDIT PROFILE</router-link></button></div>
                <br><br>
                <div class="head">
                    <div class="row">
                        <div class="col"><strong>No.Of Posts</strong></div>
                        <div class="col"><router-link :to="{path : '/friendsList/' + name , query :{q : 'followers'}}"><strong>Followers</strong></router-link></div>
                        <div class="col"><router-link :to="{path : '/friendsList/' + name , query :{q : 'following'}}"><strong>Following</strong></router-link></div>
                    </div>
                    <div class="row">
                        <div class="col"><strong>{{blogs.length}}</strong></div>
                        <div class="col"><strong>{{followers.length}}</strong></div>
                        <div class="col"><strong>{{following.length}}</strong></div>
                    </div>                      
                </div>    
                
                <div><h4>MY POSTS</h4></div>
                <div class="add-blog">
                    <button class="btn btn-primary"><router-link to="/addblog" class="add-blog">ADD POST</router-link></button>&nbsp;&nbsp;
                    <button class="btn btn-primary add-blog" @click="get_csv">EXPORT</button>
                </div>
                <br>
                <div class="row">
                    <div class="col-4 post" v-for="obj in blogs">
                        <strong>Title : </strong>{{obj.Blog_Title}} <br><br>
                        <strong>Description : </strong>{{obj.Blog_Description}}<br><br>
                        <div>
                            <button class="btn btn-primary read"><router-link :to="'/readblog/' + obj.Blog_id" class="text-col">Read</router-link></button>
                            <button class="btn btn-primary edit"><router-link :to="'/editblog/' + obj.Blog_id" class="text-col">Edit</router-link></button>
                            <button class="btn btn-primary delete"><router-link :to="'/deleteblog/' + obj.Blog_id" class="text-col">Delete</router-link></button>
                        </div>
                    </div>                                                                           
                </div>
            </div>
        </div>
    </div>    
    </div>
    `,
    data(){
        return {
            name : localStorage.getItem("name"),
            blogs : [],
            followers : [],
            following : []
        }
    },
    mounted(){
        var links = document.querySelectorAll(".link")
        console.log(links)
        
        for(var i=0;i<links.length ;i++){
            links[i].remove();
        }
        var l1 = document.createElement('link');
        l1.rel = "stylesheet";
        l1.classList.add("link")
        l1.href = "../static/main.css";
        var l2 = document.createElement('link');
        l2.rel = "stylesheet";
        l2.classList.add("link")
        l2.href = "../static/profile.css";        
        document.head.appendChild(l1);
        document.head.appendChild(l2);

        let url = 'http://localhost:5050/api/getAllBlogs/' + this.name
        
        fetch(url,{
            headers:{
                'Authentication-Token' : localStorage.getItem('auth-token')
            },      
        }).then((res)=>{
            if(res.ok){
                return res.json()
            }
        })
        .then((data)=>{
            this.blogs = data.blogs
        })        

        let url1 = 'http://localhost:5050/api/followStat/' + this.name
        
        fetch(url1,{
            headers:{
                'Authentication-Token' : localStorage.getItem('auth-token')
            },      
        }).then((res)=>{
            if(res.ok){
                return res.json()
            }
        })
        .then((data)=>{
            this.followers = data.result.Followers
            this.following = data.result.Following

        }) 

    },
    methods : {
        get_csv(){
            let url = 'http://localhost:5050/trigger-generate_csv/'+this.name;
            fetch(url,{
                headers:{
                    'Authentication-Token' : localStorage.getItem('auth-token')
                },      
            })
            .then((data) => data.json)
            .then((data) => {
                console.log(data);
                window.location.href = 'http://localhost:5050/download_file/'+this.name
                setTimeout(() => alert("Exported CSV") , 2000)
            })
        }
    }
}
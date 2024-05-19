export default{
    template:`
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
                <div class="welcome-friend">
                    <img :src="'../static/profile_pic/' + friendname + '.png'"/>
                    <h6>{{friendname}}</h6>
                </div>
                <br>
                <div class="head">
                    <div class="row">
                        <div class="col"><strong>No.Of Posts</strong></div>
                        <div class="col"><strong>Followers</strong></div>
                        <div class="col"><strong>Following</strong></div>
                    </div>
                    <div class="row">
                        <div class="col"><strong>{{blogs.length}}</strong></div>
                        <div class="col"><strong>{{followers.length}}</strong></div>
                        <div class="col"><strong>{{following.length}}</strong></div>
                    </div>                      
                </div>    
                
                <div><h4>POSTS</h4></div>
                <div class="add-blog">
                    <div class="request">
                    <button type="submit" id="follow" class="btn btn-primary" @click="follow(frnd_name,1)" :disabled="follow_val == 1">Follow</button>&nbsp;&nbsp;
                    <button type="submit" id="follow" class="btn btn-primary" @click="follow(frnd_name,0)" :disabled="follow_val != 1">Unfollow</button>
                    </div>
                </div>
                <br>
                <div class="row">
                    <div class="col-4 post" v-for="obj in blogs">
                        <strong>Title : </strong>{{obj.Blog_Title}} <br><br>
                        <strong>Description : </strong>{{obj.Blog_Description}}<br><br>
                        <div>
                            <button class="btn btn-primary read"><router-link :to="'/readblog/' + obj.Blog_id" class="text-col">Read</router-link></button>                    
                        </div>
                    </div>                                                                           
                </div>

            </div>
        </div>
    </div>
    </div>
    `,
    props : ["frnd_name"],
    data(){
        return{
            name : localStorage.getItem("name"),
            blogs : [],
            followers : [],
            following : [],
            friendname : this.frnd_name,
            follow_val : null
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

        let url = 'http://localhost:5050/api/getAllBlogs/' + this.frnd_name
        
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

        let url1 = 'http://localhost:5050/api/followStat/' + this.frnd_name
        
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
            for(var i=0; i<this.followers.length;i++){
                if (this.followers[i].friend_name === this.name){
                    this.follow_val = 1
                }
                else{
                    this.follow_val = 0
                }
            }
        }) 
    },
    methods:{
        follow(friendname,val){
            let url = 'http://localhost:5050/api/frnd_req/' + this.name + '/' + friendname + '/' + val
            fetch(url,{
                method : 'GET',
                headers:{
                    'Authentication-Token' : localStorage.getItem('auth-token')
                }
            }).then((res)=>{
                return res.json()
            }).then((data)=>{
                console.log(data);
            })
            
            let url2 = 'http://localhost:5050/api/followStat/' + this.frnd_name
        
            fetch(url2,{
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
                if(val === 1){
                    this.follow_val = 1
                }
                else{
                    this.follow_val = 0
                }
            }) 
        }
    }
}


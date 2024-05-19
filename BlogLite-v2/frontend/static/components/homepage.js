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
                <router-link to="/profile"><i class="bi bi-person-lines-fill">&nbsp;&nbsp;Profile</i></router-link>
                <router-link to="/myfeed" class="active"><i class="bi bi-house-fill">&nbsp;&nbsp;Home</i></router-link>
                <router-link to="/search"><i class="bi bi-search">&nbsp;&nbsp;Search</i></router-link>
                <router-link to="/logout"><i class="bi bi-box-arrow-left">&nbsp;&nbsp;Logout</i></router-link>
            </nav>
            <div id="right" class="col-10">
                <div><h4>MY FEED</h4></div>

                <div class="row">
                    <div class="col-6 post" v-if="blogs.length > 0" v-for="obj in blogs">
                        <strong>Title : </strong>{{obj.Blog_Title}} <br><br>
                        <strong>Owner : </strong><router-link :to="'/friendsprofile/' + obj.owner" >{{obj.owner}}</router-link><br><br>
                        <div>
                        <button class="btn btn-primary read"><router-link :to="'/readblog/' + obj.Blog_id" class="text-col">Read</router-link></button>
                        </div>
                    </div>  

                    <div class="col-12" v-else>
                        Follow friends to fill your feed with blogs
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
            blogs : []
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
        l2.href = "../static/myfeed.css";        
        document.head.appendChild(l1);
        document.head.appendChild(l2);

        let url = 'http://localhost:5050/api/Myfeed/' + this.name
        
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
            console.log(data.blogs)
        })
    }
}
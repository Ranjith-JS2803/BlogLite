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
            <div id="right" class="col-10" v-if="req == 'followers'">
                <strong><h1>Followers List</h1></strong>
                <div class="post" v-if="followers.length != 0" v-for="user in followers">
                    <div class="user">
                        <router-link :to="'/friendsprofile/' + user.friend_name" >{{user.friend_name}}</router-link>
                    </div>
                </div>

                <div class="col-12 default-following" v-if="followers.length == 0">
                    No Friend is following
                </div>                                                    
            </div>
            <div id="right" class="col-10" v-if="req == 'following'">
            <strong><h1>Following List</h1></strong>
            <div class="post" v-if="following.length != 0" v-for="user in following">
                <div class="user">
                    <router-link :to="'/friendsprofile/' + user.friend_name" >{{user.friend_name}}</router-link>
                </div>
            </div>

            <div class="col-12 default-following" v-if="following.length == 0">
                Not Following anyone
            </div>                                                    
        </div>
        </div>
    </div>
    </div>
    `,
    data(){
        return {
            followers : [1],
            following : [1],
            name : localStorage.getItem("name"),
            req : this.$route.query.q
        }
    },
    props : ["data"],
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
        l2.href = "../static/search.css";        
        document.head.appendChild(l1);
        document.head.appendChild(l2);

        let url = 'http://localhost:5050/api/followStat/' + this.name
        
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
            this.followers = data.result.Followers
            this.following = data.result.Following

        }) 
    }
}
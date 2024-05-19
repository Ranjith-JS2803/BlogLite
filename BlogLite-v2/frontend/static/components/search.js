export default {
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
                <router-link to="/profile"><i class="bi bi-person-lines-fill">&nbsp;&nbsp;Profile</i></router-link>
                <router-link to="/myfeed"><i class="bi bi-house-fill">&nbsp;&nbsp;Home</i></router-link>
                <router-link to="/search" class="active"><i class="bi bi-search">&nbsp;&nbsp;Search</i></router-link>
                <router-link to="/logout"><i class="bi bi-box-arrow-left">&nbsp;&nbsp;Logout</i></router-link>
            </nav>
            <div id="right" class="col-10">
                <form action="/search" method="POST" class="row g-3">
                    <div class="col-auto">
                        <input type="search" class="form-control" id="search_bar" name="search" placeholder="Search" v-model="search_val">
                    </div>
                    <div class="col-auto">
                    <button type="submit" @click="Search" class="btn btn-primary mb-3">
                        <span class="material-symbols-outlined">
                            search
                        </span>
                    </button>
                    </div>
                </form>
                <div class="post" v-for="frd_usr in search_list">
                    <div class="user">
                        <router-link :to="'/friendsprofile/' + frd_usr.friend_name" >{{frd_usr.friend_name}}</router-link>
                    </div>
                    <div class="request">
                        <button type="submit" id="follow" class="btn btn-primary" @click="follow(frd_usr.friend_name,1)" :disabled="frd_usr.follow_val == 1">Follow</button>&nbsp;&nbsp;
                        <button type="submit" id="follow" class="btn btn-primary" @click="follow(frd_usr.friend_name,0)" :disabled="frd_usr.follow_val == 0">Unfollow</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    </div>
    `,
    data(){
        return {
            name : localStorage.getItem('name'),
            search_val : localStorage.getItem('search_val'),
            search_list : [],
        }
    },
    methods : {
        Search(e){
            e.preventDefault();
            let url = 'http://localhost:5050/api/search/' + this.name + '/' + this.search_val
            fetch(url,{
                method : 'GET',
                headers:{
                    'Authentication-Token' : localStorage.getItem('auth-token')
                }
            }).then((res)=>{
                return res.json()
            }).then((data)=>{
                this.search_list = data.search_list
                console.log(this.search_list);
            })
        },
        follow(friendname,val){
            // e.preventDefault();
            console.log("Ranjith")
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

            let url1 = 'http://localhost:5050/api/search/' + this.name + '/' + this.search_val
            fetch(url1,{
                method : 'GET',
                headers:{
                    'Authentication-Token' : localStorage.getItem('auth-token')
                }
            }).then((res)=>{
                return res.json()
            }).then((data)=>{
                this.search_list = data.search_list
                console.log(this.search_list);
            })

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
        l2.href = "../static/search.css";        
        document.head.appendChild(l1);
        document.head.appendChild(l2);
    }
}

// {%if user_list|length != 0%}
// {%for i in user_list%}
// {%if i[1] == 1%}
    // <div class="post">
    //     <div class="user">
    //         <a href="/friend_profile">friend user_name </a>
    //     </div>
    //     <div class="request">
    //         <button type="submit" id="follow" class="btn btn-primary req-active" disabled><a href="/search/{{user_name}}?search_val={{search_val}}&req=1&friend={{i[0].user_name}}" class="text-col">Follow</a></button>&nbsp;&nbsp;
    //         <button type="submit" id="follow" class="btn btn-primary"><a href="/search/{{user_name}}?search_val={{search_val}}&req=0&friend={{i[0].user_name}}" class="text-col">Unfollow</a></button>
    //     </div>
    // </div>
// {%else%}
//     <div class="post">
//         <div class="user">
//             <a href="/friend_profile/{{user_name}}/{{i[0].user_name}}">{{i[0].user_name}}</a>
//         </div>
//         <div class="request">
//             <button type="submit" id="follow" class="btn btn-primary"><a href="/search/{{user_name}}?search_val={{search_val}}&req=1&friend={{i[0].user_name}}" class="text-col">Follow</a></button>&nbsp;&nbsp;
//             <button type="submit" id="follow" class="btn btn-primary req-active" disabled><a href="/search/{{user_name}}?search_val={{search_val}}&req=0&friend={{i[0].user_name}}" class="text-col">Unfollow</a></button>
//         </div>
//     </div>
// {%endif%}              
// {%endfor%}
// {%else%}
// <div>
//     <h1 id="not-found">User Not Found</h1>
// </div>
// {%endif%}
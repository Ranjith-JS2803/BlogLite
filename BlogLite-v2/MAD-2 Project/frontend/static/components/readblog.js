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
                <div class="head">
                    <div class="row title">
                        <h1>{{blog.Blog_Title}}</h1>
                        <h5>{{blog.Blog_Description}}</h5>
                    </div>
                </div>
                <div class="content">
                    <div class="row">
                        <div class="col-9">
                            <p>{{blog.Blog_Content}}</p>
                        </div>
                        <div class="col-3">
                            <img :src="'../static/blog_images/' + blog.owner + '-' + blog.Blog_Title + '.png'"/>
                            <h5>{{blog.Blog_Title}}</h5>
                        </div>
                    </div>
                </div>
                <br>
            </div>
        </div>
    </div>    
    </div>
    `,
    props : ["id"],
    data(){
        return {
            name : localStorage.getItem("name"),
            blog : {"Blog_Title" : null},
            comments : null,
            getComment : null
        }
    },
    mounted(){  
        var links = document.querySelectorAll(".link")
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
        l2.href = "../static/readblog.css";        
        document.head.appendChild(l1);
        document.head.appendChild(l2);     
        let url = 'http://localhost:5050/api/blog/' + this.id
        // console.log(url)
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
            this.blog = data
            this.comments = data.Blog_Comments
        }) 
    },
}
// {%if already_liked == None%}
// <button type="submit" id="follow" class="btn btn-primary req-active"><a href="/likes/{{user_name}}/{{blog.blog_id}}?like=1" class="text-col">Like</a></button>
// {%else%}
// <button type="submit" id="follow" class="btn btn-primary req-active"><a href="/likes/{{user_name}}/{{blog.blog_id}}?like=0" class="text-col">Dislike</a></button>
// {%endif%}
// methods :{
//     addComment(e){
//         let blog_id = this.blog.Blog_id;
//         e.preventDefault();
//         const formData = new FormData();
//         formData.append('comment',this.getComment)
//         let url = 'http://localhost:5050/api/addComment/' + blog_id + '/' + this.name;
//         console.log(url)
//         fetch(url,{
//             headers:{
//                 'Authentication-Token' : localStorage.getItem('auth-token')
//             },   
//             method : 'POST',
//             body:formData
//         }).then((res)=>{
//             return res.json()
//         }).then((data)=>{
//             console.log(data);
//         })
//         this.$router.push('/readblog/' + blog_id);
//         // this.$forceUpdate();
//     }
// },
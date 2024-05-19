export default{
    template:`
    <div>
        <div class="container">
            <div><img src="../static/BLOG LITE.png"/></div>
            <div class="block">
                <form action="/signup" method="POST" id="formid" enctype="multipart/form-data">
                    <div class="mb-3">
                    <label for="new_username" class="form-label">User Name</label>
                    <input type="name" class="form-control" id="new_username" name="new_username" v-model="new_username" required/>
                    </div>
                    <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input type="email" class="form-control" id="new_email" name="email" v-model="new_email"  required/>
                    </div><br>                
                    <div class="mb-3">
                    <label for="new_password" class="form-label">Password</label>
                    <input type="password" class="form-control" id="new_password" name="new_password" v-model="new_password" required/>
                    </div><br>
                    <div class="form-group">
                        <label for="image">Profile Picture : </label>
                        <input type="file" class="form-control-file" id="image" name="image">
                    </div><br>
                    <button type="submit" @click="signup" class="btn btn-primary">SIGN UP</button>
                </form>
            </div>
        </div>        
    </div>
    `,
    data(){
        return{
            new_username : null,
            new_email : null,
            new_password : null,
        }
    },   
    mounted(){
        var l = document.createElement('link');
        l.rel = "stylesheet";
        l.href = "../static/signin.css";
        l.classList.add("link")
        document.head.appendChild(l);
    },
    methods :{
        signup(e){
            e.preventDefault();
            const formData = new FormData();
            formData.append('user_name',this.new_username)
            formData.append('email',this.new_email)
            formData.append('password',this.new_password)
            formData.append('profile_pic',document.getElementById('image').files[0])

            fetch('http://localhost:5050/api/create_user',{
                method : 'POST',
                body:formData
            }).then((res)=>{
                return res.json()
            }).then((data)=>{
                console.log(data);
            })
            this.$router.push('/');  
        }
    },
}
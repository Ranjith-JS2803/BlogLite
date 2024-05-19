export default {
    template : `
    <div>
    <div class="container">
        <div><img src="../static/BLOG LITE.png"/></div>
        <div class="block">
            <form action="/" method="POST">
                <div class="mb-3">
                <label for="username" class="form-label">User Name</label>
                <input type="name" class="form-control" id="username" name="username" v-model="username" required />
                </div>
                <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" class="form-control" id="email" name="email" v-model="email" required/>
                </div>                
                <div class="mb-3">
                <label for="acc_password" class="form-label">Password</label>
                <input type="password" class="form-control" id="acc_password" name="acc_password" v-model="password" required/>
                </div>
                <button @click="login" class="btn btn-primary">SIGN IN</button>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span><router-link to='/signup' class="btn btn-primary">SIGN UP</router-link></span>
            </form>

        </div>
    </div>        
    </div>
    `,
    data(){
        return{
            username : null,
            email : null,
            password : null,
        }
    },
    mounted(){
        var l = document.createElement('link');
        l.rel = "stylesheet";
        l.href = "../static/signin.css";
        l.classList.add("link")
        document.head.appendChild(l);
    },
    methods:{
        login(e){
            e.preventDefault();
            let usr_name = this.username
            fetch('http://localhost:5050/api/login',{
                method : "POST",
                body:JSON.stringify({email : this.email,password : this.password}),
                headers:{
                    'Content-Type' : 'application/json'
                }
            }).then((res)=>{
                if(res.ok){
                    return res.json()
                }
            })
            .then((data)=>{
                if(data.active === true){
                    localStorage.setItem(
                        'auth-token',
                        data.token
                    );
                    localStorage.setItem(
                        'name',
                        usr_name
                    );
                this.$router.push('/profile');
                }
                else{
                    alert("Invalid UserName or Password")
                }
            })
        }               
    }
} 

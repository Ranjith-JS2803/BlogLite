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
            <br><br>
            <h2>EDIT PROFILE</h2>
            <br><br>
            <div class="block">
                <form action="/edit_profile" method="POST" enctype="multipart/form-data">
                    <div class="mb-3">
                    <label for="new_username" class="form-label"><strong>User Name</strong></label>
                    <input type="name" class="form-control" id="new_username" name="new_username" :value="name" disabled/>
                    </div><br>
                    <div class="mb-3">
                    <label for="old_password" class="form-label"><strong>Old Password</strong></label>
                    <input type="password" class="form-control" id="old_password" v-model="old_pass" name="old_password" required/>
                    </div><br>
                    <div class="mb-3">
                        <label for="new_password" class="form-label"><strong>New Password</strong></label>
                        <input type="password" class="form-control" id="new_password" v-model="new_pass" name="new_password" />
                        </div><br>
                    <div class="form-group">
                        <label for="image"><strong>Profile Picture : </strong></label>
                        <input type="file" class="form-control-file" id="image" name="image">
                    </div><br>
                    <div class="temp">
                        <button type="submit" @click="editProfile" class="btn btn-primary">SAVE EDIT</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
    </div>
    </div>
    `,
    data(){
        return {
            name : localStorage.getItem('name'),
            old_pass : null,
            new_pass : null
        }
    },
    methods : {
        editProfile(e){
            e.preventDefault();
            const formData = new FormData();
            formData.append('old_pass',this.old_pass)
            formData.append('new_pass',this.new_pass)
            formData.append('new_profile_pic',document.getElementById('image').files[0])
            let url = 'http://localhost:5050/api/edit_user/' + this.name
            fetch(url,{
                method : 'PUT',
                body:formData,
                headers:{
                    'Authentication-Token' : localStorage.getItem('auth-token')
                }
            }).then((res)=>{
                return res.json()
            }).then((data)=>{
                console.log(data);
                alert("Your Profile is Updated !!")
            })
        }
    }
}
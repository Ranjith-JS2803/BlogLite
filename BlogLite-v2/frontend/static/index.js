import login from './components/login.js'
import signup from './components/signup.js'
import profile from './components/profile.js'
import editProfile from './components/editprofile.js'
import addBlog from './components/addblog.js'
import readBlog from './components/readblog.js'
import editBlog from './components/editblog.js'
import deleteBlog from './components/deleteblog.js'
import search from './components/search.js'
import friendsList from './components/friendsList.js'
import myfeed from './components/homepage.js'
import friendsProfile from './components/friendsProfile.js'
import logout from './components/logout.js'

const routes =[
    { path : '/',component : login},
    { path : '/signup',component : signup},
    { path : '/profile',component : profile},
    { path : '/editprofile',component : editProfile},
    { path : '/addblog',component : addBlog},
    { path : '/readblog/:id',component : readBlog,props : true},
    { path : '/editblog/:id',component : editBlog,props : true},
    { path : '/deleteblog/:id',component : deleteBlog,props : true},
    { path : '/search',component : search},
    { path : '/friendsList/:data',component : friendsList,props : true},
    { path : '/myfeed' , component : myfeed},
    { path : '/friendsprofile/:frnd_name' , component : friendsProfile,props:true},
    { path : '/logout' , component : logout},
    { path : '*' , component : login }
]

const router = new VueRouter({
    routes
})


new Vue({
    el: '#app',
    template: `
    <div>
        <router-view></router-view>
    </div>
    `,
    router,
})

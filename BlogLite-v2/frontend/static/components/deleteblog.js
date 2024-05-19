export default{
    template : `<div></div>`,
    props : ["id"],
    methods : {
        deletePost(){
            let url = 'http://localhost:5050/api/blog/' + this.id          
            fetch(url,{
                headers:{
                    'Authentication-Token' : localStorage.getItem('auth-token')
                },      
                method : 'DELETE',
            }).then((res)=>{
                if(res.ok){
                    return res.json()
                }
            })
            .then((data)=>{
                console.log(data)
                this.$router.push('/profile');
            })
        }
    },
    created(){
        if(confirm("Are you sure you want to delete this blog ?")){
            this.deletePost()
        }
        else{
            this.$router.push('/profile');
        }
    },
}
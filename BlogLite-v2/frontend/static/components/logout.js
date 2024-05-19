export default{
    template :`<div></div>`,
    mounted(){
        localStorage.removeItem("auth-token");
        localStorage.removeItem("name");
        this.$router.push('/')
    }
}
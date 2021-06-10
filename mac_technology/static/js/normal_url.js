$("#profile_detail").click(function(e){
    console.log('dds')
    // let token = check_session()           
    // let path = "http://127.0.0.1:8000/home/" + token
    // console.log(path)
    // window.location.replace(path)

    });

function check_session(){
    try{
        token = sessionStorage.getItem('digitaltoken');
    }
    catch(e){
        alert('Humm token issues. Sorry you have to login first.')
        window.location.replace("http://127.0.0.1:8000/login/")
    }  
}
$(document).ready(function(){
    $("#button_login").click(function(e){
    e.preventDefault();
    let email = document.querySelector('#email');
    let pwd = document.querySelector('#pwd1');
    if (email.value == ""){
        alert("Email must be filled out");
    }else if(pwd.value == ""){
        alert("Password must be filled out")
    }else{
        $('.loader-box').show();
        var jsonData = {"email": email.value, "password":pwd.value}
        $.ajax({
            url: "http://127.0.0.1:8000/sign_in/",
            type: 'POST',
            contentType:'application/json',
            data: JSON.stringify(jsonData),
            dataType: 'json',
            success: function (response, textStatus, jqXHR){      
                if(jqXHR.status == 200){
                    if(response == "Email is not valid"){
                        alert(response);                        
                    }else if(response == "You gave wrong password"){
                        alert(response);
                    }else if(response == "Activate the account"){
                        pro_function(email = email.value);
                    
                    }
                    else {
                        console.log(response)
                        // sessionStorage.setItem('digitaltoken',JSON.stringify(response));
                        // goHome()
                        // let token = sessionStorage.getItem('digitaltoken');
                        // let path = "http://127.0.0.1:8000/home/"
                        window.location.replace("http://127.0.0.1:8000/login/home")
                    }
                }else{
                    alert(jqXHR);
                }
            $('.loader-box').hide();

            },
            error: function (response, textStatus, jqXHR) {
                alert(jqXHR);                        
                console.log(jqXHR)
            }
         })
    }
    $('.loader-box').hide();
    });
 });

 
function goHome(){
    let token = sessionStorage.getItem('digitaltoken');

    if(token == ""){
        window.location.replace("http://127.0.0.1:8000/login/")
    }
    else{
        let token = JSON.parse(sessionStorage.getItem('digitaltoken'));
        let h = new Headers();
        h.append('Authentication', `Bearer ${token}` );
        $.ajax({
            url: "http://127.0.0.1:8000/home/",
            type: 'GET',
            contentType:'application/json',
            headers: h,
            success: function (response, textStatus, jqXHR){      
                if(jqXHR.status == 200){
                        alert("logged in");
                }else{
                    alert(jqXHR);
                }
            },
            error: function (response, textStatus, jqXHR) {
                alert(jqXHR);                        
                console.log(jqXHR)
            }
         })
    }
}

$(document).ready(function(){
    $("#button_forget_password").click(function(e){
        e.preventDefault();
        let email = document.querySelector('#email');
        if (email.value == ""){
            alert("Email must be filled out");
        }else{
            $('.loader-box').show();
            var jsonData = {"email": email.value}
            $.ajax({
                url: 'http://127.0.0.1:8000/forget_password/email/',
                type: 'POST',
                contentType:'application/json',
                data: JSON.stringify(jsonData),
                dataType: 'json',
                success: function (response, textStatus, jqXHR) {
                    if(jqXHR.status == 201){
                        pro_forget_function(email.value)
                    }
                    else{
                        alert(response);
                    }
                $('.loader-box').hide();
                },
                error: function (response, textStatus, jqXHR) {
                    alert(jqXHR);                        
                    $('.loader-box').hide();
                }
             })
        }
    });
 });



function pro_forget_function(email){
    console.log(email)
    var code = prompt("Please check your mail and enter the token: ")
    if(code == null || code == ""){
        code = prompt("Pease check your mail and enter the token: ")
    }else{
        var jsonData = { "email": email, "token":code}
        $.ajax({
            url: '/forget_password/token/check/',
            type: 'POST',
            contentType:'application/json',
            data: JSON.stringify(jsonData),
            dataType: 'json',
            success: function (response, textStatus, jqXHR) {
                if(response == 'Token ok'){
                    set_new_password(email)
                }
                else{
                    alert(response)
                    pro_forget_function(email)
                }
            },
            error: function (response, textStatus, jqXHR) {
                alert(jqXHR);                        
                console.log(jqXHR)
            }
         })
    }
}

function set_new_password(email){
    var pass = prompt("New Password: ")
    var repassword = prompt("Re-password: ")

    if(pass != repassword){
        console.log(email)
        alert('New and Re Password is not matched. Try Again.')
        set_new_password(email)
    }else{
        var jsonData = { "email": email, "new_password":pass, "re_password":repassword}
        $.ajax({
            url: '/forget_password/change/',
            type: 'POST',
            contentType:'application/json',
            data: JSON.stringify(jsonData),
            dataType: 'json',
            success: function (response, textStatus, jqXHR) {
                if(response == 'Successfully change password'){
                    alert(response)
                    window.location.replace("http://127.0.0.1:8000/login/")
                }
                else{
                    alert(response)
                    console.log("ok")
                    set_new_password(email)
                }
            },
            error: function (response, textStatus, jqXHR) {
                alert(jqXHR);                        
                console.log(jqXHR)
            }
         })
    }

}

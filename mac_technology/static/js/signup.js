$(document).ready(function(){
    $("#formsubmit").click(function(e){
        e.preventDefault();
        let name = document.querySelector('#name');
        let email = document.querySelector('#email');
        let pwd = document.querySelector('#pwd1');
        let pwd1 = document.querySelector('#pwd2');
        let agree = document.getElementById("agree")
        if (name.value == ""){
            alert("Name must be filled out");
        }else if(email.value == ""){
            alert("Email must be filled out")
        }else if(pwd.value == ""){
            alert("Password must be filled out")
        }else if(pwd1.value == ""){
            alert("Repassword must be filled out")
        }else if(pwd.value != pwd1.value){
            alert("Password and repassword is not matching")  
        }else if(!agree.checked){
            alert("First check the agreement")
        }else{
            $('.loader-box').show();
            var jsonData = {"username": name.value, "email": email.value, "password":pwd.value}
            $.ajax({
                url: '/register/',
                type: 'POST',
                contentType:'application/json',
                data: JSON.stringify(jsonData),
                dataType: 'json',
                success: function (response, textStatus, jqXHR) {
                    if(jqXHR.status == 201){
                        pro_function(email = email.value);
                        window.location.replace("http://127.0.0.1:8000/login/")
                    }
                    else{
                        alert(response);
                    }
                $('.loader-box').hide();
                },
                error: function (response, textStatus, jqXHR) {
                    alert(jqXHR);                        
                    console.log(jqXHR)
                }
             })
        }
    });
 });



function pro_function(email){
    var code = prompt("Successfully register your account. But you need to activate your accout. pLease check your mail and enter the token: ")
    if(code == null || code == ""){
        code = prompt("Successfully register your account. But you need to activate your accout. pLease check your mail and enter the token: ")
    }else{
        var jsonData = { "email": email, "token":code}
        $.ajax({
            url: '/activate/',
            type: 'POST',
            contentType:'application/json',
            data: JSON.stringify(jsonData),
            dataType: 'json',
            success: function (response, textStatus, jqXHR) {
                if(jqXHR.status == 200){
                    alert(response)
                }
                else{
                    alert(response);
                }
            },
            error: function (response, textStatus, jqXHR) {
                alert(jqXHR);                        
                console.log(jqXHR)
            }
         })
        alert("Thank you")
    }
}
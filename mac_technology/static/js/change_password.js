$(document).ready(function(){
    $("#button_change_password").click(function(e){
        e.preventDefault();
        console.log("ok")
        let current_password = document.querySelector('#current_password');
        let new_password = document.querySelector('#new_password');
        let re_password = document.querySelector('#re_password');
        if (current_password.value == ""){
            alert("Current password must be filled out");
        }
        else if(new_password.value == ""){
            alert("New password must be filled out");
        }
        else if(re_password.value == ""){
            alert("New password must be filled out");
        }
        else if(re_password.value != new_password.value ){
            alert("New password must and re-password not matched");
        }
        else{
            $('.loader-box').show();
            var form = $('#change_password_form')[0];
            var form_data = new FormData(form);
            // var form_data = $(form).serialize();
            $.ajax({
                url: '/change_password/confirm/',
                type: 'POST',
                enctype: 'multipart/form-data',
                // contentType:'application/json',
                data: form_data,
                processData: false,
                contentType: false,
                cache: false,
                timeout: 60000,
                success: function (response, textStatus, jqXHR) {
                    if(jqXHR.status == 200){
                        alert(response);
                        if(response == 'Successfully change password')
                            window.location.replace("http://127.0.0.1:8000/logout/")
                    }
                    else{
                        alert(response);
                    }
                $('.loader-box').hide();
                },
                error: function (response, textStatus, jqXHR) {
                    alert(jqXHR);                        
                    console.log(jqXHR)
                    $('.loader-box').hide();
                }
             })
        }
    });
 });

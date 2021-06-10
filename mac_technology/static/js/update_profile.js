$(document).ready(function(){
    $("#update_profile_submit").click(function(e){
        e.preventDefault();
        let first_name = document.querySelector('#first_name');
        let last_name = document.querySelector('#last_name');
        let country = document.querySelector('#country');
        let city = document.querySelector('#city');
        let local_place = document.querySelector('#local_place');
        let contact = document.querySelector('#contact');
        let date_of_birth = document.querySelector('#date_of_birth');
    
        if (first_name.value == ""){
            alert("first name must be filled out");
        }else if(last_name.value == ""){
            alert("last name must be filled out")
        // }else if(country.value == ""){
        //     alert("country must be filled out")
        }else if(contact.value == ""){
            alert("contact must be filled out")
        }else if(date_of_birth == ""){
            alert("Date of birth must be choosen")   
        // }else if($('#signature')[0].files.length === 0){
        //     alert("Signature must be selected")
        }else{
            $('.loader-box').show();
            var form = $('#profile_form')[0];
            var form_data = new FormData(form);
            // var form_data = $(form).serialize();
            $.ajax({
                url: '/user_profile/',
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
                        window.location.replace("http://127.0.0.1:8000/login/home/")
                    }
                    else{
                        alert(response);
                        window.location.replace("http://127.0.0.1:8000/login/home/")
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
    $(".delete_user").click(function(e){
        e.preventDefault();
        console.log('ok')
        let user_id = $(this).data("userid");

        confirmation_delete(user_id)
    });
 });


function filechanged(){
    var selectedFile = document.getElementById('signature').files[0];
    var img = document.getElementById('img')
  
    var reader = new FileReader();
    reader.onload = function(){
       img.src = this.result
    }
    reader.readAsDataURL(selectedFile);
}

function confirmation_delete(user_id){
    var code = confirm("Do you really want to delete this user?")
    if(code == true){
        var api = 'http://127.0.0.1:8000/user/'+parseInt(user_id)+'/'
        console.log(api)
        $.ajax({
            url: api,
            type: 'DELETE',
            contentType:'application/json',
            dataType: 'json',
            success: function (response, textStatus, jqXHR) {
                console.log(response)
                if(response == "Deleted user"){
                    alert(response)
                    window.location.replace("http://127.0.0.1:8000/users/")
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
    }
}
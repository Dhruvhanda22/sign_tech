$(document).ready(function(){
    $("#add_contract").click(function(e){
        e.preventDefault();
        let name = document.querySelector('#name');
        let email = document.querySelector('#email');
        let position = document.querySelector('#position');
        let contract_time = document.querySelector('#contract_time');
        let salary = document.querySelector('#salary');

        if (name.value == ""){
            alert("Name must be filled out");
        }else if(email.value == ""){
            alert("Email must be filled out")
        }else if(position.value == ""){
            alert("Position must be filled out")
        }else if(contract_time.value == ""){
            alert("Contract of birth must be choosen")   
        }else if(salary.value == ""){
            alert("Contract of birth must be choosen")   
        }else{
            $('.loader-box').show();
            var form = $('#contract_forms')[0];
            var form_data = new FormData(form);
            $.ajax({
                url: '/contract/',
                type: 'POST',
                enctype: 'multipart/form-data',
                data: form_data,
                processData: false,
                contentType: false,
                cache: false,
                timeout: 600000,
                success: function (response, textStatus, jqXHR) {
                    if(jqXHR.status == 200){
                        if(response="Successfully added")
                            if(confirm(response)){
                                window.location.replace("http://127.0.0.1:8000/login/home")
                            }
                            else {
                                window.location.replace("http://127.0.0.1:8000/login/home")
                            }
                        else{
                            alert(response)
                        }
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

    $("#update_contract").click(function(e){
        e.preventDefault();
        let name = document.querySelector('#name');
        let email = document.querySelector('#email');
        let position = document.querySelector('#position');
        let contract_time = document.querySelector('#contract_time');
        let salary = document.querySelector('#salary');

        if (name.value == ""){
            alert("Name must be filled out");
        }else if(email.value == ""){
            alert("Email must be filled out")
        }else if(position.value == ""){
            alert("Position must be filled out")
        }else if(contract_time.value == ""){
            alert("Contract of birth must be choosen")   
        }else if(salary.value == ""){
            alert("Contract of birth must be choosen")   
        }else{
            $('.loader-box').show();
            var form = $('#contract_forms')[0];
            var form_data = new FormData(form);
            $.ajax({
                url: '/contract/',
                type: 'PUT',
                enctype: 'multipart/form-data',
                data: form_data,
                processData: false,
                contentType: false,
                cache: false,
                timeout: 600000,
                success: function (response, textStatus, jqXHR) {
                    if(jqXHR.status == 200){
                        if(response="Successfully updated")
                            if(confirm(response)){
                                window.location.replace("http://127.0.0.1:8000/login/home")
                            }
                            else {
                                window.location.replace("http://127.0.0.1:8000/login/home")
                            }
                        else{
                            alert(response)
                        }
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

    $("#submit_contract").click(function(e){
        e.preventDefault();
        
        let id = document.querySelector('#contract_id').value;
        
        if (document.getElementById("img").style.display = ""){
            alert("You have not Signature. So first Signature first.");
        }else if(id == ""){
            alert("Contract id is not found") 
        }else{
            $('.loader-box').show();
            var jsonData = {"contract_no": id}
            $.ajax({
                url: '/contract_sign/',
                type: 'PUT',
                contentType:'application/json',
                data: JSON.stringify(jsonData),
                dataType: 'json',
                success: function (response, textStatus, jqXHR) {
                    alert(response)
                    if(jqXHR.status == 200){
                        if(response="Successfully signature"){
                            window.location.replace("http://127.0.0.1:8000/login/home")
                        }
                        else{
                            window.location.replace("http://127.0.0.1:8000/login/home")
                        }
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





 function display_signature(){
    document.getElementById("img").style.display = "";
    document.getElementById("submit_contract").style.display = "";
    document.getElementById("signature_submit").style.display = "none";
 }
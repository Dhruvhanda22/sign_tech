$(document).ready(function(){
    $("#cv_submit").click(function(e){
        e.preventDefault();
        let profession = document.querySelector('#profession');
        let education = document.querySelector('#education');
        let skills = document.querySelector('#skills');
        let experience_detail = document.querySelector('#experience_detail');
        let reference_name = document.querySelector('#reference_name');
        let reference_workat = document.querySelector('#reference_workat');
        let reference_position = document.querySelector('#reference_position');
        let reference_email = document.querySelector('#reference_email');
        let reference_contact = document.querySelector('#reference_contact');

        if (profession.value == ""){
            alert("job title must be filled out");
        }else if(education.value == ""){
            alert("education must be filled out")
        }else if(skills.value == ""){
            alert("Salary must be filled out")
        }else if(experience_detail.value == ""){
            alert("experience year must be filled out")
        }
        else{
            $('.loader-box').show();
            var form = $('#cv_form')[0];
            var form_data = new FormData(form);
            // var form_data = $(form).serialize();
            $.ajax({
                url: '/cv_add/',
                type: 'POST',
                enctype: 'multipart/form-data',
                data: form_data,
                processData: false,
                contentType: false,
                cache: false,
                timeout: 600000,
                success: function (response, textStatus, jqXHR) {
                    if(jqXHR.status == 200){
                        alert(response);
                        document.getElementById("myFieldset").disabled = true;
                        $('#enable_editing').show();
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
function myFunction() {
    document.getElementById("myFieldset").disabled = false;
    $('#enable_editing').hide();
}
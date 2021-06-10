$(document).ready(function(){
    $("#add_vacancy_submit").click(function(e){
        e.preventDefault();
        let job_title  = document.querySelector('#job_title');
        let education  = document.querySelector('#education');
        let range_of_salary  = document.querySelector('#range_of_salary');
        let plus_services  = document.querySelector('#plus_services');
        let experience_year  = document.querySelector('#experience_year');
        let expiry_date   = document.querySelector('#expiry_date');
        let task_and_responsibilities  = document.querySelector('#task_and_responsibilities');
        let qualification_and_experience  = document.querySelector('#qualification_and_experience');
        let contract_time  = document.querySelector('#contract_time');

        if (job_title.value == ""){
            alert("job title must be filled out");
        }else if(education.value == ""){
            alert("education must be filled out")
        }else if(range_of_salary.value == ""){
            alert("Salary must be filled out")
        }else if(experience_year.value == ""){
            alert("experience year must be filled out")
        }else if(expiry_date.value == ""){
            alert("expiry date must be choosen")   
        }else if(task_and_responsibilities.value == ""){
            alert("task and responsibilities must be choosen")   
        }else if(qualification_and_experience.value == ""){
            alert("qualification and experience must be choosen")   
        }else if(contract_time.value == ""){
            alert("contract time must be choosen")   
        }
        else{
            $('.loader-box').show();
            var form = $('#vacancy_form')[0];
            var form_data = new FormData(form);
            // var form_data = $(form).serialize();
            $.ajax({
                url: '/vacancy/',
                type: 'POST',
                enctype: 'multipart/form-data',
                data: form_data,
                processData: false,
                contentType: false,
                cache: false,
                timeout: 600000,
                success: function (response, textStatus, jqXHR) {
                    if(jqXHR.status == 201){
                        alert(response);
                        document.getElementById("vacancy_form").reset();
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


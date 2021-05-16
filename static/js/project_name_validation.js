const project_name_target = document.querySelector('#name');
const invalid_feedback = document.querySelector('.invalid-feedback');
const valid_feedback = document.querySelector('.valid-feedback');
project_name_target.addEventListener('keyup',(input) =>{
    const user_proj_name = input.target.value
    project_name_target.classList.remove("is-invalid")
    project_name_target.classList.remove("is-valid")
    invalid_feedback.style.display = "none";
   
    if(user_proj_name.length > 0){
        fetch("/validate_project",{
            body : JSON.stringify({name:user_proj_name}),
            method : "POST",
        }).then((res)=>res.json()).then((data)=>{
            if (data.project_name_error){
                project_name_target.classList.add("is-invalid")
                invalid_feedback.style.display = "block";
                valid_feedback.style.color = "red";
                invalid_feedback.innerHTML = `<p><strong> ${data.project_name_error}</strong></p>`
            }
            if(data.project_name_valid){
                project_name_target.classList.add("is-valid")
                valid_feedback.style.display = "block";
                valid_feedback.style.color = "green";
                valid_feedback.innerHTML = `<p><strong> ${data.project_name_valid}</strong></p>`
            }

        });
    

    }
 
});
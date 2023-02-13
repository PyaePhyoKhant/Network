document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.edit').forEach(element => {
        element.addEventListener('click', function() {
            // hide elements
            element.style.display = 'none';
            const created_time_element = element.previousElementSibling.previousElementSibling;
            created_time_element.style.display = 'none';
            const description_element = element.previousElementSibling.previousElementSibling.previousElementSibling;
            description_element.style.display = 'none';

            // show elements
            const edit_form_element = element.previousElementSibling;
            edit_form_element.style.display = 'block';
        })
    })
    
    document.querySelectorAll('.edit-save').forEach(element => {
        element.addEventListener('click', function() {
            event.preventDefault();

            const form = element.form;
            const url = form.action;
            const id = form.elements.id.value;
            const description = form.elements.description.value;
            
            fetch(url, {
                method: 'PUT',
                body: JSON.stringify({
                    id: id,
                    description: description
                })
            })
            .then(function() {
                // hide elements
                form.style.display = 'none';

                // show elements
                const edit_button = form.nextElementSibling;
                edit_button.style.display = 'block';
                const created_time_element = edit_button.previousElementSibling.previousElementSibling;
                created_time_element.style.display = 'block';
                const description_element = edit_button.previousElementSibling.previousElementSibling.previousElementSibling;
                description_element.style.display = 'block';
                description_element.innerHTML = description;
            })
            .catch(error => alert('Error updating post. :('));

            return false;
        })
    })
})
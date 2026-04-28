document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('registration-form')
    const registrationModal = document.getElementById('registration-modal')

    form.addEventListener('submit', async (e) => {
        e.preventDefault()

        const formData = new FormData(form)
        try {
            const response = await fetch('/register', {
                method: 'POST',
                body: formData
            })

            const data = await response.json()

            if (data.success) {

                registrationModal.classList.remove('hidden')
                registrationModal.classList.add('flex')
                alert(data.message);
                form.reset();
            } else {
                alert('Something went wrong');
            }

        } catch (error) {
            console.error('Error', error)
        }
    })

    
})
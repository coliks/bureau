document.addEventListener('DOMContentLoaded', () => {
    const addBusinessModalOpenerBtn = document.getElementById('add-business-modal-opener')
    const businessFormModal = document.getElementById('business-form-modal')
    const businessFormCloserBtn = document.getElementById('business-form-closer')


    addBusinessModalOpenerBtn.addEventListener('click', () => {
        if (businessFormModal.classList.contains('hidden')) {
            businessFormModal.classList.remove('hidden')
            businessFormModal.classList.add('flex')
        }
    })

    businessFormCloserBtn.addEventListener('click', () => {
        if (businessFormModal.classList.contains('flex')) {
            businessFormModal.classList.remove('flex')
            businessFormModal.classList.add('hidden')
        }
    })



})
document.addEventListener('DOMContentLoaded', () => {
    let confirmCallback = null

    function showConfirmModal(title, message, isDanger = true, confirmText = 'Confirm') {
        return new Promise((resolve) => {
            const modal = document.getElementById('custom-confirm-modal')
            const titleEl = document.getElementById('confirm-title')
            const messageEl = document.getElementById('confirm-message')
            const cancelBtn = modal.querySelector('#confirm-cancel-btn')
            const actionBtn = modal.querySelector('#confirm-action-btn')
            const iconContainer = document.getElementById('confirm-icon-container')
            const iconEl = document.getElementById('confirm-icon')

            titleEl.textContent = title
            messageEl.textContent = message
            actionBtn.textContent = confirmText

            if (isDanger) {
                iconContainer.className = 'p-4 bg-red-50 rounded-full'
                iconEl.className = 'w-8 h-8 text-red-600'
                iconEl.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866 1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />`
                actionBtn.className = 'flex-1 px-4 py-3 bg-red-600 text-white text-sm font-semibold rounded-xl hover:bg-red-700 transition-all duration-200'
            } else {
                iconContainer.className = 'p-4 bg-blue-50 rounded-full'
                iconEl.className = 'w-8 h-8 text-blue-600'
                iconEl.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />`
                actionBtn.className = 'flex-1 px-4 py-3 bg-blue-600 text-white text-sm font-semibold rounded-xl hover:bg-blue-700 transition-all duration-200'
            }

            modal.classList.remove('hidden')
            modal.classList.add('flex')

            confirmCallback = (confirmed) => {
                modal.classList.add('hidden')
                modal.classList.remove('flex')
                resolve(confirmed)
            }

            cancelBtn.onclick = () => confirmCallback(false)
            actionBtn.onclick = () => confirmCallback(true)

            modal.onclick = (e) => {
                if (e.target === modal) {
                    confirmCallback(false)
                }
            }
        })
    }

    const filterBtn = document.getElementById('filter-btn')
    const filterDropdown = document.getElementById('filter-dropdown')
    const filterLabel = document.getElementById('filter-label')
    const filterOptions = document.querySelectorAll('.filter-option')
    
    function updateRadioStyles() {
        filterOptions.forEach((option) => {
            const radioInput = option.querySelector('input[type="radio"]')
            const radioCircle = option.querySelector('.radio-circle')
            const radioDot = option.querySelector('.radio-dot')
            
            if (radioInput && radioInput.checked) {
                radioCircle.className = 'w-5 h-5 rounded-full border-2 border-blue-500 flex items-center justify-center radio-circle bg-blue-50'
                if (radioDot) radioDot.classList.remove('hidden')
            } else {
                radioCircle.className = 'w-5 h-5 rounded-full border-2 border-gray-300 flex items-center justify-center radio-circle'
                if (radioDot) radioDot.classList.add('hidden')
            }
        })
    }
    
    if (filterBtn && filterDropdown) {
        filterBtn.addEventListener('click', function (e) {
            e.stopPropagation()
            filterDropdown.classList.toggle('hidden')
        })
        
        document.addEventListener('click', function (e) {
            if (!filterDropdown.contains(e.target) && !filterBtn.contains(e.target)) {
                filterDropdown.classList.add('hidden')
            }
        })
    }
    
    filterOptions.forEach((option) => {
        option.addEventListener('click', function () {
            const filter = this.dataset.filter
            const radioInput = this.querySelector('input[type="radio"]')
            if (radioInput) {
                radioInput.checked = true
            }
            filterLabel.textContent = `Filter by: ${filter.charAt(0).toUpperCase() + filter.slice(1)}`
            filterDropdown.classList.add('hidden')
            updateRadioStyles()
        })
    })
    
    updateRadioStyles()

    const addBusinessModalOpenerBtn = document.getElementById('add-business-modal-opener')
    const businessFormModal = document.getElementById('add-business-modal')
    const businessFormCloserBtn = document.getElementById('close-add-business-modal')
    const cancelAddBusiness = document.getElementById('cancel-add-business')
    const addBusinessForm = document.getElementById('add-business-form')
    const businessInfoModal = document.getElementById('business-info-modal')
    const closeBusinessInfoModal = document.getElementById('close-business-info-modal')
    let viewBusinessBtns = document.querySelectorAll('.view-business-btn')
    const imageUploadDiv = document.getElementById('business-image-upload')
    const imageInput = document.getElementById('business-image-input')
    const imagesGrid = document.getElementById('business-images-grid')
    let existingImages = []

    function getStaticUploadUrl(filename) {
        return `/static/uploads/${filename}`
    }

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

    const addImageUploadDiv = document.getElementById('add-business-image-upload')
    const addImageInput = document.getElementById('add-business-image-input')
    const addImagesGrid = document.getElementById('add-business-images-grid')
    let addSelectedFiles = []

    function addAddImageCard(file) {
        const card = document.createElement('div')
        card.className = 'aspect-square rounded-xl overflow-hidden bg-gray-50 relative group'
        
        const img = document.createElement('img')
        img.src = URL.createObjectURL(file)
        img.className = 'w-full h-full object-cover'
        
        const removeBtn = document.createElement('button')
        removeBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-5 h-5 text-white">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
        </svg>`
        removeBtn.className = 'absolute top-2 right-2 p-1.5 bg-red-500 rounded-full shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200'
        removeBtn.addEventListener('click', function(e) {
            e.stopPropagation()
            const index = Array.from(addImagesGrid.children).indexOf(card)
            addSelectedFiles.splice(index, 1)
            card.remove()
            updateAddImageInput()
        })
        
        card.appendChild(img)
        card.appendChild(removeBtn)
        addImagesGrid.appendChild(card)
    }

    function updateAddImageInput() {
        const dt = new DataTransfer()
        addSelectedFiles.forEach(file => dt.items.add(file))
        addImageInput.files = dt.files
    }

    if (addImageUploadDiv && addImageInput) {
        addImageUploadDiv.addEventListener('click', () => addImageInput.click())
        
        addImageInput.addEventListener('change', function() {
            Array.from(this.files).forEach(file => {
                addSelectedFiles.push(file)
                addAddImageCard(file)
            })
            updateAddImageInput()
        })
        
        addImageUploadDiv.addEventListener('dragover', function(e) {
            e.preventDefault()
            this.classList.add('border-green-500', 'bg-green-50')
        })
        
        addImageUploadDiv.addEventListener('dragleave', function(e) {
            e.preventDefault()
            this.classList.remove('border-green-500', 'bg-green-50')
        })
        
        addImageUploadDiv.addEventListener('drop', function(e) {
            e.preventDefault()
            this.classList.remove('border-green-500', 'bg-green-50')
            Array.from(e.dataTransfer.files).forEach(file => {
                if (file.type.startsWith('image/')) {
                    addSelectedFiles.push(file)
                    addAddImageCard(file)
                }
            })
            updateAddImageInput()
        })
    }

    if (cancelAddBusiness) {
        cancelAddBusiness.addEventListener('click', () => {
            businessFormModal.classList.add('hidden')
            businessFormModal.classList.remove('flex')
            addImagesGrid.innerHTML = ''
            addSelectedFiles = []
            const dt = new DataTransfer()
            addImageInput.files = dt.files
        })
    }
    
    businessFormCloserBtn.addEventListener('click', () => {
        if (businessFormModal.classList.contains('flex')) {
            businessFormModal.classList.remove('flex')
            businessFormModal.classList.add('hidden')
            addImagesGrid.innerHTML = ''
            addSelectedFiles = []
            const dt = new DataTransfer()
            addImageInput.files = dt.files
        }
    })





    const editForm = document.getElementById('edit-business-form')
    let pendingFormSubmit = false

    if (editForm) {
        editForm.addEventListener('submit', async function(e) {
            if (!pendingFormSubmit) {
                e.preventDefault()
                const confirmed = await showConfirmModal(
                    'Save Changes',
                    'Are you sure you want to save these changes?',
                    false,
                    'Save'
                )
                if (confirmed) {
                    pendingFormSubmit = true
                    editForm.submit()
                }
            }
        })
    }

    const archiveBtn = document.getElementById('archive-business-btn')
    let currentBusinessId = null

    if (archiveBtn) {
        archiveBtn.addEventListener('click', async function() {
            currentBusinessId = document.getElementById('edit-business-id').value
            const confirmed = await showConfirmModal(
                'Archive Business',
                'Are you sure you want to archive this business?',
                true,
                'Archive'
            )
            if (confirmed && currentBusinessId) {
                const form = document.createElement('form')
                form.method = 'POST'
                form.action = `/admin/business/${currentBusinessId}/archive`
                document.body.appendChild(form)
                form.submit()
            }
        })
    }

    const archivedBtn = document.getElementById('archived-btn')
    const archivedModal = document.getElementById('archived-modal')
    const closeArchivedModal = document.getElementById('close-archived-modal')
    const exportBtn = document.getElementById('export-business-btn')

    if (exportBtn) {
        exportBtn.addEventListener('click', async function(e) {
            e.preventDefault()
            const confirmed = await showConfirmModal(
                'Export Businesses',
                'Do you want to export the business records as an Excel file?',
                false,
                'Export'
            )
            if (confirmed) {
                window.location.href = exportBtn.href
            }
        })
    }

    function setupAllViewButtons() {
        const allViewBtns = document.querySelectorAll('.view-business-btn')
        allViewBtns.forEach((btn) => {
            if (!btn.dataset.listenerAdded) {
                btn.dataset.listenerAdded = 'true'
                btn.addEventListener('click', function() {
                    const businessData = this.dataset
                    
                    document.getElementById('edit-business-id').value = businessData.businessId
                    document.getElementById('edit-business-name').value = businessData.businessName
                    document.getElementById('edit-business-address').value = businessData.businessAddress
                    document.getElementById('edit-owner-name').value = businessData.ownerName
                    document.getElementById('edit-representative-name').value = businessData.representativeName
                    document.getElementById('edit-contact-number').value = businessData.contactNumber
                    document.getElementById('edit-business-id-code').value = businessData.businessIdCode
                    document.getElementById('edit-control-no').value = businessData.controlNo
                    document.getElementById('edit-application-no').value = businessData.applicationNo
                    document.getElementById('edit-status').value = businessData.status
                    const buildingPermitFeeEl = document.getElementById('edit-building-permit-fee')
                    if (buildingPermitFeeEl) buildingPermitFeeEl.value = businessData.buildingPermitFee
                    const zoningFeeEl = document.getElementById('edit-zoning-fee')
                    if (zoningFeeEl) zoningFeeEl.value = businessData.zoningFee
                    const occupancyFeeEl = document.getElementById('edit-occupancy-fee')
                    if (occupancyFeeEl) occupancyFeeEl.value = businessData.occupancyFee
                    document.getElementById('edit-fire-inspection-fee').value = businessData.fireInspectionFee
                    document.getElementById('edit-or-no').value = businessData.orNo

                    existingImages = []
                    const existingImagesGrid = imagesGrid.querySelectorAll('.aspect-square:not(#business-image-upload)')
                    existingImagesGrid.forEach(img => img.remove())

                    if (businessData.businessImages) {
                        try {
                            existingImages = JSON.parse(businessData.businessImages)
                            existingImages.forEach((imgFilename) => {
                                addImageCard(getStaticUploadUrl(imgFilename), imgFilename, true)
                            })
                        } catch (e) {
                            console.error('Error parsing existing images:', e)
                        }
                    }

                    document.getElementById('existing-business-images').value = JSON.stringify(existingImages)

                    businessInfoModal.classList.remove('hidden')
                })
            }
        })
    }

    setupAllViewButtons()

    function handleRetrieveDeleteButtons() {
        const retrieveBtns = document.querySelectorAll('.retrieve-business-btn')
        const deleteBtns = document.querySelectorAll('.delete-business-btn')

        retrieveBtns.forEach((btn) => {
            if (!btn.dataset.listenerAdded) {
                btn.dataset.listenerAdded = 'true'
                btn.addEventListener('click', async function() {
                    const confirmed = await showConfirmModal(
                        'Retrieve Business',
                        'Are you sure you want to retrieve this business?',
                        false,
                        'Retrieve'
                    )
                    if (confirmed) {
                        const businessId = this.dataset.businessId
                        const form = document.createElement('form')
                        form.method = 'POST'
                        form.action = `/admin/business/${businessId}/retrieve`
                        document.body.appendChild(form)
                        form.submit()
                    }
                })
            }
        })

        deleteBtns.forEach((btn) => {
            if (!btn.dataset.listenerAdded) {
                btn.dataset.listenerAdded = 'true'
                btn.addEventListener('click', async function() {
                    const confirmed = await showConfirmModal(
                        'Delete Business',
                        'Are you sure you want to delete this business? This action cannot be undone!',
                        true,
                        'Delete'
                    )
                    if (confirmed) {
                        const businessId = this.dataset.businessId
                        const form = document.createElement('form')
                        form.method = 'POST'
                        form.action = `/admin/business/${businessId}/delete`
                        document.body.appendChild(form)
                        form.submit()
                    }
                })
            }
        })
    }

    handleRetrieveDeleteButtons()

    // ── Archived modal with client-side pagination ───────────────────────────
    const ARCHIVED_PER_PAGE = 5
    let archivedCurrentPage = 1

    const archivedDataEl = document.getElementById('archived-businesses-data')
    const archivedData = archivedDataEl ? JSON.parse(archivedDataEl.textContent) : []

    const listContainer = document.getElementById('archived-list-container')
    const paginationEl = document.getElementById('archived-pagination')
    const pageInfoEl = document.getElementById('archived-page-info')
    const pageNumbersEl = document.getElementById('archived-page-numbers')
    const prevBtn = document.getElementById('archived-prev-btn')
    const nextBtn = document.getElementById('archived-next-btn')

    function escHtml(str) {
        return String(str || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')
    }

    function renderArchivedPage(page) {
        if (!listContainer) return
        archivedCurrentPage = page
        const total = archivedData.length
        const totalPages = Math.max(1, Math.ceil(total / ARCHIVED_PER_PAGE))
        const start = (page - 1) * ARCHIVED_PER_PAGE
        const slice = archivedData.slice(start, start + ARCHIVED_PER_PAGE)

        if (total === 0) {
            listContainer.innerHTML = `
              <div class="flex flex-col items-center justify-center py-16 text-gray-500">
                <div class="p-6 bg-gray-50 rounded-full mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-12 h-12 text-gray-400">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m20.25 7.5-.625 10.632a2.25 2.25 0 0 1-2.247 2.118H6.622a2.25 2.25 0 0 1-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125Z"/>
                  </svg>
                </div>
                <h3 class="text-sm font-semibold text-gray-700">No archived businesses</h3>
                <p class="text-xs text-gray-500 mt-1">No businesses have been archived yet.</p>
              </div>`
            if (paginationEl) paginationEl.classList.add('hidden')
            return
        }

        listContainer.innerHTML = slice.map(b => `
          <div class="flex items-center gap-5 p-5 bg-white rounded-md border border-gray-200 hover:border-orange-300 transition-colors duration-200">
            <div class="flex-shrink-0">
              <div class="bg-orange-600 rounded-md h-14 w-14 flex items-center justify-center">
                <span class="text-white font-bold text-lg">${escHtml(b.business_name[0]).toUpperCase()}</span>
              </div>
            </div>
            <div class="flex-grow min-w-0">
              <div class="flex items-center gap-3 flex-wrap">
                <h3 class="text-base font-semibold text-gray-800 truncate">${escHtml(b.business_name)}</h3>
                <span class="px-3 py-1 text-xs font-semibold bg-orange-100 text-orange-600 rounded-full">Archived</span>
              </div>
              <div class="flex items-center gap-3 mt-1.5 flex-wrap">
                <span class="flex items-center gap-1.5 text-xs text-gray-500 bg-white px-2 py-1 rounded-md border border-gray-200">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-3.5 h-3.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0ZM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632Z"/></svg>
                  ${escHtml(b.owner_name)}
                </span>
                <span class="flex items-center gap-1.5 text-xs text-gray-500 bg-white px-2 py-1 rounded-md border border-gray-200">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-3.5 h-3.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z"/></svg>
                  ${escHtml(b.business_address)}
                </span>
              </div>
            </div>
            <div class="flex items-center gap-2 flex-shrink-0">
              <button type="button" class="retrieve-business-btn flex items-center gap-2 px-4 py-2.5 bg-green-600 text-white text-xs font-semibold rounded-md hover:bg-green-700 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-green-500/30" data-business-id="${b.id}">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                Retrieve
              </button>
              <button type="button" class="delete-business-btn flex items-center gap-2 px-4 py-2.5 bg-white text-red-600 text-xs font-semibold rounded-md border border-red-200 hover:bg-red-50 hover:border-red-300 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-red-500/20" data-business-id="${b.id}">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0"/></svg>
                Delete
              </button>
            </div>
          </div>`).join('')

        // pagination controls
        if (paginationEl) {
            if (totalPages > 1) {
                paginationEl.classList.remove('hidden')
                pageInfoEl.textContent = `Page ${page} of ${totalPages} (${total} total)`

                // prev
                if (page <= 1) {
                    prevBtn.disabled = true
                    prevBtn.className = 'text-xs px-4 py-2 rounded-md font-medium bg-gray-200 text-gray-400 cursor-not-allowed'
                } else {
                    prevBtn.disabled = false
                    prevBtn.className = 'text-xs px-4 py-2 rounded-md font-medium bg-blue-600 text-white hover:bg-blue-700 transition-colors duration-200'
                }

                // next
                if (page >= totalPages) {
                    nextBtn.disabled = true
                    nextBtn.className = 'text-xs px-4 py-2 rounded-md font-medium bg-gray-200 text-gray-400 cursor-not-allowed'
                } else {
                    nextBtn.disabled = false
                    nextBtn.className = 'text-xs px-4 py-2 rounded-md font-medium bg-blue-600 text-white hover:bg-blue-700 transition-colors duration-200'
                }

                // page numbers
                pageNumbersEl.innerHTML = ''
                const startP = Math.max(1, page - 2)
                const endP = Math.min(totalPages, page + 2)
                for (let p = startP; p <= endP; p++) {
                    const btn = document.createElement('button')
                    btn.type = 'button'
                    btn.textContent = p
                    btn.className = `text-xs px-3 py-2 rounded-md font-medium transition-colors duration-200 ${p === page ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'}`
                    btn.addEventListener('click', () => { renderArchivedPage(p); handleRetrieveDeleteButtons() })
                    pageNumbersEl.appendChild(btn)
                }
            } else {
                paginationEl.classList.add('hidden')
            }
        }

        handleRetrieveDeleteButtons()
    }

    if (prevBtn) prevBtn.addEventListener('click', () => { if (archivedCurrentPage > 1) { renderArchivedPage(archivedCurrentPage - 1); handleRetrieveDeleteButtons() } })
    if (nextBtn) nextBtn.addEventListener('click', () => { const tp = Math.ceil(archivedData.length / ARCHIVED_PER_PAGE); if (archivedCurrentPage < tp) { renderArchivedPage(archivedCurrentPage + 1); handleRetrieveDeleteButtons() } })

    if (archivedBtn && archivedModal) {
        archivedBtn.addEventListener('click', function() {
            archivedModal.classList.remove('hidden')
            archivedModal.classList.add('flex')
            renderArchivedPage(1)
            setupAllViewButtons()
        })
    }

    if (closeArchivedModal && archivedModal) {
        closeArchivedModal.addEventListener('click', function() {
            archivedModal.classList.add('hidden')
            archivedModal.classList.remove('flex')
        })
    }

    if (archivedModal) {
        archivedModal.addEventListener('click', function(e) {
            if (e.target === archivedModal) {
                archivedModal.classList.add('hidden')
                archivedModal.classList.remove('flex')
            }
        })
    }

    if (closeBusinessInfoModal) {
        closeBusinessInfoModal.addEventListener('click', () => {
            businessInfoModal.classList.add('hidden')
        })
    }

    if (businessInfoModal) {
        businessInfoModal.addEventListener('click', function(e) {
            if (e.target === businessInfoModal) {
                businessInfoModal.classList.add('hidden')
            }
        })
    }

    if (imageUploadDiv && imageInput) {
        imageUploadDiv.addEventListener('click', function () {
            imageInput.click()
        })

        imageInput.addEventListener('change', function (e) {
            const files = e.target.files
            Array.from(files).forEach((file) => {
                const reader = new FileReader()
                reader.onload = function (event) {
                    addImageCard(event.target.result, false)
                }
                reader.readAsDataURL(file)
            })
        })
    }

    function addImageCard(src, filename, isExisting) {
        const imageCard = document.createElement('div')
        imageCard.className = 'aspect-square bg-gray-100 rounded-xl overflow-hidden relative group'
        if (isExisting) {
            imageCard.dataset.existing = 'true'
            imageCard.dataset.filename = filename
        }
        imageCard.innerHTML = `
            <img src="${src}" class="w-full h-full object-cover" alt="Business Image">
            <div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-all duration-200 flex items-center justify-center gap-2">
                <button type="button" class="p-2 bg-white rounded-lg hover:bg-gray-100 transition-all duration-200 view-image-btn">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4 text-gray-600">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0Z" />
                    </svg>
                </button>
                <button type="button" class="p-2 bg-white rounded-lg hover:bg-gray-100 transition-all duration-200 delete-image-btn">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4 text-red-500">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                    </svg>
                </button>
            </div>
        `
        imagesGrid.insertBefore(imageCard, imageUploadDiv.nextSibling)

        imageCard.addEventListener('click', function (e) {
            e.stopPropagation()
        })

        const viewBtn = imageCard.querySelector('.view-image-btn')
        viewBtn.addEventListener('click', function (e) {
            e.stopPropagation()
            window.open(src, '_blank')
        })

        const deleteBtn = imageCard.querySelector('.delete-image-btn')
        deleteBtn.addEventListener('click', function (e) {
            e.stopPropagation()
            const imgFilename = imageCard.dataset.filename
            if (imgFilename) {
                existingImages = existingImages.filter(img => img !== imgFilename)
                document.getElementById('existing-business-images').value = JSON.stringify(existingImages)
            }
            imageCard.remove()
        })
    }

    const cardViewBtn = document.getElementById('card-view-btn')
    const tableViewBtn = document.getElementById('table-view-btn')
    const cardViewContainer = document.getElementById('card-view-container')
    const tableViewContainer = document.getElementById('table-view-container')

    if (cardViewBtn && tableViewBtn) {
        cardViewBtn.addEventListener('click', () => {
            cardViewContainer.classList.remove('hidden')
            tableViewContainer.classList.add('hidden')
            cardViewBtn.classList.add('bg-white', 'text-gray-800', 'shadow-sm')
            cardViewBtn.classList.remove('text-gray-600')
            tableViewBtn.classList.remove('bg-white', 'text-gray-800', 'shadow-sm')
            tableViewBtn.classList.add('text-gray-600')
        })

        tableViewBtn.addEventListener('click', () => {
            tableViewContainer.classList.remove('hidden')
            cardViewContainer.classList.add('hidden')
            tableViewBtn.classList.add('bg-white', 'text-gray-800', 'shadow-sm')
            tableViewBtn.classList.remove('text-gray-600')
            cardViewBtn.classList.remove('bg-white', 'text-gray-800', 'shadow-sm')
            cardViewBtn.classList.add('text-gray-600')
        })
    }
})

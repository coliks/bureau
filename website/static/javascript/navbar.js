document.addEventListener('DOMContentLoaded', () => {
  const profileMenuBtn = document.getElementById('profile-menu-btn')
  const profileMenu = document.getElementById('profile-menu')

  profileMenuBtn.addEventListener('click', () => {
    if (profileMenu.classList.contains('opacity-0')) {
      profileMenu.classList.remove('w-0', 'opacity-0', 'p-0')
      profileMenu.classList.add('w-48', 'opacity-100', 'p-2')
    } else {
      profileMenu.classList.remove('w-48', 'opacity-100', 'p-2')
      profileMenu.classList.add('w-0', 'opacity-0', 'p-0')
    }
  })
})
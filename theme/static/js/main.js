// toggle button

const navMenu = document.getElementById('nav-menu')
const navLink = document.querySelectorAll('.nav-link')
const hamburger = document.getElementById('hamburger')

hamburger.addEventListener('click', ()=> {
    console.log('clicked')
    navMenu.classList.toggle('left-0')
    navMenu.classList.toggle('left-[-100%]')
    hamburger.classList.toggle('ri-close-large-fill')
})

navLink.forEach( link => {
    link.addEventListener('click', () => {
        navMenu.classList.toggle('left-0')
        navMenu.classList.toggle('left-[-100%]')
        hamburger.classList.toggle('ri-close-large-fill')
    })
})
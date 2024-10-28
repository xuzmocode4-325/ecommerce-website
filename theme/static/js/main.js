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


// Swiper

const swiper = new Swiper('.swiper', {
    // Optional parameters
    speed: 200,
    spaceBetween: 45,
    autoplay: {
        delay: 12000, 
        disableOnInteraction: false,
    },
  
    // If we need pagination
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },

    grabCursor: true,
    breakpoints: {
        640: {
            slidesPerView: 1
        },
        768: {
            slidesPerView: 2
        }, 
        1280: {
            slidesPerView: 4
        },
    }
  
  });
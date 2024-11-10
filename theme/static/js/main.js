/* toggle button */
const navMenu = document.getElementById('nav-menu')
const navLink = document.querySelectorAll('.nav-link')
const hamburger = document.getElementById('hamburger')
const categoryBtn = document.getElementById('category-btn')
const categoryList = document.getElementById('category-list')

hamburger.addEventListener('click', ()=> {
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

categoryBtn.addEventListener('click', () => {
   categoryList.classList.toggle('hidden')
   //console.log('category-btn clicked')
})


/* Swiper */
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

  /*  Scroll Up */
  const scrollUp = () => {
    const scrollUpBtn = document.getElementById('scroll-up')

    if (this.scrollY >= 250) {
        scrollUpBtn.classList.remove('-bottom-1/2')
        scrollUpBtn.classList.add('bottom-4')
    } else {
        scrollUpBtn.classList.add('-bottom-1/2')
        scrollUpBtn.classList.remove('bottom-4')
    }

  }

  window.addEventListener('scroll', scrollUp)

  /* Srroll Header  */

  const scrollHeader = () => {
    const header = document.getElementById('navbar')

    if (this.scrollY >= 50) {
        header.classList.add('border-b', 'border-yellow-500')
    } else {
        header.classList.remove('border-b', 'border-yellow-500')
    }

  }

  window.addEventListener('scroll', scrollHeader)

  /* Active Link */
  const activeLink = function() {
    const sections  = document.querySelectorAll('section')
    const navLinks = document.querySelectorAll('.nav-link')

    let current = 'home'

    sections.forEach(section => {
        const sectionTop = section.offsetTop;

        if (this.scrollY >= sectionTop - 60) {
            current = section.getAttribute('id')
            console.log(current)
        }
    })

    navLinks.forEach(item => {
        item.classList.remove("active")

        if (item.href.includes(current)) {
            item.classList.add('active')
        }
    })
  }

  window.addEventListener('scroll', activeLink)


  /* scroll reveal */

  const sr = ScrollReveal({
    origin: 'top',
    distance: '60px',
    duration: 2500,
    delay: 300,
    reset: true
  })

  sr.reveal(`.home-data, .about-top, .trending-top, .review-top, .review-swiper, 
    .footer-icon, .footer-content`)
  sr.reveal(`.home-image`, {delay: 500, scale: 0.5 })
  sr.reveal(`.service-card, .popular-card`, { interval:100 })

  sr.reveal(`.about-img_2, .about-content-1`, { origin: 'right' })
  sr.reveal(`.about-img_1, .about-content-2`, { origin: 'left' })

  sr.reveal('.copyright-text', {delay: 500, origin:'bottom'})
  sr.reveal('.footer-floral', {delay: 1000, origin:'left'})
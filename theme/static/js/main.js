/* toggle button */
const navMenu = document.getElementById('nav-menu')
const navLink = document.querySelectorAll('.nav-link')
const header = document.getElementById('navbar')
const hamburger = document.getElementById('hamburger')
const categoryBtn = document.getElementById('category-btn')
const categoryList = document.getElementById('category-list')
const sortBtn = document.getElementById('sort-button')
const sortList = document.getElementById('sort-list')
const dashBurger = document.getElementById('dash-burger')
const mobileMenu = document.getElementById('mobile-menu')
const dropdown = document.getElementById('dropdown-control')
const profileBtn = document.getElementById('profile-button')
const messages = document.querySelectorAll('.message')


messages.forEach((message) => setTimeout(function() {
   if (message) {
        message.classList.add('hidden')
   }
}, 4500))


if (dashBurger) {
    dashBurger.addEventListener('click', () => {
        console.log('dash burger!')
        if (dashBurger.classList.contains('closed')) {
            dashBurger.classList.remove('closed')
            dashBurger.classList.add('open')
            mobileMenu.classList.remove('hidden')
        } else if (dashBurger.classList.contains('open')) {
            dashBurger.classList.remove('open')
            dashBurger.classList.add('closed')
            mobileMenu.classList.add('hidden')
        }
    })
}

if (profileBtn) {
    profileBtn.addEventListener('click', () => {
        dropdown.classList.toggle('hidden')
    })
}


// navLink.forEach( link => {
//     link.addEventListener('click', () => {
//         navMenu.classList.toggle('left-0')
//         navMenu.classList.toggle('left-[-100%]')
//         hamburger.classList.toggle('ri-close-large-fill')
//     })
// })

if (categoryBtn) {
    categoryBtn.addEventListener('click', () => {
        categoryList.classList.toggle('hidden')
        //console.log('category-btn clicked')
    })
}

if (sortBtn) {
    sortBtn.addEventListener('click', () => {
        console.log(sortList)
        sortList.classList.toggle('hidden')
    })
}

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
    if (scrollUpBtn) {
        if (this.scrollY >= 250) {
            scrollUpBtn.classList.remove('-bottom-1/2')
            scrollUpBtn.classList.add('bottom-4')
    
        } else {
            scrollUpBtn.classList.add('-bottom-1/2')
            scrollUpBtn.classList.remove('bottom-4')
        }
    
    }
}

window.addEventListener('scroll', scrollUp)

/* Srroll Header  */

const scrollHeader = () => {
    if (this.scrollY >= 50) {
        header.classList.add('border-b', 'border-yellow-500')
    } else {
        header.classList.remove('border-b', 'border-yellow-500')
    }
}

window.addEventListener('scroll', scrollHeader)

/* Scroll Dropdown */ 

const hideListsOnScroll = () => {
    if (dropdown) {
        if (!dropdown.classList.contains('hidden')) {
            dropdown.classList.add('hidden');
        }
    }

    if (sortList) {
        if (!sortList.classList.contains('hidden')) {
            sortList.classList.add('hidden')
        }
    }

    if (messages) {
        messages.forEach(message => {
            if (!message.classList.contains('hidden')) {
                message.classList.add('hidden')
            }
        })
        
    }
};

window.addEventListener('scroll', hideListsOnScroll);

/* Scroll Reveal */

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
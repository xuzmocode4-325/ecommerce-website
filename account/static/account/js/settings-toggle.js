const toggleBtn = document.querySelectorAll(".settings-toggle")

toggleBtn.forEach((btn) => {
    btn.addEventListener('click', () => {
        console.log('clicked')
        btn.parentNode.classList.toggle('activated')
    })
})
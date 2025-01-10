const disableButton = () => {
    const submitBtn = document.getElementById('submit-button');
    const loadingSpinner = document.getElementById('loading-spinner');
    const buttonText = document.getElementById('button-text')

    console.log(loadingSpinner);
    
    buttonText.innerText=''
    loadingSpinner.classList.toggle("hidden");
 

    submitBtn.disabled = true;
};
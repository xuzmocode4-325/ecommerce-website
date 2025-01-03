const addButton = document.getElementById('add-button')
const scriptTag = document.querySelector('script[src*="add-button.js"]');
const cartAddUrl = scriptTag.dataset.cartAddUrl;
const csrfToken = scriptTag.dataset.csrfToken;

console.log(scriptTag.dataset)


const addToCart = async (event) => {
    event.preventDefault();

    const productId = addButton.value;
    const productQuantity = document.querySelector('#select option:checked').textContent;

    try {
        const response = await fetch(cartAddUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                product_id: productId,
                product_quantity: productQuantity,
                action: 'post'
            })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const json = await response.json();
        console.log(json); 

    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
};

// Call the function to add to cart
addButton.addEventListener('click', addToCart)


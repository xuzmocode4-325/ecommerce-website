/**
 * Retrieves the 'add-button' element from the DOM.
 * @type {HTMLElement}
 */
const addButton = document.getElementById('add-button');

/**
 * Retrieves the script tag that includes 'add-button.js' in its source attribute.
 * @type {HTMLScriptElement}
 */
const scriptTag = document.querySelector('script[src*="add-button.js"]');

/**
 * Extracts the cart add URL from the script tag's data attributes.
 * @type {string}
 */
const cartAddUrl = scriptTag.dataset.cartAddUrl;

/**
 * Extracts the CSRF token from the script tag's data attributes.
 * @type {string}
 */
const csrfToken = scriptTag.dataset.csrfToken;

/**
 * Asynchronous function to handle adding a product to the cart.
 * @param {Event} event - The event object from the click event.
 */
const addToCart = async (event) => {
    event.preventDefault();

    /**
     * Retrieves the product ID from the add button's value.
     * @type {string}
     */
    const productId = addButton.value;

    /**
     * Retrieves the selected product quantity from the dropdown.
     * @type {string}
     */
    const productQuantity = document.querySelector('#select option:checked').textContent;

    try {
        /**
         * Sends a POST request to add the product to the cart.
         * @type {Response}
         */
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
        } else {
            /**
             * Parses the JSON response from the server.
             * @type {Object}
             */
            const json = await response.json();
            //console.log(json); 
    
            document.getElementById("cart-qty-mobile").innerText = `(${json.cart_qty})`;
            document.getElementById("cart-qty-web").innerText = json.cart_qty;
        }
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
};

// Adds an event listener to the add button to trigger the addToCart function on click.
addButton.addEventListener('click', addToCart);
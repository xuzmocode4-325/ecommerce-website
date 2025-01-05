/**
 * Retrieves the 'cart-add-button' element from the DOM.
 * @type {HTMLElement}
 */
const cartAddButton = document.getElementById('cart-add-button');

/**
 * Retrieves the 'item-qty-plus' element from the DOM.
 * @type {HTMLElement}
 */
const itemQtyPlus = document.getElementById('item-qty-plus');
console.log(itemQtyPlus)

/**
 * Retrieves the 'item-qty-minus' element from the DOM.
 * @type {HTMLElement}
 */
const itemQtyMinus = document.getElementById('item-qty-minus');
console.log(itemQtyMinus)

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
    const productId = cartAddButton.value;

    /**
     * Retrieves the selected product quantity from the quantity div.
     * @type {string}
     */
    const productQuantity = document.querySelector('#item-quantity').textContent;

  
    if (productQuantity && productQuantity >= 1 && productQuantity <= 10) {

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
                    product_qty: productQuantity,
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
                //document.getElementById("item-quantity").innerText = json.product_qty
            }
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    }

    else {

        console.log("Add a product to the cart, you knitwitt!")
    }

   
};

// Adds an event listener to the add button to trigger the addToCart function on click.
cartAddButton.addEventListener('click', addToCart);

const handleItemQuantity = function(arg) {
    /**
     * Retrieves the selected product quantity from the quantity div.
     * @type {string}
     */
    const productQuantity = document.querySelector('#item-quantity')
    const currentValue = productQuantity.textContent;

    console.log(`Current Quantity: ${currentValue}, Change: ${arg}`);

    let newValue = Number(currentValue) + arg

    if (newValue < 0 ) {
        newValue = 0
        console.log("You can't place an negative order, you knitwitt!")
    } 

    if (newValue > 10) {
        newValue = 10
        console.log("Leave some product for other buyers, you knitwitt!")
    }

    productQuantity.innerText = newValue
}



itemQtyPlus.addEventListener('click', () => {
    handleItemQuantity(1); // Calls with '+1' for plus button
});

itemQtyMinus.addEventListener('click', () => {
    handleItemQuantity(-1); // Calls with '-1' for minus button
});

/**
 * Retrieves the 'checkout-form' element from the DOM.
 * @type {HTMLElement}
 */
const orderForm = document.getElementById('checkout-form');

/**
 * Retrieves the script tag that includes 'handle-payment.js' in its source attribute.
 * @type {HTMLScriptElement}
 */
const scriptTag = document.querySelector('script[src*="handle-payment.js"]');

/**
 * Extracts the cart add URL from the script tag's data attributes.
 * @type {string}
 */
const cartSubmitUrl = scriptTag.dataset.cartSubmitUrl;

/**
 * Extracts the CSRF token from the script tag's data attributes.
 * @type {string}
 */
const csrfToken = scriptTag.dataset.csrfToken;

/**
 * Asynchronous function to handle adding a product to the cart.
 * @param {Event} event - The event object from the click event.
 */
const completeOrder = async (event) => {
    event.preventDefault();

   
};

// Adds an event listener to the add button to trigger the addToCart function on click.
orderForm.addEventListener('submit', completeOrder);

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

    const firstname = document.getElementById('firstname').value;
    const surname = document.getElementById('surname').value;
    const email = document.getElementById('email').value;
    const address1 = document.getElementById('address1').value;
    const address2 = document.getElementById('address2').value;
    const city = document.getElementById('city').value;
    const state = document.getElementById('state').value;
    const country = document.getElementById('country').value; 
    const zipcode = document.getElementById('zipcode').value; 

    console.log('Firstname:', firstname);
    console.log('Surname:', surname);
    console.log('Email:', email);
    console.log('Address1:', address1);
    console.log('Address2:', address2);
    console.log('City:', city);
    console.log('State:', state);
    console.log('Country:', country);
    console.log('Zipcode:', zipcode);

    try {
        /**
         * Sends a POST request to add the product to the cart.
         * @type {Response}
         */
        const response = await fetch(cartSubmitUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                fn: firstname, 
                sn: surname, 
                em: email, 
                ad1: address1, 
                ad2: address2, 
                ct: city, 
                st: state, 
                cntry: country, 
                zip: zipcode
            })
        });

        if (!response.ok) {
            console.log(response)
            window.location.replace('payment-failed')
            throw new Error('Network response was not ok');
            
        } else {
            /**
             * Parses the JSON response from the server.
             * @type {Object}
             */
            const json = await response.json();
            //console.log(json); 
    
            window.location.replace('payment-success')
        }
    } catch (error) {
        //window.location.replace("{% url 'payment-failed' %}")
        console.error('There was a problem with the fetch operation:', error);
    }
};

// Adds an event listener to the add button to trigger the addToCart function on click.
orderForm.addEventListener('submit', completeOrder);

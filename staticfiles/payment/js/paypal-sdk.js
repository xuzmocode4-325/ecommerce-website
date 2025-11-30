const scriptTag = document.querySelector('script[src*="paypal-sdk.js"]');
const cartTotal = scriptTag.dataset.cartTotal;
const cartSubmitUrl = scriptTag.dataset.cartSubmitUrl;
const csrfToken = scriptTag.dataset.csrfToken;

const paypalButtonsComponent = paypal.Buttons({
    // optional styling for buttons
    // https://developer.paypal.com/docs/checkout/standard/customize/buttons-style-guide/
    style: {
        color: "white",
        shape: "pill",
        layout: "vertical",
        label: "checkout"
    },

    message: {
        color: 'white',
        position: 'top',
    },


    onInit: function(data, actions) {
        actions.disable();
        document.querySelectorAll('.validate').forEach(item => {
            item.addEventListener('keyup', event => {
                var order_valid = true
                
                function checkInputs(event) {
                    let order_valid = true;
                    const inputs = document.querySelectorAll('input[required]');

                    inputs.forEach(function(input) {
                        if (input.value === '') {
                            order_valid = false;
                        }
                    });

                    return order_valid;
                }

                var isOrderVerified = checkInputs();

                if (isOrderVerified) {
                    actions.enable();
                } else {
                    actions.disable();
                }
            });
        });

        var order_valid = true
                
        function checkInputs(event) {
            let order_valid = true;
            const inputs = document.querySelectorAll('input[required]');

            inputs.forEach(function(input) {
                if (input.value === '') {
                    order_valid = false;
                }
            });

            return order_valid;
        }

        var isOrderVerified = checkInputs();

        if (isOrderVerified) {
            actions.enable();
        } else {
            actions.disable();
        }
    }, 

    // set up the transaction
    createOrder: (data, actions) => {
        // pass in any options from the v2 orders create call:
        // https://developer.paypal.com/api/orders/v2/#orders-create-request-body
        const createOrderPayload = {
            purchase_units: [
                {
                    amount: {
                        value: cartTotal
                    }
                }
            ]
        };

        return actions.order.create(createOrderPayload);
    },

    // finalize the transaction
    onApprove: (data, actions) => {
        const captureOrderHandler = async (details) => {
            const payerName = details.payer.name.given_name;
            console.log('Transaction completed');

            const firstname = document.getElementById('firstname').value;
            const surname = document.getElementById('surname').value;
            const email = document.getElementById('email').value;
            const address1 = document.getElementById('address1').value;
            const address2 = document.getElementById('address2').value;
            const city = document.getElementById('city').value;
            const state = document.getElementById('state').value;
            const country = document.getElementById('country').value; 
            const zipcode = document.getElementById('zipcode').value; 
        
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
                window.location.replace('payment-failed')
            }
        };

        return actions.order.capture().then(captureOrderHandler);
    },

    // handle unrecoverable errors
    onError: (err) => {
        console.error('An error prevented the buyer from checking out with PayPal');
    }

   
});

paypalButtonsComponent
    .render("#paypal-button-container")
    .catch((err) => {
        console.error('PayPal Buttons failed to render');
});

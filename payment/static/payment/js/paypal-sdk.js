
const paypalButtonsComponent = paypal.Buttons({
    // optional styling for buttons
    // https://developer.paypal.com/docs/checkout/standard/customize/buttons-style-guide/
    style: {
        color: "white",
        shape: "pill",
        layout: "vertical",
        label: "checkout"
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
    }

   
});

paypalButtonsComponent
    .render("#paypal-button-container")
    .catch((err) => {
        console.error('PayPal Buttons failed to render');
});

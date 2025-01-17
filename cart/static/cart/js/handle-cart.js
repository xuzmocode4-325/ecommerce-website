const cartPlusButtons = document.querySelectorAll('.cart-qty-plus')
const cartMinusButtons = document.querySelectorAll('.cart-qty-minus')
const deleteButtons = document.querySelectorAll('.delete-button');
const scriptTag = document.querySelector('script[src*="handle-cart.js"]');
const cartDeleteUrl = scriptTag.dataset.cartDeleteUrl;
const cartUpdateUrl = scriptTag.dataset.cartUpdateUrl;
const cartCouponUrl = scriptTag.dataset.cartCouponUrl;
const csrfToken = scriptTag.dataset.csrfToken;
const promoButton =  document.getElementById('promo-button')
const voucherInput = document.getElementById('voucher');
const promoNotes =  document.getElementById('coupon-notes')


console.log(promoButton)

const deleteFromCart = async function(event) {
    event.preventDefault();
    const productId = this.dataset.index;

    try {
        const response = await fetch(cartDeleteUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                product_id: productId,
                action: 'post'
            })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        } else {
            const json = await response.json();
            console.log(json); 

            location.reload(true);
    
            document.getElementById("cart-qty-mobile").innerText = `(${json.cart_qty})`;
            document.getElementById("cart-qty-web").innerText = json.cart_qty;
            document.getElementById("total").innerText = `$${json.product_qty}`;
        }

    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
};


const updateCart = async function(event, value) {
    event.preventDefault(); // Prevent default action of the event

    //const productId = this.dataset.index;
    const productId = event.currentTarget.dataset.index; 
    const productQuantity = document.getElementById(`item-qty-${productId}`);

    const currentValue = productQuantity.textContent;

    //console.log(`Current Quantity: ${currentValue}, Change: ${arg}`);

    let newValue = Number(currentValue) + value

    if (newValue < 0 ) {
        newValue = 0
        console.log("You can't place an negative order, you knitwitt!")
    } 

    if (newValue > 10) {
        newValue = 10
        console.log("Leave some product for other buyers, you knitwitt!")
    }

    if (newValue && newValue >= 1 && newValue <= 10 ) {
        console.log('Yahtzee!', newValue)

        try {
            const response = await fetch(cartUpdateUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    product_id: productId,
                    product_qty: newValue,
                    action: 'post'
                })
            });
    
            if (!response.ok) {
                throw new Error('Network response was not ok');
            } else {
                const json = await response.json();
                console.log(json); 
    
                location.reload();
        
                document.getElementById("cart-qty-mobile").innerText = `(${json.cart_qty})`;
                document.getElementById("cart-qty-web").innerText = json.cart_qty;
                document.getElementById("total").innerText = `$${json.product_qty}`;
            }
    
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }

    } else {
        console.log('Non!')
    }
};
// Attach event listeners to delete buttons

const applyCoupon = async function(event) {
   
   
    const couponCode = voucherInput.value.trim();

    if (couponCode) {
        try {
            const response = await fetch(cartCouponUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken  // Ensure CSRF token is included
                },
                body: JSON.stringify({ coupon_code: couponCode })
            });

            const data = await response.json();

            if (data.success) {
                // Update the cart total on the page
                document.getElementById('cart-total').innerText = `Total: $${data.new_total}`;
                //alert('Coupon applied successfully!');
            } else {
                promoNotes.innerText = 'Invalid coupon code.'
                //alert('Invalid coupon code.');
            }
        } catch (error) {
            console.error('Error:', error);
            //alert('An error occurred while applying the coupon.');
        }
    } else {
        //alert('Please enter a coupon code.');
        promoNotes.innerText = 'Please enter a coupon code.'
    }
}

voucherInput.addEventListener('input', () => promoNotes.innerHTML = '&nbsp;')

deleteButtons.forEach(button => button.addEventListener('click', deleteFromCart));

promoButton.addEventListener('click', applyCoupon)

cartPlusButtons.forEach(button => 
    button.addEventListener('click', (event) => updateCart(event, 1))
);

cartMinusButtons.forEach(button => 
    button.addEventListener('click', (event) => updateCart(event, -1))
);
const cartPlusButtons = document.querySelectorAll('.cart-qty-plus');
const cartMinusButtons = document.querySelectorAll('.cart-qty-minus');
const deleteButtons = document.querySelectorAll('.delete-button');
const scriptTag = document.querySelector('script[src*="handle-cart.js"]');

const cartDeleteUrl = scriptTag.dataset.cartDeleteUrl;
const cartUpdateUrl = scriptTag.dataset.cartUpdateUrl;
const cartCouponUrl = scriptTag.dataset.cartCouponUrl;
const csrfToken = scriptTag.dataset.csrfToken;

const promoButton = document.querySelectorAll('#promo-button');
const promoNotes = document.querySelectorAll('.notes');

const voucherInput = document.getElementById('voucher');

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
    event.preventDefault();
    const productId = event.currentTarget.dataset.index;
    const productQuantity = document.getElementById(`item-qty-${productId}`);
    const currentValue = productQuantity.textContent;
    let newValue = Number(currentValue) + value;

    if (newValue < 1) {
        newValue = 1;
        console.log("You can't place a negative order!");
    } else if (newValue > 10) {
        newValue = 10;
        console.log("Leave some product for other buyers!");
    }

    if (newValue >= 1 && newValue <= 10) {
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
                location.reload();
                document.getElementById("cart-qty-mobile").innerText = `(${json.cart_qty})`;
                document.getElementById("cart-qty-web").innerText = json.cart_qty;
                document.getElementById("total").innerText = `$${json.product_qty}`;
            }

        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    }
};

const applyCoupon = async function(event) {
    event.preventDefault();
    const couponCode = voucherInput.value.trim()

    console.log(couponCode)

    if (couponCode) {
        try {
            const response = await fetch(cartCouponUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ coupon_code: couponCode })
            });

            const data = await response.json();

            if (data.success) {
                promoNotes.forEach(note => note.innerText = `${couponCode} coupon code applied.`);
            } else {
                promoNotes.forEach(note => note.innerText = 'Invalid coupon code.');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    } else {
        promoNotes.forEach(note => note.innerText = 'Please enter a coupon code.');
    }
};

voucherInput.addEventListener('input', () => promoNotes.forEach(note => note.innerHTML = '&nbsp;'));

deleteButtons.forEach(button => button.addEventListener('click', deleteFromCart));
promoButton.forEach(button => button.addEventListener('click', applyCoupon));
cartPlusButtons.forEach(button => button.addEventListener('click', (event) => updateCart(event, 1)));
cartMinusButtons.forEach(button => button.addEventListener('click', (event) => updateCart(event, -1)));
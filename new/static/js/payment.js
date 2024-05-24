// payment.js

function validateCardNumber() {
    var cardNumber = document.getElementById('cardnumber').value;

    if (cardNumber.length != 16) {
        alert('Card number must be 16 digits.');
        return false;
    }

    return true;
}

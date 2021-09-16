data = document.getElementsByClassName('mycart')
for (i = 0; i < data.length; i++) {
    data[i].addEventListener('click', function() {
        product = this.dataset.product_id;
        Action = this.dataset.action;
        cartmanagment(product, Action)

    })
}

function cartmanagment(product_id, action) {
    if (user == "AnonymousUser") {
        var url = '/guestcart/'
    } else {
        var url = '/updatecart/'
    }

    fetch(url, {
            method: 'POST',
            headers: {
                'content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'productid': product_id, 'action': Action })
        })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            console.log(data)
            location.reload()
        })
}
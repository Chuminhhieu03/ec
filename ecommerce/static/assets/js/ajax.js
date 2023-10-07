$.ajax({
    type: "GET",
    url: "/addToCart/",
    data: {
        'product_id': 'your_product_id',
        'quantity': 'your_quantity'
    },
    success: function(response) {
        alert(response.message);
    }
});

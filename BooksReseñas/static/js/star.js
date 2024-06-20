document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.rating-stars .fa-star');

    stars.forEach(function(star) {
        star.addEventListener('click', function() {
            const rating = parseInt(this.getAttribute('data-index'));
            document.querySelector('#id_rating').value = rating;
            stars.forEach(function(s, index) {
                if (index < rating) {
                    s.classList.add('selected');
                } else {
                    s.classList.remove('selected');
                }
            });
        });
    });

    // Al cargar la página, seleccionar las estrellas correspondientes al rating actual
    const currentRating = parseInt(document.querySelector('.rating-stars').getAttribute('data-rating'));
    stars.forEach(function(s, index) {
        if (index < currentRating) {
            s.classList.add('selected');
        }
    });
});
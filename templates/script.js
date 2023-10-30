$(document).ready(function() {
    // Function to get cupcakes from the API and add them to the page, ordered by rating
    function getCupcakes() {
        axios.get('/api/cupcakes')
            .then(function(response) {
                var cupcakes = response.data.cupcakes;

                // Sort cupcakes by rating in descending order
                cupcakes.sort(function(a, b) {
                    return b.rating - a.rating;
                });

                cupcakes.forEach(function(cupcake) {
                    $('#cupcake-list').append('<li style="background-color:' + getRandomColor() + ';">' + cupcake.flavor + ' - Rating: ' + cupcake.rating + '</li>');
                });
            })
            .catch(function(error) {
                console.log('Error:', error);
            });
    }

    // Call the function to get cupcakes and add them to the page
    getCupcakes();

    // Event listener for form submission
    $('#cupcake-form').submit(function(event) {
        event.preventDefault();

        // Get form data
        var flavor = $('#flavor').val();
        var size = $('#size').val();
        var rating = $('#rating').val();
        var image = $('#image').val(); // Assuming you have an input field with id 'image' for cupcake image URL

        // Create new cupcake object
        var newCupcake = {
            flavor: flavor,
            size: size,
            rating: parseFloat(rating), // Convert rating to float
            image: image
        };

        // Send POST request to API to add new cupcake
        axios.post('/api/cupcakes', newCupcake)
            .then(function(response) {
                // Add new cupcake to the page with a random background color
                $('#cupcake-list').prepend('<li style="background-color:' + getRandomColor() + ';">' + response.data.cupcake.flavor + ' - Rating: ' + response.data.cupcake.rating + '</li>');

                // Clear form fields
                $('#flavor').val('');
                $('#size').val('');
                $('#rating').val('');
                $('#image').val('');
            })
            .catch(function(error) {
                console.log('Error:', error);
            });
    });

    // Function to generate random color from the specified palette
    function getRandomColor() {
        var colors = ['#ecfa82', '#8ddfcb', '#82a0d8', '#edb7ed'];
        return colors[Math.floor(Math.random() * colors.length)];
    }
});

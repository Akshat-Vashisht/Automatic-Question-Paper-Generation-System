window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});

// Get all the links in the sidebar
var sidebarLinks = document.querySelectorAll('.list-group-item');

// Add a click event listener to each link
sidebarLinks.forEach(function (link) {
    link.addEventListener('click', function (event) {
        event.preventDefault(); // prevent the link from redirecting to a new page
        var href = this.getAttribute('href'); // get the href attribute of the clicked link
        loadDashboardScreen(href); // load the corresponding dashboard screen
    });
});

// Function to load the corresponding dashboard screen based on the clicked link
function loadDashboardScreen(href) {
    // Use jQuery to load the HTML content of the dashboard screen
    $('#page-content-wrapper').load(href);
}

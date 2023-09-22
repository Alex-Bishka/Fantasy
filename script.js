// Check if the page is served from GitHub Pages
let base = document.createElement('base');
if (window.location.hostname.includes('github.io')) {
    base.setAttribute('href', '/Fantasy/');
} else {
    base.setAttribute('href', '/');
}
document.head.appendChild(base);


// removing existing event handlers on the menuBtn
$(document).off('click', '#menuBtn').on('click', '#menuBtn', function () {
});

// removing existing event handlers on the closeBtn
$(document).off('click', '#closeBtn').on('click', '#closeBtn', function () {
});

// Open the menu - attaches even if the buttons aren't loaded into the dom yet
$(document).on('click', '#menuBtn', function () {
    document.getElementById('sideMenu').style.width = '250px';
    document.getElementById('sideMenu').style.zIndex = '25';
    document.getElementById('menuBtn').style.cursor = "auto"
});

// Close the menu - attaches even if the buttons aren't loaded into the dom yet
$(document).on('click', '#closeBtn', function () {
    document.getElementById('sideMenu').style.width = '0';
    document.getElementById('menuBtn').style.cursor = "pointer"
});

// rediction function for specifc blog
function redirectToBlog(blogName) {
    // Redirect to the specific blog page
    window.location.href = "/Blogs/" + blogName;
}

// Intercept anchor tag clicks to handle /Blogs specially
document.addEventListener('click', function (event) {
    if (event.target.tagName === 'A') {
        const href = event.target.getAttribute('href');
        if (href === '/Blogs') {
            event.preventDefault(); // Prevent the default action
            redirectToBlogs(); // Call your custom function
        }
    }
});

// Custom function to handle /Blogs
function redirectToBlogs() {
    // Your custom logic here, for example:
    window.location.href = "/Blogs.html"; // Navigate to blog.html
}

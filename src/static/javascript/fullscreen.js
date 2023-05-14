// Open fullscreen
function openFullscreen(imageUrl) {
    var fullScreenImage = document.createElement('div');
    fullScreenImage.classList.add('full-screen');
    fullScreenImage.innerHTML = '<img src="' + imageUrl + '"><span class="close-btn">X</span>';
    document.body.appendChild(fullScreenImage);
    document.body.style.overflow = 'hidden';
}

// Close fullscreen
function closeFullscreen() {
    var fullScreenImage = document.querySelector('.full-screen');
    fullScreenImage.parentNode.removeChild(fullScreenImage);
    document.body.style.overflow = 'auto';
}

// Click on image
var images = document.querySelectorAll('.image');
for (var i = 0; i < images.length; i++) {
    images[i].addEventListener('click', function () {
        var imageUrl = this.getAttribute('src');
        openFullscreen(imageUrl);
    });
}

// Click in X
document.addEventListener('click', function (e) {
    if (e.target.classList.contains('close-btn')) {
        closeFullscreen();
    }
});

// Click Esc
document.addEventListener('keyup', function (e) {
    if (e.key === "Escape" && document.querySelector('.full-screen')) {
        closeFullscreen();
    }
});



// Variable Declarations
const $grid = $('.grid');
const $lightbox = $('.lightbox');
const $lightboxImage = $('.lightbox-image');

// Masonry Layout Initialization
function initMasonry() {
  $grid.masonry({
    itemSelector: '.grid-item',
    columnWidth: '.grid-sizer',
    percentPosition: true
  });
}

// Fetch and Render Images
function fetchImages() {
  fetch('/api/images')
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to fetch images');
      }
      return response.json();
    })
    .then(data => {
      data.forEach(image => {
        const $gridItem = $('<div class="grid-item"></div>');
        const $image = $(`<img src="${image.url}" alt="${image.alt}">`);
        $gridItem.append($image);
        $grid.append($gridItem).masonry('appended', $gridItem);
      });
      $grid.imagesLoaded().progress(function() {
        $grid.masonry();
      });
    })
    .catch(error => {
      console.error(error);
    });
}

// Handle Heart Likes
function handleHeartLikes() {
  $grid.on('click', '.heart-icon', function() {
    const $icon = $(this);
    const imageId = $icon.data('imageId');
    fetch(`/api/images/${imageId}/like`, { method: 'POST' })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to update like count');
        }
        return response.json();
      })
      .then(data => {
        $icon.text(data.likes);
      })
      .catch(error => {
        console.error(error);
      });
  });
}

// Handle Maneki Neko Interaction
function handleManekiNeko() {
  $grid.on('click', '.maneki-neko-icon', function() {
    const $icon = $(this);
    const imageId = $icon.data('imageId');
    fetch(`/api/images/${imageId}/interaction`, { method: 'POST' })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to record interaction');
        }
        console.log('Interaction recorded');
      })
      .catch(error => {
        console.error(error);
      });
  });
}

// Initialize JavaScript Lightbox
function initLightbox() {
  const lightbox = new SimpleLightbox($lightboxImage);

  lightbox.on('show.simplelightbox', function() {
    const currentImageIndex = lightbox.currentIndex + 1;
    const totalImages = lightbox.elements.length;

    console.log(`Showing image ${currentImageIndex} of ${totalImages}`);
  });
}

// Event Listener for Keyboard Navigation in Lightbox
document.addEventListener('keydown', function(event) {
  if (event.key === 'ArrowLeft') {
    SimpleLightbox.getProbe().prev();
  } else if (event.key === 'ArrowRight') {
    SimpleLightbox.getProbe().next();
  } else if (event.key === 'Escape') {
    SimpleLightbox.getProbe().close();
  }
});

// Initialize Functions
$(function() {
  initMasonry();
  fetchImages();
  handleHeartLikes();
  handleManekiNeko();
  initLightbox();
});
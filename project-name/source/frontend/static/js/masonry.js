// Import necessary libraries and initialize variables
import imagesLoaded from 'imagesloaded';
import Masonry from 'masonry-layout';

const grid = document.querySelector('.grid');

// Initialize Masonry
const masonry = new Masonry(grid, {
  itemSelector: '.grid-item',
  columnWidth: '.grid-sizer',
  percentPosition: true,
});

// Add images to Masonry and update layout on image load
function addImagesToMasonry() {
  const imgLoad = imagesLoaded(grid);

  imgLoad.on('done', () => {
    masonry.layout();
  });
}

// Initialize the Masonry grid and lightbox functionality
document.addEventListener('DOMContentLoaded', () => {
  addImagesToMasonry();

  // TODO: Implement lightbox functionality using a library like Fancybox, Magnific Popup, or Photoswipe
});
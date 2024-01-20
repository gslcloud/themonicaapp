class Lightbox {
  constructor() {
    this.lightboxElement = null;
    // ...
  }

  init() {
    this.thumbnails = document.querySelectorAll('.image-thumbnail');
    // ...

    this.thumbnails.forEach((thumbnail) => {
      thumbnail.addEventListener('click', () => {
        this.showLightbox();
      });
    });

    // ...
  }

  showLightbox() {
    // ...
  }

  hideLightbox() {
    // ...
  }

  showNextImage() {
    // ...
  }

  showPreviousImage() {
    // ...
  }

  handleKeyboardNavigation(event) {
    // ...
  }
}

const lightboxInstance = new Lightbox();
lightboxInstance.init();

export default Lightbox;
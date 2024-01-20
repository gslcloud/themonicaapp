class lightbox {
  constructor() {
    this.lightboxContainer = document.querySelector(".lightbox");
    this.lightboxImage = this.lightboxContainer.querySelector(".lightbox-image");
    this.closeButton = this.lightboxContainer.querySelector(".lightbox-close");

    this.thumbnails = Array.from(document.querySelectorAll(".thumbnail"));
    this.currentImageIndex = 0;

    this.initialize();
  }

  initialize() {
    this.addThumbnailEventListeners();
    this.addKeyboardEventListeners();
    this.addCloseButtonEventListener();
  }

  addThumbnailEventListeners() {
    this.thumbnails.forEach((thumbnail, index) => {
      thumbnail.addEventListener("click", () => {
        this.showLightbox(index);
      });
    });
  }

  showLightbox(imageIndex) {
    this.currentImageIndex = imageIndex;
    this.lightboxImage.src = this.thumbnails[imageIndex].src;
    this.lightboxContainer.classList.add("show");
    document.body.classList.add("lightbox-active");
  }

  hideLightbox() {
    this.lightboxContainer.classList.remove("show");
    document.body.classList.remove("lightbox-active");
  }

  addKeyboardEventListeners() {
    document.addEventListener("keydown", (event) => {
      if (event.key === "ArrowLeft") {
        this.showPreviousImage();
      } else if (event.key === "ArrowRight") {
        this.showNextImage();
      } else if (event.key === "Escape") {
        this.hideLightbox();
      }
    });
  }

  showPreviousImage() {
    if (this.currentImageIndex > 0) {
      this.currentImageIndex--;
      this.lightboxImage.src = this.thumbnails[this.currentImageIndex].src;
    }
  }

  showNextImage() {
    if (this.currentImageIndex < this.thumbnails.length - 1) {
      this.currentImageIndex++;
      this.lightboxImage.src = this.thumbnails[this.currentImageIndex].src;
    }
  }

  addCloseButtonEventListener() {
    this.closeButton.addEventListener("click", () => {
      this.hideLightbox();
    });
  }
}

const myLightbox = new lightbox();

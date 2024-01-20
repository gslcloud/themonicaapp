(function() {
    class MasonryLayout {
        constructor() {
            this.container = document.getElementById("masonry-container");
        }

        fetchData() {
            fetch("/api/images")
                .then(response => {
                    if (!response.ok) {
                        throw new Error("Error fetching images data.");
                    }
                    return response.json();
                })
                .then(images => {
                    this.generateBricks(images);
                })
                .catch(error => {
                    console.error(error);
                    this.showError("Error fetching images. Please try again later.");
                });
        }

        generateBricks(images) {
            // Generate masonry bricks using the fetched images data
            images.forEach(image => {
                const brick = document.createElement("div");
                brick.classList.add("brick");
                brick.innerHTML = `<img src="${image.url}" alt="${image.title}">`;
                this.container.appendChild(brick);
            });
        }

        showError(message) {
            const errorContainer = document.createElement("div");
            errorContainer.classList.add("error-message");
            errorContainer.innerText = message;
            this.container.appendChild(errorContainer);
        }
    }

    const masonryLayout = new MasonryLayout();
    masonryLayout.fetchData();
})();
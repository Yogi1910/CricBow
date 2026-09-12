document.addEventListener('DOMContentLoaded', () => {
    // Get all ribbon blocks
    const ribbonBlocks = document.querySelectorAll('.ribbon-block');

    // Retrieve the selected block from local storage
    const selectedBlockIndex = localStorage.getItem('selectedBlockIndex');

    // Add click event listeners to each block
    ribbonBlocks.forEach((block, index) => {
        block.addEventListener('click', () => {
            // Remove 'selected' class from all blocks
            ribbonBlocks.forEach((b) => {
                b.classList.remove('selected');
            });

            // Add 'selected' class to the clicked block
            block.classList.add('selected');

            // Store the selected block's index in local storage
            localStorage.setItem('selectedBlockIndex', index.toString());
        });

        // Set the initial selected state based on local storage
        if (index.toString() === selectedBlockIndex) {
            block.classList.add('selected');
        }
    });
});

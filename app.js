document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.querySelector("input[type='file']");
    if (fileInput) {
        fileInput.addEventListener("change", () => {
            if (fileInput.files.length > 0) {
                console.log(`Selected label file: ${fileInput.files[0].name}`);
            }
        });
    }
});

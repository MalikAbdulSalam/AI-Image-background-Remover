const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const preview = document.getElementById("preview");
const spinner = document.getElementById("spinner");
const form = document.getElementById("uploadForm");

dropZone.onclick = () => fileInput.click();

dropZone.addEventListener("dragover", e => {
    e.preventDefault();
    dropZone.style.background = "#e0f4ff";
});

dropZone.addEventListener("dragleave", () => {
    dropZone.style.background = "white";
});

dropZone.addEventListener("drop", e => {
    e.preventDefault();
    fileInput.files = e.dataTransfer.files;
    showPreview(fileInput.files);
});

fileInput.addEventListener("change", () => {
    showPreview(fileInput.files);
});

function showPreview(files) {
    preview.innerHTML = "";
    [...files].forEach(file => {
        const img = document.createElement("img");
        img.src = URL.createObjectURL(file);
        img.style.width = "180px";
        img.style.borderRadius = "8px";
        preview.appendChild(img);
    });
}

form.onsubmit = () => {
    spinner.style.display = "flex";
};

// ===========================
// STATE
// ===========================

let image = null;
let zoom = 1;
let pan = { x: 0, y: 0 };
let isDragging = false;
let dragStart = { x: 0, y: 0 };


// ===========================
// DOM ELEMENTS
// ===========================

const canvas = document.getElementById('imageCanvas');
const ctx = canvas.getContext('2d');
const imageInput = document.getElementById('imageInput');
const zoomInBtn = document.getElementById('zoomInBtn');
const zoomOutBtn = document.getElementById('zoomOutBtn');
const resetBtn = document.getElementById('resetBtn');
const downloadBtn = document.getElementById('downloadBtn');
const zoomDisplay = document.getElementById('zoomDisplay');
const placeholder = document.getElementById('placeholder');
const footer = document.getElementById('footer');


// ===========================
// DRAWING FUNCTIONS
// ===========================

function drawCanvas() {
    if (!image) return;

    // Clear canvas with dark background
    ctx.fillStyle = '#0a0a0a';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Save context state
    ctx.save();

    // Translate to center, apply zoom and pan
    ctx.translate(canvas.width / 2, canvas.height / 2);
    ctx.scale(zoom, zoom);
    ctx.translate(pan.x / zoom, pan.y / zoom);
    ctx.translate(-image.width / 2, -image.height / 2);

    // Draw image
    ctx.drawImage(image, 0, 0);

    // Restore context state
    ctx.restore();
}


// ===========================
// IMAGE UPLOAD
// ===========================

imageInput.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            const img = new Image();
            img.onload = function() {
                image = img;
                zoom = 1;
                pan = { x: 0, y: 0 };
                placeholder.style.display = 'none';
                footer.style.display = 'block';
                updateButtons();
                drawCanvas();
            };
            img.src = event.target.result;
        };
        reader.readAsDataURL(file);
    }
});


// ===========================
// ZOOM FUNCTIONS
// ===========================

function handleZoom(direction) {
    const zoomStep = 0.2;
    if (direction === 'in') {
        zoom = Math.min(zoom + zoomStep, 5);
    } else {
        zoom = Math.max(zoom - zoomStep, 0.1);
    }
    updateButtons();
    drawCanvas();
}

zoomInBtn.addEventListener('click', () => handleZoom('in'));
zoomOutBtn.addEventListener('click', () => handleZoom('out'));


// ===========================
// RESET FUNCTION
// ===========================

resetBtn.addEventListener('click', function() {
    zoom = 1;
    pan = { x: 0, y: 0 };
    updateButtons();
    drawCanvas();
});


// ===========================
// MOUSE WHEEL ZOOM
// ===========================

canvas.addEventListener('wheel', function(e) {
    e.preventDefault();
    const direction = e.deltaY < 0 ? 'in' : 'out';
    handleZoom(direction);
}, { passive: false });


// ===========================
// PAN WITH MOUSE
// ===========================

canvas.addEventListener('mousedown', function(e) {
    isDragging = true;
    dragStart = { x: e.clientX, y: e.clientY };
});

canvas.addEventListener('mousemove', function(e) {
    if (!isDragging) return;

    const dx = e.clientX - dragStart.x;
    const dy = e.clientY - dragStart.y;

    pan.x += dx;
    pan.y += dy;

    dragStart = { x: e.clientX, y: e.clientY };
    drawCanvas();
});

canvas.addEventListener('mouseup', function() {
    isDragging = false;
});

canvas.addEventListener('mouseleave', function() {
    isDragging = false;
});


// ===========================
// DOWNLOAD FUNCTION
// ===========================

downloadBtn.addEventListener('click', function() {
    const link = document.createElement('a');
    link.href = canvas.toDataURL('image/png');
    link.download = 'canvas-image.png';
    link.click();
});


// ===========================
// UI UPDATE FUNCTIONS
// ===========================

function updateButtons() {
    zoomInBtn.disabled = !image || zoom >= 5;
    zoomOutBtn.disabled = !image || zoom <= 0.1;
    resetBtn.disabled = !image;
    downloadBtn.disabled = !image;
    zoomDisplay.textContent = `Zoom: ${(zoom * 100).toFixed(0)}%`;
}


// ===========================
// INITIALIZATION
// ===========================

updateButtons();

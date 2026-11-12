// Find the canvas on the page and get its 2D drawing tool (the "context")
const canvas = document.getElementById('doodle-canvas');
const ctx = canvas.getContext('2d');

// initial drawing setup, subject to change
ctx.lineWidth = 5;
ctx.lineCap = 'round';
ctx.lineJoin = 'round';
ctx.strokeStyle = 'black';

let isDrawing = false;

function getPos(event) {
    return {
        x: event.offsetX * (canvas.width / canvas.clientWidth),
        y: event.offsetY * (canvas.height / canvas.clientHeight),
    };
}

function startDrawing(event) {
    isDrawing = true;
    const pos = getPos(event);
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
}

function draw(event) {
    if (!isDrawing) return;
    const pos = getPos(event);
    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
}

function stopDrawing() {
    isDrawing = false;
}

canvas.addEventListener('pointerdown', startDrawing);
canvas.addEventListener('pointermove', draw);
canvas.addEventListener('pointerup', stopDrawing);
canvas.addEventListener('pointerleave', stopDrawing);

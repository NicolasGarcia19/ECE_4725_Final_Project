// Find the canvas on the page and get its 2D drawing tool (the "context")
const canvas = document.getElementById('doodle-canvas');
const line = canvas.getContext('2d');

// initial drawing setup, subject to change
line.lineWidth = 4;              // matches the "thin" size button
line.lineCap = 'round';
line.lineJoin = 'round';
line.strokeStyle = '#2a2a2e';    // matches the black color button

let isDrawing = false;

canvas.addEventListener("mousedown", (e) => {
    isDrawing = true;
    line.beginPath();
    line.moveTo(e.offsetX, e.offsetY);
});

canvas.addEventListener("mousemove", (e) => {
    if (!isDrawing)
        return;

    line.lineTo(e.offsetX, e.offsetY);
    line.stroke();
});

canvas.addEventListener("mouseup", (e) => {
    isDrawing = false;
});

// tool buttons
const clearBtn = document.getElementById('clear-btn');
const eraserBtn = document.getElementById('eraser-btn');
let isErasing = false;
let penColor = '#2a2a2e';
let penSize = 4;

// Go back to drawing with the current pen color and size (eraser off)
function usePen() {
    isErasing = false;
    line.globalCompositeOperation = 'source-over';
    line.strokeStyle = penColor;
    line.lineWidth = penSize;
    eraserBtn.classList.remove('active');
    canvas.classList.remove('erasing');
}

// Clear
clearBtn.addEventListener("click", () => {
    line.clearRect(0, 0, canvas.width, canvas.height);
});

// Eraser
eraserBtn.addEventListener("click", () => {
    if (isErasing) {
        usePen();
        return;
    }
    isErasing = true;
    line.globalCompositeOperation = 'destination-out';
    line.lineWidth = 20;
    eraserBtn.classList.add('active');   // pressed-in look
    canvas.classList.add('erasing');     // flipped-pencil cursor
});

// Marker colors
document.querySelectorAll('.swatch').forEach((btn) => {
    btn.addEventListener("click", () => {
        document.querySelectorAll('.swatch').forEach((b) => b.classList.remove('active'));
        btn.classList.add('active');
        penColor = btn.dataset.color;
        usePen();
    });
});

// Pen sizes
document.querySelectorAll('.size-btn').forEach((btn) => {
    btn.addEventListener("click", () => {
        document.querySelectorAll('.size-btn').forEach((b) => b.classList.remove('active'));
        btn.classList.add('active');
        penSize = Number(btn.dataset.size);
        usePen();
    });
});

// send doodle 


// MOOD SHARING
// sends to the pi
async function sendMood(mood) {
    const response = await fetch("/led/on", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mood: mood })
    });
}
// hooking up
const helloBtn = document.querySelector('.mood-btn[data-mood="hello"]');
helloBtn.addEventListener("click", () => {
    sendMood("hello");
});
const missBtn = document.querySelector('.mood-btn[data-mood="miss"]');
missBtn.addEventListener("click", () => {
    sendMood("miss");
});
const proudBtn = document.querySelector('.mood-btn[data-mood="proud"]');
proudBtn.addEventListener("click", () => {
    sendMood("proud");
});
const loveBtn = document.querySelector('.mood-btn[data-mood="love"]');
loveBtn.addEventListener("click", () => {
    sendMood("love");
});


// haptic hug
const hugBtn = document.getElementById('hug-btn');
const MAX_HOLD_MS = 2000;   // holding this long (or longer) = max intensity
let hugStart = null;

// Sends a hug to the other device
function sendHug(intensity) {
    console.log("Hug sent, intensity:", intensity);
}

// press hug
hugBtn.addEventListener("pointerdown", (e) => {
    e.preventDefault();
    hugStart = performance.now();
    hugBtn.classList.add('holding');
    hugBtn.setPointerCapture(e.pointerId);  // keep tracking even if the finger slides off
});

// release hug
function endHug() {
    if (hugStart === null)
        return;
    const heldFor = performance.now() - hugStart;
    hugStart = null;
    hugBtn.classList.remove('holding');

    const fraction = Math.min(heldFor / MAX_HOLD_MS, 1);    // 0 to 1, capped
    const intensity = Math.max(1, Math.ceil(fraction * 10)); // 1 to 10
    sendHug(intensity);
}

hugBtn.addEventListener("pointerup", endHug);
hugBtn.addEventListener("pointercancel", endHug);

// stop the phone's long-press menu from popping up on the heart
hugBtn.addEventListener("contextmenu", (e) => e.preventDefault());
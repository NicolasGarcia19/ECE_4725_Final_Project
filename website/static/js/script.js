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

// ---- tool buttons ----
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

// Clear: wipe the whole canvas
clearBtn.addEventListener("click", () => {
    line.clearRect(0, 0, canvas.width, canvas.height);
});

// Eraser: click to turn on, click again to go back to the pen
eraserBtn.addEventListener("click", () => {
    if (isErasing) {
        usePen();
        return;
    }
    isErasing = true;
    // "destination-out" makes strokes remove ink instead of adding it
    line.globalCompositeOperation = 'destination-out';
    line.lineWidth = 20;
    eraserBtn.classList.add('active');   // pressed-in look
    canvas.classList.add('erasing');     // flipped-pencil cursor
});

// Marker colors: pick one, move the ring to it, go back to the pen
document.querySelectorAll('.swatch').forEach((btn) => {
    btn.addEventListener("click", () => {
        document.querySelectorAll('.swatch').forEach((b) => b.classList.remove('active'));
        btn.classList.add('active');
        penColor = btn.dataset.color;
        usePen();
    });
});

// Pen sizes: same idea
document.querySelectorAll('.size-btn').forEach((btn) => {
    btn.addEventListener("click", () => {
        document.querySelectorAll('.size-btn').forEach((b) => b.classList.remove('active'));
        btn.classList.add('active');
        penSize = Number(btn.dataset.size);
        usePen();
    });
});

// ---- send doodle ----
const sendBtn = document.getElementById('send-btn');

// Sends the drawing to the other device.
// For now it only logs it; the real sending to the Pi goes here later.
function sendDoodle(image) {
    console.log("Doodle sent:", image.slice(0, 60) + "...");
}

sendBtn.addEventListener("click", () => {
    // turn the drawing into an image (a long text string of PNG data)
    sendDoodle(canvas.toDataURL('image/png'));

    // little "Sent!" message, then back to normal
    sendBtn.textContent = 'Sent! ♡';
    sendBtn.disabled = true;
    setTimeout(() => {
        sendBtn.textContent = 'Send ✈';
        sendBtn.disabled = false;
    }, 1500);
});

// ---- mood sharing ----

// Sends a mood to the other device.
// For now it only logs it; the real sending to the Pi goes here later.
function sendMood(mood) {
    console.log("Mood sent:", mood);
}

// Hook up every mood button; each one knows its mood from data-mood="..."
document.querySelectorAll('.mood-btn').forEach((btn) => {
    btn.addEventListener("click", () => {
        sendMood(btn.dataset.mood);
    });
});

// ---- haptic hug ----
const hugBtn = document.getElementById('hug-btn');
const MAX_HOLD_MS = 2000;   // holding this long (or longer) = max intensity
let hugStart = null;

// Sends a hug to the other device. intensity is 1 (quick tap) to 10 (held 2s+).
// For now it only logs it; the real sending to the Pi goes here later.
function sendHug(intensity) {
    console.log("Hug sent, intensity:", intensity);
}

// Press: start the timer; the CSS "holding" class makes it grow + shake
hugBtn.addEventListener("pointerdown", (e) => {
    e.preventDefault();
    hugStart = performance.now();
    hugBtn.classList.add('holding');
    hugBtn.setPointerCapture(e.pointerId);  // keep tracking even if the finger slides off
});

// Release: work out how long it was held, send it, shrink back
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
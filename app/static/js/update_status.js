// Disable F5 and Ctrl+R
window.addEventListener('keydown', function(e) {
    if ((e.which || e.keyCode) == 116 || (e.ctrlKey && (e.which === 82))) {
        e.preventDefault();
    }
});

// Disable context menu (right-click) and refresh
window.addEventListener('contextmenu', function(e) {
    e.preventDefault();
}, false);


let startY; // Variable to store the initial touch position
let startX; // Variable to store the initial touch position along the X-axis

// Listen for touchstart event
document.addEventListener('touchstart', function(event) {
  // Get the starting X and Y positions of the touch
  startX = event.touches[0].clientX;
  startY = event.touches[0].clientY;
}, false);

// Listen for touchmove event
document.addEventListener('touchmove', function(event) {
  // Calculate the distance the finger has moved along the Y-axis
  let currentY = event.touches[0].clientY;
  let distanceY = startY - currentY;

  // Calculate the distance the finger has moved along the X-axis
  let currentX = event.touches[0].clientX;
  let distanceX = startX - currentX;

  // Check if the user is swiping from the top of the screen
  if (distanceY > 0 && Math.abs(distanceX) < Math.abs(distanceY / 2)) {
    // Prevent the default behavior (e.g., scroll or refresh)
    event.preventDefault();
  }
}, false);

// Listen for touchend event
document.addEventListener('touchend', function(event) {
  // Reset the starting position
  startY = null;
  startX = null;
}, false);

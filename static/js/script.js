/* # Author: Francois Oratile Kgatlhanye
 * # Date: 2026-06-04
 * # Description: Functionality of Oradio website.
 */

// Dropdown
const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");
if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
  });
  document.addEventListener("click", (e) => {
    if (!dropdownButton.contains(e.target) && !dropdownMenu.contains(e.target)) {
      dropdownMenu.classList.remove("show");
    }
  });
}

// Avatar preview
const photoInput = document.querySelector("#avatar");
const photoPreview = document.querySelector("#preview-avatar");
if (photoInput)
  photoInput.onchange = () => {
    const [file] = photoInput.files;
    if (file) photoPreview.src = URL.createObjectURL(file);
  };

// Scroll to bottom
const conversationThread = document.querySelector(".room__box");
if (conversationThread) conversationThread.scrollTop = conversationThread.scrollHeight;

// Exclusive audio — one plays at a time
// Uses capture on window so it catches the event before the browser handles it
let currentAudio = null;

window.addEventListener("play", (e) => {
  if (e.target.tagName !== "AUDIO") return;
  if (currentAudio && currentAudio !== e.target) {
    currentAudio.pause();
    currentAudio.currentTime = 0;
  }
  currentAudio = e.target;
}, true);

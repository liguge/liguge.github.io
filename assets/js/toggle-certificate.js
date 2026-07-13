/**
 * Toggle certificate image visibility by ID
 * Usage: onclick="toggleCertificate('esiImage')"
 */
function toggleCertificate(imgId) {
  var img = document.getElementById(imgId);
  if (!img) return;
  img.style.display = (img.style.display === "none") ? "inline-block" : "none";
}

/**
 * Toggle certificate image visibility by ID
 * Usage: onclick="toggleCertificate('esiImage')"
 */
function toggleCertificate(imgId) {
  const img = document.getElementById(imgId);
  if (!img) return;
  img.style.visibility = img.style.visibility === 'visible' ? 'hidden' : 'visible';
}

function toggleCertificate1(imgId) {
  var img = document.getElementById(imgId);
  if (!img) return;
  img.style.display = img.style.display === "none" ? "inline-block" : "none";
}


const modal = document.getElementById('modal');
const modalImg = document.getElementById('modalImage');
const closeBtn = document.getElementsByClassName('close')[0];
const galleryImages = document.querySelectorAll('.gallery-img');

// Открытие модального окна для любой картинки
galleryImages.forEach(img => {
  img.addEventListener('click', function() {
    modal.style.display = 'block';
    modalImg.src = this.getAttribute('data-src');
  });
});

// Закрытие по клику на крестик
closeBtn.onclick = function() {
  modal.style.display = 'none';
}

// Закрытие по клику вне картинки
modal.onclick = function(event) {
  if (event.target === modal) {
    modal.style.display = 'none';
  }
}

// Закрытие по нажатию Escape
document.addEventListener('keydown', function(event) {
  if (event.key === 'Escape' && modal.style.display === 'block') {
    modal.style.display = 'none';
  }
});
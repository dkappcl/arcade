const search = document.getElementById('search');
if (search) {
  search.addEventListener('input', () => {
    const term = search.value.toLowerCase().trim();
    document.querySelectorAll('.card').forEach(card => {
      card.style.display = card.dataset.name.includes(term) ? '' : 'none';
    });
  });
}

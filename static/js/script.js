document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('click', function() {
        const fullText = card.getAttribute('data-text');
        document.getElementById('modalText').textContent = fullText;
        document.getElementById('modal').style.display = 'flex';
    });
});

document.getElementById('closeModal').addEventListener('click', function() {
    document.getElementById('modal').style.display = 'none';
});

window.addEventListener('click', function(event) {
    const modal = document.getElementById('modal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});
document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('click', function() {
        const fullText = card.getAttribute('data-text');
        document.getElementById('modalText').textContent = fullText;
        document.getElementById('modal').style.display = 'flex';
    });
});

document.getElementById('closeModal').addEventListener('click', function() {
    document.getElementById('modal').style.display = 'none';
});

window.addEventListener('click', function(event) {
    const modal = document.getElementById('modal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});


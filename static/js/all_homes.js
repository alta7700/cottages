(function () {
    document.querySelectorAll('.home-card--images-carousel').forEach(el => {
        const indexes = Array.from({ length: el.children.length }, (_, i) => i);
        for (let i = 1; i <= 3; i++) {
            const [index] = indexes.splice(Math.floor(Math.random() * indexes.length), 1);
            el.children.item(index).classList.add(`i${i}`)
        }
    });

    document.querySelectorAll('.home-card').forEach(card => {
        card.querySelector('.home-card--book-btn-wrapper button')?.addEventListener('click', e => {
            e.preventDefault();
            ticketFormPortal.show(card.dataset.homeId)
        })
    });
})();

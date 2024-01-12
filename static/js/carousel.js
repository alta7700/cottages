document.querySelectorAll('.carousel').forEach(carousel => {
    function selectImage(e) {
        const currentSelected = scroller.querySelector('.carousel-image[data-selected]')
        if (currentSelected !== null) {
            delete currentSelected.dataset.selected
        }
        const img = scroller.querySelector(
            `.carousel-image[data-position="${e.target.dataset.position}"] > img`
        )
        preview.replaceChildren(img.cloneNode())
    }
    function setPreviewImage(index) {
        const img = scroller.querySelector(
            `.carousel-image[data-position="${e.target.dataset.position}"] > img`
        )
        preview.replaceChildren(img.cloneNode())
    }

    const preview = carousel.appendChild(document.createElement('div'))
    preview.classList.add('carousel-preview')
    preview.appendChild(carousel.querySelector(
        '.carousel-image[data-selected] > img'
    ).cloneNode())
    const scroller = carousel.appendChild(document.createElement('div'))
    scroller.classList.add('carousel-images-scroller')
    carousel.querySelectorAll('.carousel-image').forEach(item => {
        const img = item.appendChild(document.createElement('img'))
        img.src = item.dataset.src
        img.alt = ''
        scroller.appendChild(carousel.removeChild(item)).addEventListener('click', selectImage)
    })
})
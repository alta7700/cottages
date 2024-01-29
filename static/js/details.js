document.querySelectorAll('.swiper[data-carousel]').forEach(el => {
    const swiperThumb  = new Swiper(el.parentElement.querySelector('[data-carousel-thumb]'), {
        a11y: false,
        slidesPerView: 'auto',
        freeMode: true,
        spaceBetween: 8,
    })
    const swiper = new Swiper(el, {
        a11y: false,
        pagination: {
            el: '.carousel-pagination',
            clickable: true,
            renderBullet(index, className) {
                const name = el.querySelectorAll('.swiper-slide').item(index).dataset.name
                return `<span class="${className}"><span class="text">${name}</span></span>`
            },
            modifierClass: 'carousel-pagination-',
            horizontalClass: 'carousel-pagination-horizontal',
            bulletClass: 'carousel-bullet button medium light',
            bulletActiveClass: 'dark',
        },
        navigation: {
            prevEl: '.carousel-prev',
            nextEl: '.carousel-next',
        },
        thumbs: {
            swiper: swiperThumb,
        },
        spaceBetween: 8,
    });
    const updateThumb = (xx) => {
        swiperThumb.slides.forEach((el, index) => {
            if (index === swiper.activeIndex) {
                el.firstElementChild.classList.add('dark')
                el.firstElementChild.classList.remove('light')
            } else {
                el.firstElementChild.classList.add('light')
                el.firstElementChild.classList.remove('dark')
            }
        });
        // if (!swiperThumb.el.checkVisibility()) return
        let offset =
            swiperThumb.slides[swiper.activeIndex].getBoundingClientRect().x
            -
            swiperThumb.el.getBoundingClientRect().x;
        const maxOffset = swiperThumb.el.scrollWidth - swiperThumb.el.clientWidth;
        if (offset > maxOffset) offset = maxOffset;
        if (offset === 0) return
        swiperThumb.setTranslate(swiperThumb.getTranslate() - offset);
    }
    updateThumb();
    swiper.on('slideChange', updateThumb)
});

(function() {
    const coversEl = document.querySelector('.home-covers');
    const detailsEl = document.querySelector('.home-details');

    const swiperEl = coversEl.querySelector('.swiper');
    const initialSlide = Array.from(swiperEl.querySelectorAll('.swiper-slide'))
        .findIndex(el => el.dataset.homeId === window.initialHomeId.toString())
    const swiper = new Swiper(swiperEl, {
        a11y: false,
        initialSlide: initialSlide === -1 ? 0 : initialSlide,
        navigation: {
            prevEl: coversEl.querySelector('.home-covers-prev'),
            nextEl: coversEl.querySelector('.home-covers-next'),
        },
    });
    coversEl.querySelectorAll('[data-book-btn]').forEach(btn => {
        btn.addEventListener('click', () => {
            ticketFormPortal.show({ homeId: swiper.slides[swiper.activeIndex].dataset.homeId });
        })
    });
    const pagesButton = swiper.el.querySelector('.home-covers-pages .text');
    pagesButton.addEventListener('click', () => {
        detailsEl.scrollIntoView({ behavior: "smooth" })
    })
    function onCoverChange() {
        Array.from(detailsEl.children).forEach(el => el.classList.add('hidden'));
        detailsEl.children.item(swiper.activeIndex).classList.remove('hidden');
        pagesButton.textContent =
            `${swiper.slides.at(swiper.activeIndex).dataset.homeName} ${swiper.activeIndex + 1}/${swiper.slides.length}`;
    }
    swiper.on('slideChange', onCoverChange);
    onCoverChange();

    Array.from(detailsEl.children).forEach(detail => {
        const buttons = detail.querySelector('.home-info-main-buttons').children;
        buttons.item(0)?.classList.replace('light', 'dark')
        buttons.item(1)?.classList.replace('light', 'dark')
        detail.querySelectorAll('.button[data-show-on-map]').forEach(el => {
            el.addEventListener('click', () => {
                detail.querySelector('.home-location')?.scrollIntoView({ behavior: "smooth" });
            })
        })
    })
    swiperEl.classList.remove('invisible')
})();

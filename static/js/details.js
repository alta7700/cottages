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
    const updateThumb = () => {
        const activeName = swiper.slides[swiper.activeIndex].dataset.name;
        swiperThumb.slides.forEach((el) => {
            if (el.dataset.name === activeName) {
                el.firstElementChild.classList.add('dark')
                el.firstElementChild.classList.remove('light')
            } else {
                el.firstElementChild.classList.add('light')
                el.firstElementChild.classList.remove('dark')
            }
        });
        if (!swiperThumb.el.checkVisibility()) return
        let offset = swiperThumb.slides[swiper.activeIndex].getBoundingClientRect().x;
        const maxOffset = swiperThumb.el.scrollWidth - swiperThumb.el.clientWidth;
        if (offset > maxOffset) offset = maxOffset;
        if (offset === 0) return
        swiperThumb.setTranslate(swiperThumb.getTranslate() - offset);
    }
    updateThumb()
    swiper.on('slideChange', updateThumb)
});

(function() {
    const coversEl = document.querySelector('.home-covers');

    const swiperEl = coversEl.querySelector('.swiper');
    const swiper = new Swiper(swiperEl, {
        a11y: false,
        pagination: {
            el: coversEl.querySelector('.home-covers-pages'),
            type: 'custom',
            renderCustom(swiper, current, total) {
                const c = current.toFixed().padStart(2, '0')
                const t = total.toFixed().padStart(2, '0')
                return `<span class="text">${c} / ${t}</span>`
            }
        },
        navigation: {
            prevEl: coversEl.querySelector('.home-covers-prev'),
            nextEl: coversEl.querySelector('.home-covers-next'),
        },
    });
    coversEl.querySelector('.home-covers--book-btn').addEventListener('click', () => {
        console.log(swiper.slides[swiper.activeIndex].dataset.homeId)
        ticketFormPortal.show({ homeId: swiper.slides[swiper.activeIndex].dataset.homeId });
    });
})();

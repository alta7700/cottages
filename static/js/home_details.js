
(function() {
    const covers = document.getElementById('home-covers');
    const homeIDs = [...covers.querySelectorAll('.home-cover')].map(el => Number(el.dataset.homeId));
    covers.onHomeChange = []
    const details = document.getElementById('home-details');

    function getLastHomeIndex() { return homeIDs.length - 1 }

    function getActiveHomeEl() { return covers.querySelector('.home-cover[data-active]') }

    function getActiveHomeDetailEl() { return details.querySelector('.home-detail[data-active]') }

    function getActiveHomeIndex() { return Number(getActiveHomeEl().dataset.position) }

    function getHomeElByIndex(index) { return covers.querySelector(`.home-cover[data-position="${index}"]`) }

    function getHomeDetailElByIndex(index) { return details.querySelector(`.home-detail[data-position="${index}"]`) }

    function getPrevHomeIndex() {
        const currentIndex = getActiveHomeIndex();
        return currentIndex === 0 ? getLastHomeIndex() : currentIndex - 1;
    }

    function getNextHomeIndex() {
        const currentIndex = getActiveHomeIndex();
        return currentIndex === getLastHomeIndex() ? 0 : currentIndex + 1;
    }

    function getChevron(pos) {
        return covers.querySelector(`.chevron-btn[data-${pos}]`)
    }

    function setActiveIndex(index) {
        const pastIndex = getActiveHomeIndex()
        delete getActiveHomeEl().dataset.active;
        delete getActiveHomeDetailEl().dataset.active;

        getHomeElByIndex(index).dataset.active = '';
        getHomeDetailElByIndex(index).dataset.active = '';

        const leftChevron = getChevron('left')
        const rightChevron = getChevron('right')
        leftChevron.classList.remove('hidden')
        rightChevron.classList.remove('hidden')
        if (index === 0) {
            leftChevron.classList.add('hidden');
        }
        if (index === getLastHomeIndex()) {
            rightChevron.classList.add('hidden');
        }
        covers.onHomeChange.forEach(callback => callback(index, pastIndex))
    }

    function showPrevHome() {
        getChevron('right').classList.remove('hidden');
        setActiveIndex(getPrevHomeIndex());
    }

    function showNextHome() {
        getChevron('left').classList.remove('hidden');
        setActiveIndex(getNextHomeIndex());
    }

    // активируем первый или установленный из шаблона активный дом
    if (initialHomeId !== undefined) {
        document.querySelector(`.home-cover[data-home-id="${initialHomeId}"]`).dataset.active = '';
        document.querySelector(`.home-detail[data-home-id="${initialHomeId}"]`).dataset.active = '';
    } else {
        document.querySelector('.home-cover[data-position="0"]').dataset.active = '';
        document.querySelector('.home-detail[data-position="0"]').dataset.active = '';
    }

    // Скрываем левый или правый шевроны если уперлись с самого начала
    getChevron('left').addEventListener('click', showPrevHome);
    getChevron('right').addEventListener('click', showNextHome);
    if (getActiveHomeIndex() === 0) {
        getChevron('left').classList.add('hidden');
    }
    if (getActiveHomeIndex() === getLastHomeIndex()) {
        getChevron('right').classList.add('hidden');
    }

    // добавляем к видео хэндлер перехода на другую вкладку или дом. Необходимо останавливать видео
    document.querySelectorAll('.tabs').forEach(tabs => {
        const youtubeVideo = tabs.querySelector('.home-detail__video iframe')
        youtubeVideo && tabs.onTabChange.push((_, pastTabName) => {
            pastTabName === 'video' && youtubeVideo.contentWindow.postMessage(
                '{"event":"command","func":"pauseVideo","args":""}', '*'
            )
        })
    })
    covers.onHomeChange.push((_, pastIndex) => {
        details.querySelector(
            `.home-detail[data-position="${pastIndex}"] .home-detail__video iframe`
        )?.contentWindow.postMessage('{"event":"command","func":"pauseVideo","args":""}', '*')
    })

    // скролим до табов если при переходе из списка "Все дома" не была нажата кнопка забронировать
    if (new URLSearchParams(window.location.search).get('scroll') === "1") {
        setTimeout(() =>
            document.querySelector('#home-details').scrollIntoView({behavior: "smooth"}),
            300
        )
    }


    const formDialog = document.querySelector('#book-home');
    const form = formDialog.querySelector('form');

    // добавляем календарь на dtrange
    new AirDatepicker(form.querySelector('input[name="dtrange"]'), {
        range: true,
        minDate: new Date(),
        dateFormat: "dd.MM.yyyy",
        multipleDatesSeparator: " - ",
    })

    // добавляем на все кнопки "Забронировать" на обложке открытие формы с подстановкой имя и homeId в форму
    covers.querySelectorAll('.home-cover').forEach(cover => {
        cover.querySelector('.primary-button').addEventListener('click', (e) => {
            formDialog.showPopover();
            form.reset();
            form.querySelector('input[name="home"]').value = cover.dataset.homeId;
            formDialog.querySelector('.book-home-form-name').textContent =
                e.currentTarget.parentElement.querySelector('.home-cover__info__name').textContent;
        })
    })
    // убираем ошибку с поля при начале ввода в него
    form.querySelectorAll('input:not([type="hidden"])').forEach(el => {
        el.addEventListener('focus', () => {
            if (el.dataset.hasError !== undefined) {
                delete el.dataset.hasError
            }
        })
    })
    // Отправляем запрос на сервер вместо обычного поведения браузера на отправку формы
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        form.querySelectorAll('button[type="submit"], input').forEach(el => {
            el.disabled = true;
        });
        fetch('/ticket', {method: "post", body: formData})
            .then(res => {
                if (res.status === 200) {
                    const parent = form.parentElement;
                    parent.removeChild(form);
                    parent.dataset.completed = '';
                    const text = parent.appendChild(document.createElement('p'));
                    text.innerHTML = 'Заявка успешно отправлена.<br>Менеджер свяжется с вами для уточнения деталей.';
                    formDialog.close();
                    console.info('notify success');
                }
                if (res.status === 400) return res.json()
            })
            .then(data => {
                if (data?.errors) {
                    data.errors.forEach(fieldName => {
                        form.querySelector(`input[name="${fieldName}"]`).dataset.hasError = '';
                    })
                }
            })
            .catch(() => {
                formDialog.close();
                console.error('notify error');
            })
            .finally(() => {
                form.querySelectorAll('button[type="submit"], input').forEach(el => {
                    el.disabled = false;
                });
            });
    });
})();

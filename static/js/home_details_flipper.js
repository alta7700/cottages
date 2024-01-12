const covers = document.getElementById('home-covers');
covers.onHomeChange = []
const details = document.getElementById('home-details');

function getLastHomeIndex() { return homeIDs.length - 1 }

function getActiveHomeEl() { return covers.querySelector('.home-cover[data-active]') }
function getActiveHomeDetailEl() { return details.querySelector('.home-detail[data-active]') }
function getActiveHomeIndex() { return Number(getActiveHomeEl().dataset.position) }
function getHomeElByIndex(index) {
    return covers.querySelector(`.home-cover[data-position="${index}"]`)
}
function getHomeDetailElByIndex(index) {
    return details.querySelector(`.home-detail[data-position="${index}"]`)
}

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

getChevron('left').addEventListener('click', showPrevHome);
getChevron('right').addEventListener('click', showNextHome);
if (getActiveHomeIndex() === 0) {
    getChevron('left').classList.add('hidden');
}
if (getActiveHomeIndex === getLastHomeIndex()) {
    getChevron('right').classList.add('hidden');
}
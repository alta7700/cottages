document.querySelectorAll('.tabs').forEach(tabs => {
    const tabLabels = tabs.insertBefore(document.createElement('div'), tabs.firstChild)
    tabLabels.classList.add('tab-labels')

    function selectTab(e) {
        const newTabName = e.target.dataset.name
        const currentSelected = tabLabels.querySelector(`.tab-label[data-selected]`)
        const currentTabName = currentSelected.dataset.name
        if (newTabName === currentTabName) {
            return
        }

        delete currentSelected.dataset.selected
        delete tabs.querySelector(`.tab[data-selected]`).dataset.selected

        tabLabels.querySelector(`.tab-label[data-name="${newTabName}"]`).dataset.selected = ''
        tabs.querySelector(`.tab[data-name="${newTabName}"]`).dataset.selected = ''
        tabs.onTabChange.forEach(callback => callback(newTabName, currentTabName))
    }

    tabs.querySelectorAll(`.tab`).forEach(tab => {
        const tabLabelEl = tabLabels.appendChild(document.createElement('span'))
        tabLabelEl.classList.add('tab-label')
        tabLabelEl.role = 'button'
        tabLabelEl.tabIndex = 0
        tabLabelEl.addEventListener('click', selectTab)
        tabLabelEl.addEventListener('keydown', e => ['Space', 'Enter'].includes(e.code) && selectTab(e))
        tabLabelEl.dataset.name = tab.dataset.name
        tabLabelEl.textContent = tab.dataset.label
        if (tab.dataset.selected !== undefined) {
            tabLabelEl.dataset.selected = tab.dataset.selected
        }
    })
    tabs.onTabChange = []
})
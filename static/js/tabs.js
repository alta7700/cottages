document.querySelectorAll('.tabs').forEach(tabs => {
    const tabLabels = tabs.insertBefore(document.createElement('div'), tabs.firstChild)
    tabLabels.classList.add('tab-labels')

    function selectTab(e) {
        const tabName = e.target.dataset.name
        const currentSelected = tabLabels.querySelector(`.tab-label[data-selected]`)
        if (tabName === currentSelected.dataset.name) {
            return
        }

        delete currentSelected.dataset.selected
        delete tabs.querySelector(`.tab[data-selected]`).dataset.selected

        tabLabels.querySelector(`.tab-label[data-name="${tabName}"]`).dataset.selected = ''
        tabs.querySelector(`.tab[data-name="${tabName}"]`).dataset.selected = ''
    }

    tabs.querySelectorAll(`.tab`).forEach(tab => {
        const tabLabelEl = tabLabels.appendChild(document.createElement('span'))
        tabLabelEl.classList.add('tab-label')
        tabLabelEl.role = 'button'
        tabLabelEl.tabIndex = 0
        tabLabelEl.addEventListener('click', selectTab)
        tabLabelEl.dataset.name = tab.dataset.name
        tabLabelEl.textContent = tab.dataset.label
        if (tab.dataset.selected !== undefined) {
            tabLabelEl.dataset.selected = tab.dataset.selected
        }
    })
})
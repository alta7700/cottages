document.querySelectorAll('#portals .portal').forEach(portal => {
    portal.show = function(params) {
        portal.dataset.open = '';
        portal.dispatchEvent(new CustomEvent('showPortal', { detail: params }))
    }
    portal.hide = function(params) {
        delete portal.dataset.open
        portal.dispatchEvent(new CustomEvent('hidePortal', { detail: params }))
    }
    portal.querySelector('.modal-close-wrapper button').addEventListener('click', () => {
        portal.hide({ escape: true })
    })

    if (portal.dataset.disableHideOnEscape === undefined) {
        portal.addEventListener('showPortal', () => {
            function hidePortalOnEscape(e) {
                if (e.key === 'Escape') {
                    e.preventDefault();
                    e.stopPropagation();
                    portal.hide({escape: true})
                }
            }
            document.addEventListener('keydown', hidePortalOnEscape)
            portal.addEventListener('hidePortal', () => {
                document.removeEventListener('keydown', hidePortalOnEscape)
            }, {once: true})
        });
    }
});
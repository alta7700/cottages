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

(function() {
    let notifications = document.querySelector('#notifications');
    if (!notifications) {
        notifications = document.body.appendChild(document.createElement('div'));
    }
    notifications.id = 'notifications';
    document.closeNotification = function (el) {
        notifications.removeChild(el);
    }
    document.showNotification = function (text, options) {
        const {
            autoClose = 5000,
            status = 'success',
            onClose,
        } = options || {};
        const notificationEl = notifications.appendChild(document.createElement('div'));
        notificationEl.classList.add('notification');
        notificationEl.dataset.status = status;
        notificationEl.innerHTML =
            `<div class="notification-info">
                <div class="notification-icon">${icons[status]}</div>
                <p>${text}</p>
            </div>
            <div class="notification-close-wrapper">
                <button class="button medium icon-button" data-close-btn>${icons.close}</button>
            </div>`;

        notificationEl.close = () => {
            document.closeNotification(notificationEl);
            notificationEl.autoCloseTimer && clearTimeout(notificationEl.autoCloseTimer);
            onClose && onClose();
        };
        if (autoClose) {
            notificationEl.autoCloseTimer = setTimeout(notificationEl.close, autoClose);
        }
        notificationEl.querySelector('[data-close-btn]').addEventListener('click', notificationEl.close)
        return notificationEl;
    };

    const icons = {
        success: '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M9.99999 15.172L19.192 5.979L20.607 7.393L9.99999 18L3.63599 11.636L5.04999 10.222L9.99999 15.172Z"></path></svg>',
        error: '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 22C6.477 22 2 17.523 2 12C2 6.477 6.477 2 12 2C17.523 2 22 6.477 22 12C22 17.523 17.523 22 12 22ZM12 20C14.1217 20 16.1566 19.1571 17.6569 17.6569C19.1571 16.1566 20 14.1217 20 12C20 9.87827 19.1571 7.84344 17.6569 6.34315C16.1566 4.84285 14.1217 4 12 4C9.87827 4 7.84344 4.84285 6.34315 6.34315C4.84285 7.84344 4 9.87827 4 12C4 14.1217 4.84285 16.1566 6.34315 17.6569C7.84344 19.1571 9.87827 20 12 20ZM11 15H13V17H11V15ZM11 7H13V13H11V7Z"></path></svg>',
        close: '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M11.9997 10.5862L16.9497 5.63623L18.3637 7.05023L13.4137 12.0002L18.3637 16.9502L16.9497 18.3642L11.9997 13.4142L7.04974 18.3642L5.63574 16.9502L10.5857 12.0002L5.63574 7.05023L7.04974 5.63623L11.9997 10.5862Z"></path></svg>',
    }
})();

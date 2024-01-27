document.addEventListener("DOMContentLoaded", () => {
    const ticketFormPortal = document.querySelector('#ticket-form-portal');
    const ticketForm = document.querySelector('#ticket-form');

    // PhoneField //////////////////////////////////////////////////////////////////////////////////////////////////////
    (function () {
        function getInputNumbers(value) {
            return value.replace(/\D/g, '');
        }
        function onPhonePaste(e) {
            const input = e.target;
            const inputNumbers = getInputNumbers(input.value);
            const pasted = e.clipboardData || window.clipboardData;
            if (pasted) {
                let pastedText = getInputNumbers(pasted.getData('Text'));
                if (pastedText.length === 11) pastedText = pastedText.slice(1);
                if (pastedText.length === 10) input.value = pastedText;
                else input.value = inputNumbers;
            }
        }
        function onPhoneInput(e, ignoreSelection = false) {
            const input = e.target;
            let inputNumbers = getInputNumbers(input.value);
            if (!ignoreSelection && input.value.length !== input.selectionStart) {
                if (e.data && /\D/g.test(e.data)) {
                    input.value = inputNumbers;
                }
                return;
            }

            if (inputNumbers.length === 11 && ['7', '8'].includes(inputNumbers[0])) {
                inputNumbers = inputNumbers.slice(1);
            }
            if (inputNumbers.length > 10) return;

            let formattedInputValue = '';
            if (inputNumbers.length > 0) {
                formattedInputValue += '(' + inputNumbers.substring(0, 3);
            }
            if (inputNumbers.length > 3) {
                formattedInputValue += ') ' + inputNumbers.substring(3, 6);
            }
            if (inputNumbers.length > 6) {
                formattedInputValue += '-' + inputNumbers.substring(6, 8);
            }
            if (inputNumbers.length > 8) {
                formattedInputValue += '-' + inputNumbers.substring(8, 10);
            }
            input.value = formattedInputValue;
            if (inputNumbers.length === 10) {
                input.dataset.filled = "";
            } else {
                delete input.dataset.filled;
            }
        }
        const inputEl = ticketForm.querySelector('.input[name="phone"]');
        inputEl.addEventListener('input', onPhoneInput, false);
        inputEl.addEventListener('change', (e) => onPhoneInput(e, true), false);
        inputEl.addEventListener('paste', onPhonePaste, false);
    })();
    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    // TextField ///////////////////////////////////////////////////////////////////////////////////////////////////////
    (function () {
        function setFilledTextFieldIfRespond(el) {
            let min = el.minLength;
            let max = el.maxLength;
            if (min === -1 && el.required) {
                min = 1;
            }
            if (el.value.length >= min && (max === -1 || el.value.length <= max)) {
                el.dataset.filled = "";
            } else {
                delete el.dataset.filled;
            }
        }
        const inputEl = ticketForm.querySelector('.input[name="name"]');
        inputEl.addEventListener('input', (e) => setFilledTextFieldIfRespond(e.target));
        inputEl.addEventListener('change', (e) => setFilledTextFieldIfRespond(e.target));
        setFilledTextFieldIfRespond(inputEl);
    })();
    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    // NumberField /////////////////////////////////////////////////////////////////////////////////////////////////////
    (function () {
        function getValidInteger(v) {
            let num = parseInt(v, 10);
            if (isNaN(num)) return null;
            return num;
        }
        function getMinMax(input) {
            return [
                input.min ? Number(input.min) : undefined,
                input.max ? Number(input.max) : undefined
            ];
        }
        function setValue(input, value) {
            const [min, max] = getMinMax(input);
            if (value === null) {
                input.value = min ?? (max === undefined ? 1 : (max < 1 ? max : 1));
                return;
            }
            if (min !== undefined && value < min) value = min;
            else if (max !== undefined && value > max) value = max;
            input.value = value;
            if (minusButton) minusButton.disabled = value <= min;
            if (plusButton) plusButton.disabled = value >= max;
            delete input.dataset.hasError;
            input.dataset.filled = '';
        }
        const inputEl = ticketForm.querySelector('.input[name="guests"]');
        const minusButton  = inputEl.parentElement.parentElement.querySelector('.number-input-minus');
        const plusButton  = inputEl.parentElement.parentElement.querySelector('.number-input-plus');
        minusButton?.addEventListener('click', () => {
            let value = getValidInteger(inputEl.value);
            setValue(inputEl, value !== null ? value - 1 : null);
        })
        plusButton?.addEventListener('click', () => {
            let value = getValidInteger(inputEl.value);
            setValue(inputEl, value !== null ? value + 1 : null);
        })
        inputEl.addEventListener('change', () => {
            let value = getValidInteger(inputEl.value);
            if (value === null) {
                inputEl.dataset.hasError = '';
                delete inputEl.dataset.filled
                return
            }
            setValue(inputEl, value);
        })
        setValue(inputEl, inputEl.value ? inputEl.value : null)
    })();

    // DateRangeField //////////////////////////////////////////////////////////////////////////////////////////////////
    (function () {
        const inputEl = ticketForm.querySelector('.input[name="dtrange"]');
        inputEl.parentElement.querySelector(".input-icon-helper")?.addEventListener('click', () => inputEl.focus())
        new AirDatepicker(inputEl, {
            range: true,
            minDate: new Date(),
            dateFormat: "dd.MM.yyyy",
            multipleDatesSeparator: " - ",
            container: ticketFormPortal,
            autoClose: false,
            keyboardNav: false,
            buttons: [
                {
                    content: 'Пятница - Воскресенье',
                    onClick(dp) {
                        dp.clear();
                        const today = new Date();
                        const friday = new Date();
                        const day = today.getDay();
                        if (day === 6) {
                            friday.setDate(today.getDate() + 6);
                        } else if (day === 0) {
                            friday.setDate(today.getDate() + 5);
                        } else if (day === 5) {
                            friday.setDate(today.getDate() + 7);
                        } else {
                            friday.setDate(today.getDate() + 5 - day);
                        }
                        dp.selectDate([
                            friday,
                            new Date(friday.getFullYear(), friday.getMonth(), friday.getDate() + 2)
                        ]);
                    }
                },
            ],
            position({$datepicker, $pointer}) {
                let coords = inputEl.parentElement.getBoundingClientRect(),
                    dpHeight = $datepicker.clientHeight,
                    dpWidth = $datepicker.clientWidth;

                $datepicker.style.left = `${coords.x + coords.width / 2 - dpWidth / 2}px`;
                $datepicker.style.top = `${coords.y - dpHeight - 17}px`;

                $pointer.style.display = 'none';
            },
        })
    })();
    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    // all fields //////////////////////////////////////////////////////////////////////////////////////////////////////
    (function () {
        function removeHasErrorAttrOnFocus(e) {
            delete e.target.dataset.hasError;
        }
        ticketForm.querySelectorAll('.input').forEach(input => {
            input.addEventListener('focus', removeHasErrorAttrOnFocus)
        })
    })();
    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    document.querySelector('#open-ticket-form').addEventListener('click', () => {
        ticketFormPortal.dataset.open = '';
        document.addEventListener('keydown', function closeTicketFormOnEscape(e) {
            if (e.key === 'Escape') delete ticketFormPortal.dataset.open;
            document.removeEventListener('keydown', closeTicketFormOnEscape)
        })
    })

    document.querySelector('#close-ticket-form').addEventListener('click', () => {
        delete ticketFormPortal.dataset.open;
    })
});

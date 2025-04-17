const helpers = {
  toggleClass: function (options = {}) {
    const {
      triggerSelector,
      eTargetSelector,
      toggleClass = 'active',
      triggerToggle = false,
      aria = {
        enable: false,
        initText: 'Открыть меню',
        onChangeText: 'Закрыть меню',
      },
    } = options;

    const trigger = document.querySelector(triggerSelector);

    if (!trigger) return;

    if (aria.enable) {
      trigger.setAttribute('aria-label', aria.initText);
    }

    const changeAriaAttribute = () => {
      let ariaLabelStateCondition = 'true' === trigger.getAttribute('aria-expanded');

      trigger.setAttribute('aria-expanded', !ariaLabelStateCondition),
        ariaLabelStateCondition
          ? trigger.setAttribute('aria-label', aria.initText)
          : trigger.setAttribute('aria-label', aria.onChangeText);
    };

    trigger.addEventListener('click', () => {
      if (aria.enable) {
        changeAriaAttribute();
      }

      const target = document.querySelector(eTargetSelector);

      if (!target) return;

      target.classList.toggle(toggleClass);

      if (!triggerToggle) return;
      trigger.classList.toggle(toggleClass);
    });
  },

  initMailForms: (options = {}) => {
    const {
      formSelectorAttribute = null,
      formSelectorName = null,
      buttonStateAttribute,
      closeButtonName = 'hide',
      openButtonName = 'show',
      hidingFieldsContainer,
      hideClass = 'hide',
    } = options;

    const mailForms = document.querySelectorAll(
      `[data-${formSelectorAttribute}=${formSelectorName}]`,
    );

    checkFormAvailable(mailForms);

    mailForms.forEach((form, idx) => {
      const hideTab = form.querySelector(`[data-${buttonStateAttribute}=${closeButtonName}]`);
      const showTab = form.querySelector(`[data-${buttonStateAttribute}=${openButtonName}]`);
      const submitBtn = form.querySelector('.btn')

      /* Накидываю хэш на инпуты, если вдруг ID и name аттрибуты одинаковые будут в разных формах */
      /* Берем все инпуты в форме */
      const inputs = form.querySelectorAll('input');

      // эмуляция отправки формы и очистка полей
      const handleSubmit = (e) => {
        e.preventDefault();
        inputs.forEach(input => {
          if (input.type === 'text' || input.type === 'email' || input.type === 'tel') input.value = ''
        })
      }
      submitBtn.addEventListener('click', handleSubmit)

      /* Фильтруем по наличию ID */
      let targetInputs = Array.from(inputs).filter((el) => el.id);

      /* Объявляю перемнную для сохранения предыдущего рандомного числа(ниже) */
      let prevRndNum;

      targetInputs.forEach((input) => {
        /* Рандом число */
        let rndNum = idx + getRndInteger(1, 999);

        /* Выполняется пока пред. ранд. число равно текущему */
        do {
          rndNum = idx + getRndInteger(1, 100) + getRndInteger(1, 999);
        } while (rndNum === prevRndNum);

        const nextEl = input.nextElementSibling;
        const prevEl = input.previousElementSibling;

        /* Чтоб не сломалось если вдруг соседа нет */
        if (!(nextEl || prevEl)) return;

        /* Если инпут ID равен for="" у лейбла накидываем хэш */
        if (nextEl.tagName === 'LABEL' && input.id === nextEl.htmlFor) {
          input.id = `${input.id}-${rndNum}`;
          nextEl.htmlFor = `${nextEl.htmlFor}-${rndNum}`;
        } else if (prevEl.tagName === 'LABEL' && input === prevEl.htmlFor) {
          input.id = `${input.id}-${rndNum}`;
          prevEl.htmlFor = `${prevEl.htmlFor}-${rndNum}`;
        }

        /* Обновляем рандом */
        //todo Нужно сделать по-другому. Добавлять все рандомные числа в массив и сверяться при каждой итерации, чтоюы ни одна цифра не повторилась
        prevRndNum = rndNum;
      });

      checkStateButtonsAvailable(hideTab, showTab);

      const formFields = form.querySelector(hidingFieldsContainer);

      if (hideTab.checked) {
        disableFields(formFields);
        hideFields(formFields, hideClass);
      } else if (showTab.checked) {
        enableFields(formFields);
        showFields(formFields, hideClass);
      }

      form.addEventListener('change', (e) => {
        if (e.target === hideTab) {
          disableFields(formFields);
          hideFields(formFields, hideClass);
        }
        if (e.target === showTab) {
          enableFields(formFields);
          showFields(formFields, hideClass);
        }
      });
    });

    function hideFields(elem, className) {
      elem.classList.add(className);
      elem.style.height = '0';
      elem.style.height = '0';
    }

    function showFields(elem, className) {
      elem.classList.remove(className);
      elem.style.height = `${elem.scrollHeight}px`;
    }

    function disableFields(container) {
      const inputs = container.querySelectorAll('input');

      inputs.forEach((input) => {
        input.setAttribute('disabled', '');
      });
    }

    function enableFields(container) {
      const inputs = container.querySelectorAll('input');

      inputs.forEach((input) => {
        input.removeAttribute('disabled');
      });
    }

    function checkFormAvailable(mailForms) {
      if (!mailForms.length) {
        console.error(mailForms);
        console.error(
          `Аттрибут заполнен некорректно или отсутствует в документе, проверьте корректность заполнения`,
        );
        return;
      }
    }

    function checkStateButtonsAvailable(hideTab, showTab) {
      if (!hideTab) {
        throw new TypeError(
          `Аттрибут кнопки закрытия заполнен некорректно или отсутствует, проверьте наличие и правильность заполнения.
          hideTab: ${hideTab}`,
        );
      }
      if (!showTab) {
        throw new TypeError(`Аттрибут кнопки открытия заполнен некорректно или отсутствует, проверьте наличие и правильность заполнения.
        showTab: ${showTab}`);
      }
    }
    function getRndInteger(min, max) {
      return Math.floor(Math.random() * (max - min + 1)) + min;
    }
  },

  // initMailForms: (options = {}) => {
  //   const {form = null, btnSubmit = null, tabClass = null} = options
  //   let isChecked = true;
  //   const tabs = form.querySelectorAll(tabClass)
  //   const childInfo = form.querySelector('.form__group--additional')

  //   const togglerClick = (e) => {
  //     const isAdult = e.currentTarget.dataset.tab === 'adult'
  //     if (isAdult && childInfo) return childInfo.classList.add('hide')
  //   }
  //   const handleClick = (e) => {
  //     e.preventDefault();
  //     const inputs = Array.from(form.querySelectorAll('input'))
  //     isChecked = inputs.forEach(input => {
  //       if (input.type === 'checkbox') {
  //         if (!input.checked) return isChecked = false
  //       } else {
  //         console.log(input.value.length);
  //         if (input.value.length) return isChecked = false
  //       }
  //     })
      
  //     if (isChecked) return alert('Форма успешна отправлена')
  //     alert('Проверьте правильность формы')
  //   }

  //   if (form && btnSubmit) {
  //     btnSubmit.addEventListener('click', handleClick)
  //   }
  //   if (tabs) {
  //     tabs.forEach(tab => tab.addEventListener('click', togglerClick))
  //   }
  // }
};

export const toggleClass = helpers.toggleClass;
export const initMailForms = helpers.initMailForms;

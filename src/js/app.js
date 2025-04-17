import { TabManager } from './modules/tabs-manager.js';
import { toggleClass } from './modules/helpers.js';
import { initMailForms } from './modules/helpers.js';
import { Popup } from './modules/popup.js';

import Swiper, { Thumbs, A11y, Keyboard, Navigation } from 'swiper';
import 'swiper/css';
import 'swiper/css/a11y';
import 'swiper/css/keyboard';

/* Функция инициации слайдеров */
function initSwiperSliders(selector, options = {}) {
  const elements = document.querySelectorAll(selector);

  elements.forEach((el) => {
    let slider = new Swiper(selector, options);
  });
}

/* Вкл./выкл. слайдер на брейкпоинте */
function sliderStateSwitcher(slider) {
  return function (e) {
    if (e.matches) {
      slider.destroy(false, true);
    } else {
      slider.init();
    }
  };
}

document.addEventListener('DOMContentLoaded', () => {
  /* Иниц. форм */
  initMailForms({
    /* data-${formSelectorAttribute}="${formSelectorName}" */
    /* 1. Аттрибут формы(аналогичный ставим в хтмл) */
    formSelectorAttribute: 'form',
    /* 2. Название формы(value аттрибута, аналогичное ставим в хтмл) */
    formSelectorName: 'trial-form',

    /* [data-${buttonStateAttribute}=${closeButtonName}] */
    /* [data-${buttonStateAttribute}=${openButtonName}] */

    /* 3. Аттрибут состояния кнопки */
    buttonStateAttribute: 'state-fields',
    /* 4, 5. Название кнопок открытия закрытия(value аттрибута, аналогичное ставим в хтмл, сделано только 2 кнопки откр./закр.) */
    closeButtonName: 'hide',
    openButtonName: 'show',
    /* 6. Селектор контейнера, который прячем(Прячу блок с доп. полями) */
    hidingFieldsContainer: '.form__group--additional',
    /* 7. Класс для скрытия эл-та */
    hideClass: 'hide',
  });
  /* Переключатель моб. меню */
  toggleClass({
    triggerSelector: '.main-nav__trigger',
    eTargetSelector: '.main-nav__dropdown',
    toggleClass: 'open',
    triggerToggle: true,
    aria: {
      enable: true,
      initText: 'Открыть меню',
      onChangeText: 'Закрыть меню',
    },
  });

  /* Popup */
  const trialPopup = new Popup({
    popupId: 'trial', //id попапа
    triggerAttributeName: 'trigger-for',
    //чтобы искать активный попап ('popupSelector + openSelector')
    popupSelector: '.popup',
    popupCloseSelector: '.popup__close',
    popupOutsideAreaSelector: '.popup__inner',
    openSelector: 'open',
    //название класса, при наличии которого в хтмл блокируется скролл
    lockPaddingSelector: '.lock-padding',
    //должен быть равен скорости анимации
    timeout: 300,
    // isChanged: (qqq) => {
    //   if (trialPopup.isOpen) {
    //     console.log('qqq');
    //   }
    // },
  });

  /* Tabs */
  const mainTabs = new TabManager('prices-tabs', {
    tabListSelector: '.prices__tabs',
    tabBtnSelector: '.prices__button',
    tabPanelSelector: '.prices__rates',

    tabActiveClass: 'active',
    panelActiveClass: 'show',
  });

  const onlineRatesTabs = new TabManager('prices-online-tabs', {
    tabListSelector: '.prices__tabs',
    tabBtnSelector: '.prices__button',
    tabPanelSelector: '.prices__rates-group',

    tabActiveClass: 'active',
    panelActiveClass: 'show',
  });

  const offlineRatesTabs = new TabManager('prices-offline-tabs', {
    tabListSelector: '.prices__tabs',
    tabBtnSelector: '.prices__button',
    tabPanelSelector: '.prices__rates-group',

    tabActiveClass: 'active',
    panelActiveClass: 'show',
  });

  /* Sliders */
  const historyNavLineSlider = new Swiper('.history__nav-line', {
    modules: [A11y, Keyboard],
    a11y: true,
    keyboard: true,
    slidesPerView: 'auto',
    spaceBetween: 60,
  });
  const historySlider = new Swiper('.slider-history', {
    modules: [Thumbs],
    thumbs: {
      swiper: historyNavLineSlider,
    },
    spaceBetween: 50,
  });

  /* Result section slider */
  const mediaQuery = window.matchMedia('(min-width: 768px)');

  const resultSectionSlider = new Swiper('.result .swiper', {
    init: false,
    spaceBetween: 20,
    slidesPerView: 1.2,
    breakpoints: {
      400: {
        slidesPerView: 1.5,
      },
      480: {
        slidesPerView: 1.6,
      },
      576: {
        slidesPerView: 1.8,
      },
      620: {
        slidesPerView: 2.2,
      },
      680: {
        slidesPerView: 2.4,
      },
    },
  });

  if (!mediaQuery.matches) {
    resultSectionSlider.init();
  }

  const sliderStateSwitcherHandler = sliderStateSwitcher(resultSectionSlider);

  mediaQuery.addEventListener('change', sliderStateSwitcherHandler);

  /* Price cards sliders */
  initSwiperSliders('.prices__rates-group', {
    spaceBetween: 20,
    breakpoints: {
      440: {
        slidesPerView: 1.5,
      },
      500: {
        slidesPerView: 1.7,
      },
      576: {
        slidesPerView: 1.8,
      },
      620: {
        slidesPerView: 2,
      },
      680: {
        slidesPerView: 2.3,
      },
      768: {
        slidesPerView: 2.5,
      },
      850: {
        slidesPerView: 2.7,
      },
      992: {
        slidesPerView: 2.6,
      },
      1024: {
        slidesPerView: 3,
        spaceBetween: 30,
      },
      1300: {
        slidesPerView: 3,
        spaceBetween: 70,
      },
    },
  });

  // Slider teachers
  initSwiperSliders('.teachers__slider .swiper', {
    spaceBetween: 20,
    modules: [Navigation],
    navigation: {
      nextEl: '.teachers__slider .swiper-button-next',
      prevEl: '.teachers__slider .swiper-button-prev',
    },
    breakpoints: {
      440: {
        slidesPerView: 1.5,
      },
      500: {
        slidesPerView: 1.7,
      },
      576: {
        slidesPerView: 1.8,
      },
      620: {
        slidesPerView: 2,
      },
      680: {
        slidesPerView: 2.3,
      },
      768: {
        slidesPerView: 2.5,
      },
      850: {
        slidesPerView: 2.7,
      },
      992: {
        slidesPerView: 2.6,
      },
      1024: {
        slidesPerView: 3,
        spaceBetween: 30,
      },
      1300: {
        slidesPerView: 3,
        spaceBetween: 70,
      },
    },
  })

  // Slider feedback
  initSwiperSliders('.feedback__slider .swiper', {
    spaceBetween: 32,
    modules: [Navigation],
    navigation: {
      nextEl: '.feedback__slider .swiper-button-next',
      prevEl: '.feedback__slider .swiper-button-prev',
    },
    breakpoints: {
      440: {
        slidesPerView: 1.5,
        spaceBetween: 12,
      },
      500: {
        slidesPerView: 1.7,
      },
      576: {
        slidesPerView: 1.8,
      },
      620: {
        slidesPerView: 2,
      },
      680: {
        slidesPerView: 2.3,
      },
      768: {
        slidesPerView: 2.5,
      },
      850: {
        slidesPerView: 2.7,
      },
      992: {
        slidesPerView: 2.6,
        spaceBetween: 16,
      },
      1024: {
        slidesPerView: 3,
        spaceBetween: 24,
      },
      1300: {
        slidesPerView: 3,
        spaceBetween: 32,
      },
    },
  })
});


// расписание занятий
document.addEventListener('DOMContentLoaded', function() {
  const tabs = document.querySelectorAll('.tab');
  
  tabs.forEach(tab => {
      tab.addEventListener('click', () => {
          // Удаляем активный класс у всех табов
          tabs.forEach(t => t.classList.remove('active'));
          
          // Добавляем активный класс текущему табу
          tab.classList.add('active');
          
          // Скрываем все контенты
          document.querySelectorAll('.tab-content').forEach(content => {
              content.classList.remove('active');
          });
          
          // Показываем нужный контент
          const tabId = tab.getAttribute('data-tab');
          document.getElementById(tabId).classList.add('active');
      });
  });
});
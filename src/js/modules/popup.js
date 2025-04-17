export class Popup {
  constructor(options = {}) {
    let defaultOptions = {
      isChanged: () => {},
    };

    const {
      popupId = null,
      triggerAttributeName = 'trigger-for',
      popupSelector = '.popup',
      popupCloseSelector = '.popup-close',
      popupOutsideAreaSelector = null,
      openSelector = 'open',
      linkAttributeKey = 'data-popup-id',
      lockPaddingSelector = '.lock-padding',
      timeout = 0,
    } = options;

    this.options = Object.assign(defaultOptions, options);

    this.popupId = popupId;
    this.triggerAttributeName = `data-` + triggerAttributeName;

    //Берем все кнопки с аатрибутом равным ID попапа
    this.popupTriggers = document.querySelectorAll(`[${this.triggerAttributeName}="${popupId}"]`);

    this.popupSelector = popupSelector;
    this.popupCloseSelector = popupCloseSelector;
    this.openSelector = openSelector;
    this.popupOutsideAreaSelector = popupOutsideAreaSelector;
    this.linkAttributeKey = linkAttributeKey;
    this.lockPadding = document.querySelectorAll(lockPaddingSelector);

    this.body = document.querySelector('body');
    this.unlock = true;

    this.timeout = timeout;

    this.check();
    this.init();
  }

  check() {
    if (!this.popupTriggers.length) {
      throw new TypeError(`
        Проверьте наличие аттрибутов кнопки открытия попапа и ID попапа в документе, а также их совпадение со значениями аттрибутов передаваемых в параметрах. 
        Текущее значение параметров:
          "triggerAttributeName": ${this.triggerAttributeName} ,
          "popupId": ${this.popupId} ,
      `);
    }
  }

  init() {
    this.popupTriggers.forEach((el) => {
      el.addEventListener('click', (e) => {
        if (el.tagName === 'A') {
          e.preventDefault();
        }

        const currentPopup = document.getElementById(this.popupId);

        this.popupOpen(currentPopup);
      });
    });
  }

  popupOpen(popup) {
    if (popup && this.unlock) {
      const popupActive = document.querySelector(this.popupSelector + '.' + this.openSelector);
      if (popupActive) {
        this.popupClose(popupActive, false);
      } else {
        this._bodyLock();
      }

      popup.classList.add(this.openSelector);

      let handler = (e) => {
        if (!e.target.closest(this.popupOutsideAreaSelector)) {
          popup.removeEventListener('click', handler);
          this.popupClose(popup);
        }
        const closeButtonList = popup.querySelectorAll(this.popupCloseSelector);

        closeButtonList.forEach((el) => {
          if (el === e.target) {
            popup.removeEventListener('click', handler);
            this.popupClose(popup);
          }
        });
      };
      popup.addEventListener('click', handler);

      // this.options.isChanged(this);
    }
  }

  popupClose(popup, doUnlock = true) {
    // console.log(this.unlock);
    // if (this.unlock) {
    popup.classList.remove(this.openSelector);
    if (doUnlock) {
      this._bodyUnlock();
    }
    // console.log(this.unlock);
    // }
  }

  _scrollBarWidth(withPx = false) {
    let documentWidth = Math.round(document.documentElement.clientWidth);
    let windowsWidth = Math.round(window.innerWidth);
    let scrollbarWidth = windowsWidth - documentWidth;

    if (withPx) {
      return scrollbarWidth + 'px';
    } else {
      return scrollbarWidth;
    }
    // return scrollbarWidth;
  }

  _bodyLock() {
    if (this.lockPadding.length > 0) {
      for (let index = 0; index < this.lockPadding.length; index++) {
        const el = this.lockPadding[index];
        el.style.paddingRight = this._scrollBarWidth(true);
      }
    }

    this.body.style.paddingRight = this._scrollBarWidth(true);
    this.body.style.overflow = 'hidden';

    this.unlock = false;

    setTimeout(function () {
      this.unlock = true;
    }, this.timeout);
  }

  _bodyUnlock() {
    setTimeout(() => {
      if (this.lockPadding.length > 0) {
        for (let index = 0; index < this.lockPadding.length; index++) {
          const el = this.lockPadding[index];
          el.style.paddingRight = '0px';
        }
      }
      this.body.style.paddingRight = '0px';
      this.body.style.overflow = '';
    }, this.timeout);

    this.unlock = false;

    setTimeout(() => {
      this.unlock = true;
    }, this.timeout);
  }
}

//todo при размещении кнопки открытия попапа в еще одеом попапе (множественные модалки), некорректно работает, нужно разьираться и допиливать

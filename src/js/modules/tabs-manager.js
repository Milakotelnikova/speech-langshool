export class TabManager {
  constructor(selector, options = {}) {
    let defaultOptions = {
      isChanged: () => {},
    };

    const {
      tabListSelector = null,
      tabBtnSelector = null,
      tabPanelSelector = null,

      tabActiveClass = 'active',
      panelActiveClass = 'active',
    } = options;

    this.options = Object.assign(defaultOptions, options);

    this.selector = selector;

    this.tabs = document.querySelector(`[data-tabs="${selector}"]`);

    this.tabActiveClass = tabActiveClass;
    this.panelActiveClass = panelActiveClass;

    if (this.tabs) {
      this.tabList = this.tabs.querySelector(tabListSelector);
      this.tabsBtns = this.tabList.querySelectorAll(tabBtnSelector);
      this.tabsPanels = this.tabs.querySelectorAll(tabPanelSelector);
    } else {
      // console.error('Селетор data-tabs не существует');
      return;
    }

    this.check();

    this.init();

    this.events();
  }

  check() {
    if (document.querySelectorAll(`[data-tabs="${this.selector}"]`).length > 1) {
      console.error('Количество элементов с одинаковым data-tabs больше одного');
      return;
    }

    if (this.tabsBtns.length !== this.tabsPanels.length) {
      console.error(
        `Количество кнопок и элементов табов не совпадает.
        Табы: `,
        this.tabsPanels,
        ` Кнопки табов: `,
        this.tabsBtns
      );
      return;
    }
  }

  init() {
    this.tabList.setAttribute('role', 'tablist');

    this.tabsBtns.forEach((el, idx) => {
      el.setAttribute('role', 'tab');
      el.setAttribute('tabindex', '-1');
      el.setAttribute('id', `${this.selector}-${idx + 1}`);
      el.classList.remove(this.tabActiveClass);
    });

    this.tabsPanels.forEach((el, idx) => {
      el.setAttribute('role', 'tabpanel');
      el.setAttribute('tabindex', '-1');
      el.setAttribute('aria-labelledby', this.tabsBtns[idx].id);
      el.classList.remove(this.panelActiveClass);
    });

    this.tabsBtns[0].classList.add(this.tabActiveClass);
    this.tabsBtns[0].removeAttribute('tabindex');
    this.tabsBtns[0].setAttribute('aria-selected', 'true');

    this.tabsPanels[0].classList.add(this.panelActiveClass);
  }

  events() {
    this.tabsBtns.forEach((el, idx) => {
      el.addEventListener('click', (e) => {
        let currentTab = this.tabList.querySelector('[aria-selected]');

        if (e.currentTarget !== currentTab) {
          this.switchTabs(e.currentTarget, currentTab);
        }
      });

      el.addEventListener('keydown', (e) => {
        let index = Array.prototype.indexOf.call(this.tabsBtns, e.currentTarget);

        let dir = null;

        //key left
        if (e.which === 37) {
          dir = index - 1;
          //key right
        } else if (e.which === 39) {
          dir = index + 1;
          //key down
        } else if (e.which === 40) {
          dir = 'down';
        }

        if (dir === null) return;

        if (dir === 'down') {
          this.tabsPanels[idx].focus();
        } else if (this.tabsBtns[dir]) {
          this.switchTabs(this.tabsBtns[dir], e.currentTarget);
        }
      });
    });
  }

  switchTabs(newTab, oldTab = this.tabs.querySelector('[aria-selected]')) {
    newTab.focus();
    newTab.removeAttribute('tabindex');
    newTab.setAttribute('aria-selected', 'true');

    oldTab.removeAttribute('aria-selected');
    oldTab.setAttribute('tabindex', '-1');

    let idx = Array.prototype.indexOf.call(this.tabsBtns, newTab);
    let oldIdx = Array.prototype.indexOf.call(this.tabsBtns, oldTab);

    this.tabsPanels[oldIdx].classList.remove(this.panelActiveClass);
    this.tabsPanels[idx].classList.add(this.panelActiveClass);

    this.tabsBtns[oldIdx].classList.remove(this.tabActiveClass);
    this.tabsBtns[idx].classList.add(this.tabActiveClass);

    this.options.isChanged(this);
  }
}

export async function initTrialForm() {
    console.log('=== ИНИЦИАЛИЗАЦИЯ ФОРМЫ ===');
  
    const formPopup = document.getElementById('form-popup'); // форма в попапе
    const formPage = document.getElementById('trial-form'); // форма на странице
    
    if (!formPopup && !formPage) {
      console.error('Формы не найдены!');
      return;
    }
  
    const csrfToken = document.cookie.match(/csrftoken=([^;]+)/)?.[1] || 
                    document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    if (!csrfToken) {
      console.error('Ошибка соединения с сервером.');
      return;
    }
  
  
    // загрузка курсов
    let coursesSelectOriginalHTML = '';
    try {
      const res = await fetch('http://localhost:8000/api/courses/categories/');
      if (res.ok) {
        const { results } = await res.json();
        coursesSelectOriginalHTML = 
          '<option value="" disabled selected>Выберите курс</option>' +
          results.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
      }
    } catch (err) {
      console.error('Ошибка загрузки курсов:', err);
    }
  
    const initForm = (form) => {
      if (!form || form.dataset.initialized === 'true') return;
      form.dataset.initialized = 'true';
  
      const isPopup = form.id === 'form-popup';
      const button = form.querySelector('[type="submit"]');
      const courseSelect = isPopup 
        ? form.querySelector('#lang-popup') 
        : form.querySelector('#lang');
      const childFields = form.querySelector('.form__group--additional');
      const forWhomRadios = form.querySelectorAll('[name="for-whom"]');
  
      if (!button || !courseSelect || !childFields) {
        console.error('Не найдены элементы формы:', {form, button, courseSelect, childFields});
        return;
      }
  
      // заполнение select курсами
      if (coursesSelectOriginalHTML) {
        courseSelect.innerHTML = coursesSelectOriginalHTML;
        courseSelect.setAttribute('required', '');
      }
  
      // обработчик переключения "Взрослые/Дети"
      forWhomRadios.forEach(radio => {
        radio.addEventListener('change', () => {
          const showChildFields = radio.dataset.stateFields === 'show';
          childFields.classList.toggle('hide', !showChildFields);
          childFields.querySelectorAll('input').forEach(input => {
            input.required = showChildFields;
          });
        });
      });
  
      // Обработчик телефона
      const phoneInput = form.querySelector('[name="phone"]');
      if (phoneInput) {
        phoneInput.addEventListener('input', (e) => {
          let val = e.target.value;
          val = val.replace(/[^\d+]/g, '');
          if (val.indexOf('+') > 0) val = val.replace(/\+/g, '');
          if (val.length > 0 && val[0] !== '+') val = val.replace(/\+/g, '');
          if (val.length > 17) val = val.slice(0, 17);
          e.target.value = val;
        });
      }
  
      // Обработчик отправки формы
      form.addEventListener('submit', async (e) => {
        e.preventDefault();
      
        form.querySelectorAll('.form-error').forEach(el => el.textContent = '');
      
        if (!form.checkValidity()) {
          form.reportValidity();
          return;
        }
      
        const originalText = button.value;
        button.value = 'Отправляю...';
        button.disabled = true;
      
      
  
        const isChild = form.querySelector('[name="for-whom"]:checked')?.dataset.stateFields === 'show';
        const data = {
          course_id: parseInt(courseSelect.value, 10),
          study_type: form.querySelector('[name="where-study"]:checked').id.split('-')[0],
          name: form.querySelector('[name="name"]').value.trim(),
          phone: form.querySelector('[name="phone"]').value.trim(),
          email: form.querySelector('[name="email"]').value.trim(),
          child_name: isChild ? form.querySelector('[name="child_name"]').value.trim() : null,
          child_age: isChild ? parseInt(form.querySelector('[name="child_age"]').value.trim(), 10) : null
        };
  
        try {
          const resp = await fetch('http://localhost:8000/api/applications/apply/', {
            method: 'POST',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data)
          });
  
  
          // модальное окно после отправки формы
          const modal = document.getElementById('thank-you-modal');
          if (modal) {
            modal.style.display = 'flex';
            modal.addEventListener('click', function closeModal(e) {
              if (e.target === modal) {
                modal.style.display = 'none';
                modal.removeEventListener('click', closeModal);
              }
            });
          }
  
          // сброс формы
          form.reset();
          if (courseSelect) {
            courseSelect.innerHTML = coursesSelectOriginalHTML;
            courseSelect.value = '';
          }
  
        } catch (err) {
          console.error('Ошибка отправки:', err);
          alert('Не удалось отправить форму. Пожалуйста, попробуйте позже.');
        } finally {
          button.disabled = false;
          button.value = originalText;
        }
      });
    };
  
    // инициалищация форм
    initForm(formPopup);
    initForm(formPage);
  
    console.log('=== ФОРМЫ ГОТОВЫ ===');
  }
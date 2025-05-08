document.addEventListener('DOMContentLoaded', async function () {
  if (!document.getElementById('lessonsContainer')) {
    return;
  }
  const API_URL = 'http://localhost:8000/api/courses/lessons/';
  const ENROLLMENT_API_URL = 'http://localhost:8000/api/courses/enrollments/';
  const modalOverlay = document.getElementById('modalOverlay');
  const confirmCancel = document.getElementById('confirmCancel');
  const closeModal = document.getElementById('closeModal');
  const lessonsContainer = document.getElementById('list1');
  let currentEnrollmentId = null;

  const appointments = {}; // lesson.id => { button, enrollmentId, status }

  function getCSRFToken() {
    return document.cookie
      .split('; ')
      .find(row => row.startsWith('csrftoken='))
      ?.split('=')[1] || '';
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function formatDateTime(datetime) {
    const date = new Date(datetime);
    return date.toLocaleString('ru-RU', {
      day: '2-digit', month: '2-digit', year: 'numeric',
      hour: '2-digit', minute: '2-digit'
    });
  }

  function createLessonCard(lesson, enrolled, status, enrollmentId) {
    const name = escapeHtml(lesson.name);
    const desc = escapeHtml(lesson.description);
    const teacher = escapeHtml(lesson.teacher_name);
    const location = escapeHtml(lesson.location);
    const start = formatDateTime(lesson.start_time);
    const end = formatDateTime(lesson.end_time);

    let buttonText = '';
    let disabledAttr = '';
    let buttonClass = '';

    if (lesson.is_full && !enrolled) {
      buttonText = 'Занятие заполнено';
      disabledAttr = 'disabled';
      buttonClass = 'appointment-button disabled';
    } else if (enrolled) {
      const statusText =
        status === 'pending' ? 'Ожидает' :
        status === 'confirmed' ? 'Подтверждено' :
        'Отменено';
      buttonText = `Статус: ${statusText}`;
      buttonClass = 'appointment-button cancel';
    } else {
      buttonText = 'Записаться';
      buttonClass = 'appointment-button register';
    }

    return `
      <div class="card">
        <h2 class="card__title">${name}</h2>
        <p class="card__content">Описание: ${desc}</p>
        <p class="card__content">Преподаватель: ${teacher}</p>
        <p class="card__content">${start} — ${end}</p>
        <p class="card__content">Место: ${location}</p>
        <p class="card__content">Осталось мест: ${lesson.available_seats}</p>
        <div class="appointment-container" data-id="${lesson.id}" data-enrollment-id="${enrollmentId || ''}">
          <a class="${buttonClass} btn btn--size-normal btn--purple" ${disabledAttr} >${buttonText}</a>
        </div>
      </div>
    `;
  }

  async function fetchLessons() {
    const res = await fetch(API_URL, { credentials: 'include' });
    if (!res.ok) throw new Error('Ошибка загрузки занятий');
    const data = await res.json();
    return data.results;  // <-- получаем масив занятий
  }
  

  async function fetchEnrollments() {
    const res = await fetch(ENROLLMENT_API_URL, { credentials: 'include' });
    if (!res.ok) throw new Error('Ошибка загрузки записей');
    const data = await res.json();
    return data.results; // получаем масив записей
  }
  
  async function displayMyEnrollments() {
    const container = document.getElementById('myEnrollmentsContainer');
    const loading = document.getElementById('loadingMyEnrollments');
    const error = document.getElementById('errorMyEnrollments');
  
    container.innerHTML = '';
    loading.style.display = 'block';
    error.style.display = 'none';
  
    try {
      const enrollments = await fetchEnrollments();
  
      if (!enrollments.length) {
        container.innerHTML = '<p>У вас нет записей</p>';
        return;
      }
  
      for (const enrollment of enrollments) {
        const lesson = enrollment.lesson;
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = createLessonCard(lesson, true, enrollment.status, enrollment.id);
        container.appendChild(card);
  
        const button = card.querySelector('.appointment-button');
        button.addEventListener('click', () => {
          currentEnrollmentId = enrollment.id;
          modalOverlay.style.display = 'flex';
        });
      }
    } catch (err) {
      console.error(err);
      error.style.display = 'block';
      error.textContent = 'Ошибка при загрузке записей.';
    } finally {
      loading.style.display = 'none';
    }
  }
  

  async function displayLessons() {
    const lessons = await fetchLessons();
    const enrollments = await fetchEnrollments();

    lessonsContainer.innerHTML = '';
    if (!lessons.length) {
      lessonsContainer.innerHTML = '<p>Нет доступных занятий</p>';
      return;
    }

    for (const lesson of lessons) {
      const enrollment = enrollments.find(e => e.lesson.id === lesson.id);
      const enrolled = Boolean(enrollment);
      const status = enrollment?.status || null;
      const enrollmentId = enrollment?.id || null;

      const card = document.createElement('div');
      card.className = 'card';
      card.innerHTML = createLessonCard(lesson, enrolled, status, enrollmentId);
      lessonsContainer.appendChild(card);

      const button = card.querySelector('.appointment-button');
      appointments[lesson.id] = { button, enrollmentId, status };

      button.addEventListener('click', () => {
        if (!enrolled && !(lesson.is_full)) {
          enrollToLesson(lesson.id);
        } else if (enrolled) {
          currentEnrollmentId = enrollmentId;
          modalOverlay.style.display = 'flex';
        }
      });
    }
  }

  async function enrollToLesson(lessonId) {
    try {
      const res = await fetch(ENROLLMENT_API_URL, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({ lesson_id: lessonId, child_id: null }),
      });

      if (!res.ok) throw new Error('Не удалось записаться на занятие');
      await displayLessons();
      await displayMyEnrollments();
    } catch (err) {
      alert(err.message);
    }
  }

  async function cancelEnrollment(enrollmentId) {
    try {
        const res = await fetch(`${ENROLLMENT_API_URL}${enrollmentId}/`, {
            method: 'DELETE',
            credentials: 'include',
            headers: {
                'X-CSRFToken': getCSRFToken(),
            },
        });

        if (!res.ok) throw new Error('Не удалось отменить запись');

        await displayLessons();
        await displayMyEnrollments();
    } catch (err) {
        alert(err.message);
    }
}


  confirmCancel?.addEventListener('click', async () => {
    if (currentEnrollmentId) {
      await cancelEnrollment(currentEnrollmentId);
      modalOverlay.style.display = 'none';
    }
  });

  closeModal?.addEventListener('click', () => {
    modalOverlay.style.display = 'none';
  });

  modalOverlay?.addEventListener('click', (e) => {
    if (e.target === modalOverlay) {
      modalOverlay.style.display = 'none';
    }
  });

  await displayLessons();
  await displayMyEnrollments();

});

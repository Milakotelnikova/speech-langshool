document.addEventListener('DOMContentLoaded', async () => {
  const form = document.getElementById('loginForm');
  if (!form) return;

  const errorDiv = document.getElementById('login-error');
  const loginMessageDiv = document.getElementById('login-message');

  // csrf токен
  async function getCSRFToken() {
      try {
          const response = await fetch('http://localhost:8000/api/accounts/csrf/', {
              credentials: 'include'
          });
          if (!response.ok) throw new Error('CSRF request failed');
          return response.headers.get('X-CSRFToken') || 
                 document.cookie.match(/csrftoken=([^;]+)/)?.[1];
      } catch (error) {
          console.error('CSRF error:', error);
          return null;
      }
  }

  form.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    errorDiv.textContent = '';
    loginMessageDiv.textContent = '';
    
    const email    = form.querySelector('input[name="email"]').value.trim();
    const password = form.querySelector('input[name="password"]').value;
  
    try {
      const csrfToken = await getCSRFToken();
      if (!csrfToken) throw new Error('Ошибка соединения с сервером.');
  
      const response = await fetch('http://localhost:8000/api/accounts/login/', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ email, password })
      });
  
      const payload = await response.json();
  
      if (!response.ok) {
        const message = payload.detail 
          ? payload.detail 
          : Object.values(payload).flat().join(' | ');
        throw new Error(message);
      }
  
      // информационное сообщение
      loginMessageDiv.style.color = 'green';
      loginMessageDiv.textContent = 'Вы успешно вошли! Перенаправляем…';
  
      // редирект через полсекунды
      setTimeout(() => {
        window.location.href = '/';
      }, 500);
  
    } catch (err) {
      errorDiv.textContent = err.message;
    }
  });
  

});
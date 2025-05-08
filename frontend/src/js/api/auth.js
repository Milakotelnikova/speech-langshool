document.addEventListener('DOMContentLoaded', () => {
  initializeAuth();
});

async function initializeAuth() {
  try {
    const isAuth = await checkAuthWithAPI();
    updateAuthButtons(isAuth);
    setupAuthInterceptors();
  } catch (error) {
    console.error('Auth initialization failed:', error);
    updateAuthButtons(false);
  }
}

// обновление кнопок авторизации
function updateAuthButtons(isAuthenticated) {
  const desktopButton = document.getElementById('authButtonDesktop');
  const mobileButton = document.getElementById('authButtonMobile');
  const logoutDesktop = document.getElementById('logoutButton');
  const logoutMobile = document.getElementById('logoutButtonMobile');

  [desktopButton, mobileButton].forEach(button => {
    if (!button) return;

    if (isAuthenticated) {
      button.textContent = 'Мои уроки';
      button.href = 'lessons.html';
      button.onclick = null;
    } else {
      button.textContent = 'Войти';
      button.href = 'login.html';
    }

    button.classList.remove('hidden');
    button.classList.add('visible');
  });

  [logoutDesktop, logoutMobile].forEach(button => {
    if (!button) return;

    if (isAuthenticated) {
      button.style.display = 'block';
      button.classList.remove('hidden');
      button.onclick = async (e) => {
        e.preventDefault();
        await logout();
      };
    } else {
      button.style.display = 'none';
    }
  });
}




// Проверка авторизации через API
async function checkAuthWithAPI() {
  try {
    const response = await fetch('http://localhost:8000/api/accounts/profile/', {
      method: 'GET',
      credentials: 'include',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    });

    if (!response.ok) {
      throw new Error('Not authenticated');
    }
    
    return true;
  } catch (error) {
    return false;
  }
}

// перехватчик 403 
function setupAuthInterceptors() {
  const originalFetch = window.fetch;

  window.fetch = async function(resource, config = {}) {
    const method = (config.method || 'GET').toUpperCase();

    if (['POST', 'PUT', 'DELETE', 'PATCH'].includes(method)) {
      const headers = config.headers || {};
      headers['X-CSRFToken'] = getCookie('csrftoken');
      headers['X-Requested-With'] = 'XMLHttpRequest';
      config.headers = headers;
    }

    config.credentials = 'include';

    const response = await originalFetch(resource, config);

    if (response.status === 403) {
      window.location.href = '/login.html?next=' + encodeURIComponent(window.location.pathname);
      return Promise.reject(new Error('Forbidden'));
    }

    return response;
  };
}

// выход из системы
async function logout() {
  try {
    await fetch('http://localhost:8000/api/accounts/logout/', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      }
    });
  } finally {
    updateAuthButtons(false);
    window.location.href = '/';
  }
}

// csrf токен
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

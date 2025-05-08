document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('registerForm');
  const errorDiv = document.getElementById('form-error');
  
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
  
      const name = document.getElementById('name').value.trim();
      const phone = document.getElementById('phone').value.trim();
      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value;
      const passwordConfirm = document.getElementById('password_confirm').value;
      const accept = document.getElementById('accept').checked;
  
      errorDiv.textContent = "";
      errorDiv.style.color = "red";
  
      if (!accept) {
        errorDiv.textContent = "Вы должны согласиться с политикой конфиденциальности.";
        return;
      }
  
      // Проверка на совпадение паролей
      if (password !== passwordConfirm) {
        errorDiv.textContent = "Пароли не совпадают.";
        return;
      }
  
      fetch('http://localhost:8000/api/accounts/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: name,
          phone: phone,
          email: email,
          password: password,
          password_confirm: passwordConfirm
        })
      })
        .then(response => {
          return response.json().then(data => ({ ok: response.ok, data }));
        })
        .then(({ ok, data }) => {
          if (ok) {
            errorDiv.style.color = "green";
              window.location.href = '/';
          } else {
            errorDiv.textContent = formatErrors(data);
          }
        })
        .catch(() => {
          errorDiv.textContent = "Ошибка соединения с сервером.";
        });
  
      function formatErrors(errors) {
        return Object.entries(errors).map(([_, messages]) => {
          return Array.isArray(messages) ? messages.join(', ') : messages;
        }).join(' | ');
      }
    });
  }
});

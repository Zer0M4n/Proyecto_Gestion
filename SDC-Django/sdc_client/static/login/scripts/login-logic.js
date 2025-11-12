document.getElementById('login-form').addEventListener('submit', async function(e) {
            e.preventDefault(); // Evita el envío tradicional del formulario
            
            const email = document.getElementById('email-input').value;
            const password = document.getElementById('password-input').value;
            const errorP = document.getElementById('error-message');
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            errorP.textContent = ''; // Limpia errores previos

            try {
                const response = await fetch('/api/login/', { // Llama a tu nueva API
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    // ¡Éxito! Guarda los tokens
                    localStorage.setItem('accessToken', data.access);
                    localStorage.setItem('refreshToken', data.refresh);
                    
                    // Redirige al feed correspondiente
                    window.location.href = data.user.redirect_url;
                } else {
                    // Muestra el error (ej. "Credenciales inválidas")
                    errorP.textContent = data.error || 'Error al iniciar sesión.';
                }

            } catch (error) {
                console.error('Error de red:', error);
                errorP.textContent = 'Error de conexión. Inténtalo de nuevo.';
            }
        });
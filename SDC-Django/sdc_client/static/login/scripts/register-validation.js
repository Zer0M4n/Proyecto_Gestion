document.addEventListener("DOMContentLoaded", () => {
    
    // --- Regex para validación ---
    const REGEX = {
        noNumbers: /^[a-zA-Z\s]+$/,
        onlyNumbers: /^\d+$/,
        email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
        curp: /^[A-ZÑ][AEIOU][A-ZÑ]{2}[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])[HM](AS|BC|BS|CC|CS|CH|CL|CM|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS)[B-DF-HJ-NP-TV-ZÑ]{3}[A-Z0-9][0-9]$/,
        rfc: /^[A-ZÑ]{4}[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])[A-Z0-9]{3}$|^[A-Z&Ñ]{3}[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])[A-Z0-9]{3}$/
    };

    // --- Función helper para mostrar feedback ---
    function showFeedback(element, message, isValid) {
        element.textContent = message;
        element.className = 'feedback-msg'; // Reset
        if (message) {
            element.classList.add(isValid ? 'valid' : 'invalid');
        }
    }

    // --- FORMULARIO PERSONA ---
    const formPerson = document.getElementById("form-person");
    if (formPerson) {
        const firstName = document.getElementById("id_person_first_name");
        const middleName = document.getElementById("id_person_middle_name");
        const firstSurname = document.getElementById("id_person_first_surname");
        const secondSurname = document.getElementById("id_person_second_surname");
        const curp = document.getElementById("id_person_curp");
        const email = document.getElementById("id_person_email");
        const phone = document.getElementById("id_person_phone");
        const password = document.getElementById("id_person_password");
        const confirmPassword = document.getElementById("id_confirm_person_password");
        
        const fnameFeedback = document.getElementById("fname-feedback");
        const mnameFeedback = document.getElementById("mname-feedback");
        const fsurnameFeedback = document.getElementById("fsurname-feedback");
        const ssurnameFeedback = document.getElementById("ssurname-feedback");
        const curpFeedback = document.getElementById("curp-feedback");
        const emailFeedback = document.getElementById("email-feedback");
        const phoneFeedback = document.getElementById("phone-feedback");
        const passwordFeedback = document.getElementById("password-feedback");
        const confirmPasswordFeedback = document.getElementById("confirm-password-feedback");
        const strengthBar = document.getElementById("password-strength-bar")?.querySelector('.bar');

        // Validar Nombres (sin números)
        firstName?.addEventListener("input", () => {
            const valid = REGEX.noNumbers.test(firstName.value);
            showFeedback(fnameFeedback, valid || !firstName.value ? "" : "El nombre no debe contener números.", valid);
        });
        middleName?.addEventListener("input", () => {
            const valid = REGEX.noNumbers.test(middleName.value);
            showFeedback(mnameFeedback, valid || !middleName.value ? "" : "El nombre no debe contener números.", valid);
        });
        firstSurname?.addEventListener("input", () => {
            const valid = REGEX.noNumbers.test(firstSurname.value);
            showFeedback(fsurnameFeedback, valid || !firstSurname.value ? "" : "El apellido no debe contener números.", valid);
        });
        secondSurname?.addEventListener("input", () => {
            const valid = REGEX.noNumbers.test(secondSurname.value);
            showFeedback(ssurnameFeedback, valid || !secondSurname.value ? "" : "El apellido no debe contener números.", valid);
        });

        // Validar Teléfono (solo números)
        phone?.addEventListener("input", () => {
            const valid = REGEX.onlyNumbers.test(phone.value);
            showFeedback(phoneFeedback, valid || !phone.value ? "" : "El teléfono debe contener solo números.", valid);
        });

        // Validar Email
        email?.addEventListener("input", () => {
            const valid = REGEX.email.test(email.value);
            showFeedback(emailFeedback, valid || !email.value ? "" : "Formato de correo no válido.", valid);
        });

        // Validar CURP
        curp?.addEventListener("input", () => {
            const valid = REGEX.curp.test(curp.value.toUpperCase());
            showFeedback(curpFeedback, valid || !curp.value ? "" : "Formato de CURP no válido.", valid);
        });

        // Validar Seguridad de Contraseña
        password?.addEventListener("input", () => {
            const value = password.value;
            let score = 0;
            if (value.length >= 8) score++;
            if (/[A-Z]/.test(value)) score++;
            if (/[a-z]/.test(value)) score++;
            if (/[0-9]/.test(value)) score++;
            if (/[^A-Za-z0-9]/.test(value)) score++;

            strengthBar.className = 'bar'; // Reset
            let feedbackMsg = "";

            if (value.length === 0) {
                // No mostrar nada si está vacío
            } else if (score <= 2) {
                strengthBar.classList.add('weak');
                feedbackMsg = "Contraseña débil.";
            } else if (score <= 4) {
                strengthBar.classList.add('medium');
                feedbackMsg = "Contraseña media.";
            } else {
                strengthBar.classList.add('strong');
                feedbackMsg = "Contraseña fuerte.";
            }
            showFeedback(passwordFeedback, feedbackMsg, score > 2);
            validatePasswordMatch(); // Re-validar la confirmación
        });

        // Validar Coincidencia de Contraseña
        function validatePasswordMatch() {
            if (!confirmPassword) return;
            const valid = password.value === confirmPassword.value;
            showFeedback(confirmPasswordFeedback, valid || !confirmPassword.value ? "" : "Las contraseñas no coinciden.", valid);
        }
        confirmPassword?.addEventListener("input", validatePasswordMatch);
    }

    // --- FORMULARIO INSTITUCIÓN ---
    const formInstitution = document.getElementById("form-institution");
    if (formInstitution) {
        const rfc = document.getElementById("id_institution_rfc");
        const email = document.getElementById("id_institution_email");
        const password = document.getElementById("id_institution_password");
        const confirmPassword = document.getElementById("id_confirm_institution_password");

        const rfcFeedback = document.getElementById("rfc-feedback");
        const emailFeedback = document.getElementById("inst-email-feedback");
        const passwordFeedback = document.getElementById("inst-password-feedback");
        const confirmPasswordFeedback = document.getElementById("inst-confirm-password-feedback");
        const strengthBar = document.getElementById("inst-password-strength-bar")?.querySelector('.bar');
        
        // Validar RFC
        rfc?.addEventListener("input", () => {
            const valid = REGEX.rfc.test(rfc.value.toUpperCase());
            showFeedback(rfcFeedback, valid || !rfc.value ? "" : "Formato de RFC no válido.", valid);
        });

        // Validar Email de Institución
        email?.addEventListener("input", () => {
            const valid = REGEX.email.test(email.value);
            showFeedback(emailFeedback, valid || !email.value ? "" : "Formato de correo no válido.", valid);
        });

        // Validar Seguridad de Contraseña de Institución
        password?.addEventListener("input", () => {
            const value = password.value;
            let score = 0;
            if (value.length >= 8) score++;
            if (/[A-Z]/.test(value)) score++;
            if (/[a-z]/.test(value)) score++;
            if (/[0-9]/.test(value)) score++;
            if (/[^A-Za-z0-9]/.test(value)) score++;

            strengthBar.className = 'bar'; // Reset
            let feedbackMsg = "";

            if (value.length === 0) {
                // No mostrar nada si está vacío
            } else if (score <= 2) {
                strengthBar.classList.add('weak');
                feedbackMsg = "Contraseña débil.";
            } else if (score <= 4) {
                strengthBar.classList.add('medium');
                feedbackMsg = "Contraseña media.";
            } else {
                strengthBar.classList.add('strong');
                feedbackMsg = "Contraseña fuerte.";
            }
            showFeedback(passwordFeedback, feedbackMsg, score > 2);
            validatePasswordMatch(); // Re-validar la confirmación
        });

        // Validar Coincidencia de Contraseña de Institución
        function validatePasswordMatch() {
            if (!confirmPassword) return;
            const valid = password.value === confirmPassword.value;
            showFeedback(confirmPasswordFeedback, valid || !confirmPassword.value ? "" : "Las contraseñas no coinciden.", valid);
        }
        confirmPassword?.addEventListener("input", validatePasswordMatch);
    }
});
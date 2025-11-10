(() => {
    let currentUser = null;

    document.addEventListener('DOMContentLoaded', async () => {
        try {
            if (!window.authAPI || !window.authAPI.isAuthenticated()) {
                window.location.href = '/login.html';
                return;
            }

            window.dispatchEvent(new Event('authChange'));
            await loadUserData();
            await loadCareerList();
            bindEvents();
        } catch (error) {
            console.error('Error inicializando perfil:', error);
            showAlert('No se pudo cargar la información del usuario', 'danger');
        }
    });

    async function loadUserData() {
        currentUser = await window.authAPI.getCurrentUser();
        updateProfileView();
    }

    async function loadCareerList() {
        try {
            const select = document.getElementById('editCareer');
            if (!select) return;

            select.innerHTML = '<option value="">Selecciona una carrera</option>';
            const carreras = await window.authAPI.getCarreras();
            carreras.forEach(career => {
                const option = document.createElement('option');
                option.value = career;
                option.textContent = career;
                select.appendChild(option);
            });
        } catch (error) {
            console.error('Error cargando carreras:', error);
        }
    }

    function bindEvents() {
        document.getElementById('editProfileBtn')?.addEventListener('click', enableEditMode);
        document.getElementById('cancelEditBtn')?.addEventListener('click', cancelEditMode);
        document.getElementById('saveProfileBtn')?.addEventListener('click', saveProfile);
        document.getElementById('verifyEmailBtn')?.addEventListener('click', resendVerification);
        document.getElementById('changePasswordBtn')?.addEventListener('click', changePassword);
    }

    function updateProfileView() {
        const name = currentUser.name || currentUser.email;
        const career = currentUser.career || 'Sin definir';
        const semestre = currentUser.semestre || '-';
        const campus = currentUser.campus_nombre || 'Sin asignar';
        const role = getRoleText(currentUser.role);

        document.querySelectorAll('[data-profile="name"]').forEach(el => el.textContent = name);
        document.getElementById('profileEmail')?.setAttribute('value', currentUser.email || '');
        document.getElementById('profileCareer')?.setAttribute('value', career);
        document.getElementById('profileSemester')?.setAttribute('value', semestre);
        document.getElementById('profileCampus')?.setAttribute('value', campus);
        document.getElementById('profileRole')?.setAttribute('value', role);

        const emailStatus = document.getElementById('emailStatus');
        const verifyBtn = document.getElementById('verifyEmailBtn');
        if (emailStatus) {
            if (currentUser.is_email_verified) {
                emailStatus.textContent = 'Tu correo está verificado';
                emailStatus.className = 'text-success';
                if (verifyBtn) verifyBtn.classList.add('d-none');
            } else {
                emailStatus.textContent = 'Tu correo no está verificado';
                emailStatus.className = 'text-warning';
                if (verifyBtn) verifyBtn.classList.remove('d-none');
            }
        }
    }

    function enableEditMode() {
        document.getElementById('editName')?.setAttribute('value', currentUser.name || '');
        const careerSelect = document.getElementById('editCareer');
        if (careerSelect) careerSelect.value = currentUser.career || '';
        document.getElementById('editSemester')?.setAttribute('value', currentUser.semestre || '');
        document.getElementById('editSection')?.classList.remove('d-none');
        document.getElementById('editName')?.focus();
    }

    function cancelEditMode() {
        document.getElementById('editSection')?.classList.add('d-none');
    }

    async function saveProfile() {
        const name = document.getElementById('editName')?.value.trim();
        const career = document.getElementById('editCareer')?.value;
        const semesterValue = document.getElementById('editSemester')?.value;
        const semester = semesterValue ? parseInt(semesterValue, 10) : null;

        if (!name || !career || !semester) {
            showAlert('Por favor completa todos los campos para actualizar tu perfil', 'warning');
            return;
        }

        try {
            await window.authAPI.updateProfile({ name, career, semestre: semester });
            showAlert('Perfil actualizado correctamente', 'success');
            await loadUserData();
            cancelEditMode();
        } catch (error) {
            console.error('Error actualizando perfil:', error);
            showAlert(error.message || 'No fue posible actualizar el perfil', 'danger');
        }
    }

    async function changePassword() {
        const currentPassword = document.getElementById('currentPassword')?.value;
        const newPassword = document.getElementById('newPassword')?.value;
        const confirmPassword = document.getElementById('confirmPassword')?.value;

        if (!currentPassword || !newPassword || !confirmPassword) {
            showAlert('Completa todos los campos de contraseña', 'warning');
            return;
        }

        if (newPassword !== confirmPassword) {
            showAlert('Las nuevas contraseñas no coinciden', 'warning');
            return;
        }

        try {
            await window.authAPI.changePassword(currentPassword, newPassword, confirmPassword);
            showAlert('Contraseña actualizada correctamente', 'success');
            ['currentPassword', 'newPassword', 'confirmPassword'].forEach(id => {
                const input = document.getElementById(id);
                if (input) input.value = '';
            });
        } catch (error) {
            console.error('Error cambiando contraseña:', error);
            showAlert(error.message || 'No fue posible cambiar la contraseña', 'danger');
        }
    }

    async function resendVerification() {
        try {
            if (!currentUser?.email) return;
            await window.authAPI.resendVerificationCode(currentUser.email);
            showAlert('Correo de verificación enviado. Revisa tu bandeja de entrada.', 'success');
        } catch (error) {
            console.error('Error enviando verificación:', error);
            showAlert(error.message || 'No fue posible reenviar el correo de verificación', 'danger');
        }
    }

    function getRoleText(role) {
        const roles = {
            student: 'Estudiante',
            moderator: 'Moderador',
            admin_global: 'Administrador'
        };
        return roles[role] || 'Estudiante';
    }

    function showAlert(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 1055; min-width: 280px;';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(alertDiv);
        setTimeout(() => alertDiv.remove(), 5000);
    }
})();


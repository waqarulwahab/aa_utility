/**
 * Authentication System JavaScript
 * Handles client-side functionality for the authentication system
 */

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Password strength indicator
    const passwordFields = document.querySelectorAll('input[type="password"]');
    
    passwordFields.forEach(function(field) {
        if (field.id.includes('password1') || field.id.includes('new_password1')) {
            // Create strength indicator
            const strengthIndicator = document.createElement('div');
            strengthIndicator.className = 'password-strength mt-2 mb-3';
            strengthIndicator.innerHTML = `
                <div class="progress" style="height: 5px;">
                    <div class="progress-bar" role="progressbar" style="width: 0%;" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
                </div>
                <small class="strength-text text-muted mt-1 d-block">Password strength: Too weak</small>
            `;
            
            field.parentNode.insertBefore(strengthIndicator, field.nextSibling);
            
            // Update strength on input
            field.addEventListener('input', function() {
                updatePasswordStrength(field.value, strengthIndicator);
            });
        }
    });

    // OTP input field enhancements
    const otpInput = document.querySelector('.otp-input');
    if (otpInput) {
        otpInput.addEventListener('input', function() {
            // Convert input to digits only
            this.value = this.value.replace(/\D/g, '');
            
            // Add visual feedback on entering OTP
            if (this.value.length === 6) {
                this.classList.add('is-valid');
            } else {
                this.classList.remove('is-valid');
            }
        });
        
        // Auto focus OTP input when page loads
        otpInput.focus();
    }
    
    // Profile picture preview
    const profilePicInput = document.querySelector('input[type="file"][name="profile_picture"]');
    if (profilePicInput) {
        profilePicInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    const profileImage = document.querySelector('.profile-image');
                    const profilePlaceholder = document.querySelector('.profile-image-placeholder');
                    
                    if (profileImage) {
                        profileImage.src = e.target.result;
                    } else if (profilePlaceholder) {
                        // Create image if only placeholder exists
                        const img = document.createElement('img');
                        img.src = e.target.result;
                        img.className = 'profile-image';
                        
                        const container = profilePlaceholder.parentNode;
                        container.removeChild(profilePlaceholder);
                        container.appendChild(img);
                    }
                };
                
                reader.readAsDataURL(this.files[0]);
            }
        });
    }
});

/**
 * Updates password strength indicator based on password value
 * @param {string} password - The password to evaluate
 * @param {HTMLElement} indicator - The strength indicator element
 */
function updatePasswordStrength(password, indicator) {
    const progressBar = indicator.querySelector('.progress-bar');
    const strengthText = indicator.querySelector('.strength-text');
    
    // Calculate strength
    let strength = 0;
    let feedback = 'Too weak';
    
    if (password.length >= 8) {
        strength += 25;
    }
    
    if (password.match(/[A-Z]/)) {
        strength += 25;
    }
    
    if (password.match(/[0-9]/)) {
        strength += 25;
    }
    
    if (password.match(/[^A-Za-z0-9]/)) {
        strength += 25;
    }
    
    // Update progress bar
    progressBar.style.width = strength + '%';
    progressBar.setAttribute('aria-valuenow', strength);
    
    // Set color based on strength
    if (strength <= 25) {
        progressBar.className = 'progress-bar bg-danger';
        feedback = 'Too weak';
    } else if (strength <= 50) {
        progressBar.className = 'progress-bar bg-warning';
        feedback = 'Weak';
    } else if (strength <= 75) {
        progressBar.className = 'progress-bar bg-info';
        feedback = 'Good';
    } else {
        progressBar.className = 'progress-bar bg-success';
        feedback = 'Strong';
    }
    
    // Update text
    strengthText.textContent = 'Password strength: ' + feedback;
}

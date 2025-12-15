document.getElementById('loginForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;
        const errorDiv = document.getElementById('login-error');
        // Demo: hardcoded username/password
        if(username === 'admin' && password === 'admin123') {
            document.getElementById('login-container').style.display = 'none';
            document.getElementById('main-content').style.display = '';
        } else {
            errorDiv.textContent = 'Invalid username or password!';
            errorDiv.style.display = 'block';
        }
    });
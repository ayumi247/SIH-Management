async function checkAuthStatus() {
    try {
        const user = await fetchAPI('/users/me');
        return user;
    } catch (error) {
        return null;
    }
}

async function logout() {
    try {
        await fetchAPI('/auth/logout', { method: 'POST' });
        localStorage.removeItem('access_token');
        // Redirect to root level index
        window.location.href = '../../index.html';
    } catch (error) {
        alert('Logout failed: ' + error.message);
    }
}

// Automatically check auth and enforce protection on dashboard pages
async function requireAuth(expectedRole = null) {
    const user = await checkAuthStatus();
    if (!user) {
        window.location.href = '../../index.html';
        return null;
    }
    
    if (expectedRole && user.role !== expectedRole) {
        alert('Unauthorized access');
        window.location.href = '../../index.html';
        return null;
    }
    return user;
}
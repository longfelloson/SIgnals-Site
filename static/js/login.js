async function loginUser() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const credentials = {
        email: email,
        password: password,
    }
    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(credentials)
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail.msg);
        }

        const data = await response.json();
        document.cookie = `access_token=${data.access_token}; path=/; SameSite=Lax`;
        window.location.href = '/';
    } catch (error) {
        alert(error.message);
    }
}


async function logoutUser() {
    await fetch("/logout", {
        method: 'POST',
    });
    window.location.href = '/';
}

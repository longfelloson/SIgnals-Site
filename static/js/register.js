async function registerUser() {
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const info = {
        username: username,
        password: password,
        email: email,
    }

    try {
        const response = await fetch("/register", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(info)
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

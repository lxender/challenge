document.getElementById("loginForm").addEventListener("submit", async e => {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const res = await fetch(`${BACKEND_URL}/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password }),
        credentials: "include"
    });

    if (res.ok) {
        window.location.href = "/dashboard.html";
    } else {
        alert("Invalid credentials");
    }
});
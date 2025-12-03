document.getElementById("registrationForm").addEventListener("submit", async e => {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const username = document.getElementById("username").value;

    const res = await fetch(`${BACKEND_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password, username })
    });

    if (res.ok) {
        window.location.href = "/index.html";
    } else {
        alert("Registration failed");
    }
});
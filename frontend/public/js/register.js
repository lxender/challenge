document.getElementById("registrationForm").addEventListener("submit", async e => {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const name = document.getElementById("name").value;

    const res = await fetch(`${BACKEND_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password, name })
    });

    const json = await res.json();
    
    if (res.ok) {
        alert(json.message);
        sessionStorage.setItem("jwt", json.access_token);
        window.location.href = "/";
    } else {
        alert(json.detail);
    }
});
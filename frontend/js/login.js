class XLogin extends HTMLElement {
    constructor() {
        super();

        this.render();
    }

    async handleSubmit(e) {
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

        const json = await res.json();

        if (res.ok) {
            sessionStorage.setItem("jwt", json.access_token);
            window.location.href = "/dashboard.html";
        } else {
            alert(json.detail);
        }
    }

    render() {
        const templateString = `
        <form id="loginForm">
            <input type="email" placeholder="E-Mail" name="email" id="email" required>
            <input type="password" placeholder="Password" name="password" id="password" required>
            <button type="submit">Login</button>
        </form>
        <a href="/register.html"><small>Don't have an account?</small></a>
        `

        this.innerHTML = templateString;
        this.querySelector("#loginForm").addEventListener("submit", this.handleSubmit);
    }
}

customElements.define("x-login", XLogin);
class LogButton extends HTMLElement {
    connectedCallback() {
        const token = sessionStorage.getItem("jwt");
        const isLoggedIn = token != null;
        this.innerHTML = `
            <button id="log-btn">${isLoggedIn ? "Log out" : "Log in"}</button>
        `

        const btn = this.querySelector("#log-btn");
        btn.addEventListener("click", () => {
            if (isLoggedIn) {
                sessionStorage.removeItem("jwt");
                window.location.href = "/";
            } else {
                window.location.href = "/login";
            }
        });
    }
}

customElements.define("log-button", LogButton);

class XNav extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
            <nav class="main-nav">
                <ul id="links">
                    <li><a href="/">Home</a></li>
                    <li><a href="/register">Register</a></li>
                    <li><a href="/login">Login</a></li>
                    <li><a href="/dashboard">User Dashboard</a></li>
                    <li><a href="/admin">Admin Dashboard</a></li>
                    <li><a href="${BACKEND_URL}/docs">API Docs</a></li>
                </ul>

                <log-button></log-button>
            </nav>
        `;
    }
}

customElements.define("x-nav", XNav);

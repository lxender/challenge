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
                </ul>

                <button id="logout-btn">Log out</button>
            </nav>
        `;

        const btn = this.querySelector("#logout-btn");
        btn.addEventListener("click", () => {
            sessionStorage.removeItem("jwt");
            window.location.href = "/";
        });
    }
}

customElements.define("x-nav", XNav);

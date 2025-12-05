class AdminUserControls extends HTMLElement {
    constructor() {
        super();

        this.token = sessionStorage.getItem("jwt");
        this.editingIndex = -1;
    }

    async connectedCallback() {
        await this.fetchUsers();
        this.render();
    }

    async fetchUsers() {
        const res = await fetch(`${BACKEND_URL}/admin/users`, {
            headers: {
                "Authorization": `Bearer ${this.token}`
            }
        });
        const json = await res.json();

        if (!res.ok) {
            alert(json.detail);
            if (res.status === 401) window.location.href = "/";
            this.users = []
        }

        this.users = json.users;
    }

    async saveUserToDatabase(newUser) {
        const res = await fetch(`${BACKEND_URL}/admin/create`, {
            method: "POST",
            body: JSON.stringify(newUser),
            headers: {
                "Authorization": `Bearer ${this.token}`,
                "Content-Type": "application/json"
            }
        });
        const json = await res.json();

        if (!res.ok) {
            alert(json.detail);
        }
    }

    async updateUserInDatabase(id, changes) {
        for (const key in changes) {
            await fetch(`${BACKEND_URL}/admin/update`, {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${this.token}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    loginId: id,
                    [key]: changes[key]
                })
            });
        }
    }

    async deleteUserInDatabase(id) {
        await fetch(`${BACKEND_URL}/admin/delete`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${this.token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                loginId: id,
            })
        });
    }

    render() {
        this.innerHTML = `
            <button id="ua-add" class="btn primary">Add user</button>
            <section class="ua-card">
                <table class="ua-table">
                <thead>
                    <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Login ID</th>
                    <th>Password</th>
                    <th style="width:170px">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${this.users.map((user, i) => this.renderRow(user, i)).join("")}
                </tbody>
                </table>
            </section>
        `;

        this.registerEvents();
    }

    renderRow(user, i) {
        if (i === this.editingIndex) {
            return `
                <tr>
                    <td><input id="ua-name-${i}" type="text" value="${user.name}"></td>
                    <td><input id="ua-email-${i}" type="email" value="${user.email}"></td>
                    <td>${user.loginId ?? ""}</td>
                    <td><input id="ua-pass-${i}" type="password"></td>
                    <td>
                        <button data-save="${i}" class="btn primary">Save</button>
                        <button data-cancel="${i}" class="btn ghost">Cancel</button>
                    </td>
                </tr>
            `;
        }

        return `
            <tr>
                <td>${user.name}</td>
                <td>${user.email}</td>
                <td>${user.loginId}</td>
                <td>*********</td>
                <td>
                    <button data-edit="${i}" class="btn primary">Edit</button>
                    <button data-delete="${i}" class="btn danger">Delete</button>
                </td>
            </tr>
        `;
    }

    registerEvents() {
        this.querySelector("#ua-add").addEventListener("click", () => {
            this.users.push({
                new: true,
                name: "",
                email: "",
                loginId: "",
                password: ""
            });
            const idx = this.users.length - 1;
            this.editingIndex = idx;
            this.render();
        });

        this.querySelectorAll("[data-edit]").forEach(btn =>
            btn.addEventListener("click", () => {
                const idx = Number(btn.dataset.edit);
                this.editingIndex = idx;
                this._originalUser = JSON.parse(JSON.stringify(this.users[idx]));
                this.render();
            })
        );

        this.querySelectorAll("[data-delete]").forEach(btn =>
            btn.addEventListener("click", async () => {
                const i = Number(btn.dataset.delete);
                if (confirm(`Delete user "${this.users[i].name}"?`)) {
                    this.editingIndex = -1;
                    await this.deleteUserInDatabase(this.users[i].loginId);
                    await this.fetchUsers();
                    this.render();
                }
            })
        );

        this.querySelectorAll("[data-save]").forEach(btn =>
            btn.addEventListener("click", async () => {
                const i = Number(btn.dataset.save);
                const isNewUser = this.users[i].new;

                const original = this._originalUser;

                const pass = this.querySelector(`#ua-pass-${i}`).value;
                const updated = {
                    name: this.querySelector(`#ua-name-${i}`).value.trim(),
                    email: this.querySelector(`#ua-email-${i}`).value.trim(),
                    password: pass === "" ? undefined : pass
                };

                if (isNewUser) {
                    await this.saveUserToDatabase(updated);
                } else {
                    const changes = {};
                    for (const key of Object.keys(updated)) {
                        if (updated[key] !== original[key]) {
                            changes[key] = updated[key];
                        }
                    }

                    if (Object.keys(changes).length > 0) {
                        await this.updateUserInDatabase(original.loginId, changes);
                    }
                }

                this.editingIndex = -1;

                await this.fetchUsers();
                this.render();
            })
        );

        this.querySelectorAll("[data-cancel]").forEach(btn =>
            btn.addEventListener("click", () => {
                this.editingIndex = -1;
                this.render();
            })
        );
    }
}

customElements.define("admin-user-controls", AdminUserControls);

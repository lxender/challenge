import "./user-profile-item.js";

class UserProfile extends HTMLElement {
    constructor() {
        super();

        this.token = sessionStorage.getItem("jwt");;
        if (this.token === null) {
            window.location.href = "/";
        }
    }

    async connectedCallback() {
        const res = await fetch(
            `${BACKEND_URL}/profile`,
            { 
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${this.token}`
                }
            }
        );
        const json = await res.json();

        if (res.ok) {
            this.data = json.profile;
            this.render();
        } else {
            alert(JSON.stringify(json.detail));
        }
    }

    async saveToDatabase(key, newData) {
        const res = await fetch(
            `${BACKEND_URL}/profile/update/${key}`,
            {
                method: "POST", 
                headers: {
                    "Authorization": `Bearer ${this.token}`,
                },
                body: newData[key]
            }
        )

        if (!res.ok) {
            const json = await res.json();
            alert(JSON.stringify(json.detail));
        }
    }

    handleItemSave(newData) {
        const key = Object.keys(newData)[0];
        this.saveToDatabase(key, newData);
    }

    render() {
        if (this.data === undefined) return;

        this.innerHTML = "";

        // Don't expose the password, use a dummy field
        this.data["password"] = "***********";

        for (const key in this.data) {
            const detail = document.createElement("user-profile-item");
            detail.data = { [key]: this.data[key] };
            detail.onSave = this.handleItemSave.bind(this);
            this.appendChild(detail);
        }
    }
}
customElements.define("user-profile", UserProfile);
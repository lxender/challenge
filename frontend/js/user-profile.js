import "./user-profile-item.js";

class UserProfile extends HTMLElement {
    constructor() {
        super();
    }

    async connectedCallback() {
        const token = sessionStorage.getItem("jwt");
        if (token === null) {
            window.location.href = "/";
        }

        const res = await fetch(
            `${BACKEND_URL}/profile`,
            {
                method: "POST", headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );
        const json = await res.json();
        
        if (res.ok) {
            console.log(json);
            this.data = json.details;
            this.render();
        } else {
            alert(JSON.stringify(json.detail));
        }
    }

    handleSave(newData) {
        console.log(newData);
    }

    render() {
        if (this.data === undefined) return;

        this.innerHTML = "";

        for (const key in this.data) {
            const detail = document.createElement("user-profile-item");
            detail.data = { [key]: this.data[key] };
            detail.onSave = this.handleSave;
            this.appendChild(detail);
        }
    }
}
customElements.define("user-profile", UserProfile);
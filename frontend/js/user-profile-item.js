const showModeTemplate = `
<h3 id="title"></h3>
<div id="value-wrapper">
    <div id="value"></div>
    <button id="value-edit-btn">Update</button>
</div>
`;

const editModeTemplate = `
<h3 id="title"></h3>
<div id="value-wrapper">
    <input />
    <button id="value-save-btn">Save</button>
    <button id="value-cancel-btn">Cancel</button>
</div>
`;

class UserProfileItem extends HTMLElement {
    constructor() {
        super();

        this.mode = "show";

        this.render();
    }

    get mode() {
        return this._mode;
    }

    set mode(value) {
        this._mode = value;
        this.render();
    }

    get data() {
        return this._data;
    }

    set data(value) {
        this._data = value;
        this.render();
    }

    save(key, newValue) {
        this._data[key] = newValue;
        const copy = JSON.parse(JSON.stringify(this._data));
        this.onSave?.(copy);
        this.mode = "show";
    }

    render() {
        if (this._data === undefined) return;
        this.innerHTML = "";

        const template = this.mode === "show" ? showModeTemplate : editModeTemplate;
        this.innerHTML = template;

        const key = Object.keys(this._data)[0];

        const title = this.querySelector("#title");
        title.innerHTML = key.substring(0, 1).toUpperCase() + key.substring(1);

        if (this.mode === "show") {
            const valueEl = this.querySelector("#value");
            valueEl.innerHTML = this._data[key];

            const editBtn = this.querySelector("#value-edit-btn");
            editBtn.addEventListener("click", () => this.mode = "edit");
        } else {
            const input = this.querySelector("input");
            input.value = key === "password" ? "" : this._data[key];

            const saveBtn = this.querySelector("#value-save-btn");
            saveBtn.addEventListener("click", () => {
                this.save(key, input.value);
            });

            const cancelBtn = this.querySelector("#value-cancel-btn");
            cancelBtn.addEventListener("click", () => {
                this.mode = "show";
            });
        }
    }
}

customElements.define("user-profile-item", UserProfileItem);
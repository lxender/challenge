const templateStyle = `
<style>
    #value-wrapper {
        display: flex;
        gap: 1em;
        align-items: baseline;
    }
</style>
`

const showModeTemplate = `
${templateStyle}
<h3 id="title"></h3>
<div id="value-wrapper">
    <span id="value"></span>
    <button id="value-edit-btn">Update</button>
</div>
`;

const editModeTemplate = `
${templateStyle}
<h3 id="title"></h3>
<div id="value-wrapper">
    <input />
    <button id="value-save-btn">Save</button>
</div>
`;

class UserProfileItem extends HTMLElement {
    constructor() {
        super();

        this.mode = "show";

        this.attachShadow({ mode: "open" });
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
        const root = this.shadowRoot;
        root.innerHTML = "";

        const template = this.mode === "show" ? showModeTemplate : editModeTemplate;
        root.innerHTML = template;

        const key = Object.keys(this._data)[0];

        const title = root.getElementById("title");
        title.innerHTML = key.substring(0, 1).toUpperCase() + key.substring(1);

        if (this.mode === "show") {
            const valueEl = root.getElementById("value");
            valueEl.innerHTML = this._data[key];

            const editBtn = root.querySelector("button");
            editBtn.addEventListener("click", () => this.mode = "edit");
        } else {
            const input = root.querySelector("input");
            input.value = this._data[key];

            const saveBtn = root.querySelector("button");
            saveBtn.addEventListener("click", () => {
                this.save(key, input.value);
            });
        }
    }
}

customElements.define("user-profile-item", UserProfileItem);
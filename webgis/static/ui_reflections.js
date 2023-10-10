function createTextElement(text, type="label") {
    let label = document.createElement(type);
    label.setAttribute("for", text)
    let description = document.createTextNode(text);
    label.appendChild(description);
    
    return label
}

// How the form to apply a new entry will look like
const type_gui_reflections = {
    "Dropdown": (name, params) => {
        let label = createTextElement(name, "legend")

        let dropdown = document.createElement("select");
        dropdown.setAttribute("name", name)
        dropdown.type = "select";

        let fieldset = document.createElement("fieldset");
        fieldset.setAttribute("id", name);  
        fieldset.setAttribute("class", "form-check");
        params.values.forEach(value => {
            let div = document.createElement("div");
            let option = document.createElement("option");
            option.setAttribute("name", name)
            option.innerHTML = value
            dropdown.appendChild(option);
        });

        return {"label": label, "input": dropdown};
    },
    "Comment": (name, value) => {
        let label = createTextElement(name, "legend")
        
        let textInput = document.createElement("input");
        textInput.setAttribute("name", name)
        textInput.type = "text";
        let div = document.createElement("div");
        div.appendChild(textInput);

        return {"label": label, "input": div};
    },
    "Spinbox": (name, value) => {
        let label = createTextElement(name, "legend")

        let numberInput = document.createElement("input");
        numberInput.setAttribute("name", name)
        numberInput.type = "number";
        let div = document.createElement("div");
        div.appendChild(numberInput)

        return {"label": label, "input": div};
    },
    "Image": (name, value) => {
        let label = createTextElement(name, "legend")

        let parent = document.createElement("span");

        let imageButton = document.createElement("input");
        imageButton.type = "file";
        imageButton.accept = "image";
        imageButton.capture = "environment";

        // The visible form is the imageButton created above, but we can't save a binary image
        // in there. Therefore, we create a hidden input within which we save the binary image.
        // This hidden input is what is sent to the server.
        let imageInput = document.createElement("input");
        imageInput.setAttribute("name", name)
        imageInput.type = "hidden";

        imageButton.addEventListener('change', function() {
            // As soon as an image is selected in the imageButton, convert it to Base64 binary
            // and save the result into the imageInput.
            if (this.files && this.files[0]) {
                const file = this.files[0]
                const reader = new FileReader()
                reader.onloadend = () => {
                    imageInput.value = reader.result
                }
                reader.readAsDataURL(file)
            }
        });

        parent.appendChild(imageButton);
        parent.appendChild(imageInput);

        return {"label": label, "input": parent};
    },
    "Radio": (name, params) => {
        let title = createTextElement(name, "legend")

        let fieldset = document.createElement("fieldset");
        fieldset.setAttribute("id", name);  
        fieldset.setAttribute("class", "form-check");
        params.values.forEach(value => {
            let div = document.createElement("div");
            let label = createTextElement(value)
            label.setAttribute("class", "form-check-label")
            let radio = document.createElement("input");
            radio.setAttribute("name", name)
            radio.setAttribute("value", value)
            radio.setAttribute("class", "form-check-input")
            radio.type = "radio";
            div.appendChild(label);
            div.appendChild(radio);
            fieldset.appendChild(div);
        });

        return {"label": title, "input": fieldset};
    },
    "Checkbox": (name, params) => {
        let title = createTextElement(name, "legend")
        
        let fieldset = document.createElement("fieldset");
        fieldset.setAttribute("id", name);   
        fieldset.setAttribute("class", "form-check");
        params.values.forEach(value => {
            let div = document.createElement("div");
            let label = createTextElement(value)
            label.setAttribute("class", "form-check-label")
            let checkbox = document.createElement("input");
            checkbox.setAttribute("name", name)
            checkbox.setAttribute("value", value)
            checkbox.setAttribute("class", "form-check-input")
            checkbox.type = "checkbox";
            div.appendChild(label);
            div.appendChild(checkbox);
            fieldset.appendChild(div);
        });

        return {"label": title, "input": fieldset};
    }
} 

// How an applied entry will be displayed
const type_display_reflections = {
    "Dropdown": (name, value) => {
        let container = document.createElement("container");

        let label = document.createElement("label");
        let description = document.createTextNode(name + ": " + value);

        label.appendChild(description);
        container.appendChild(label);

        return container;
    },
    "Comment": (name, value) => {
        let container = document.createElement("container");

        let label = document.createElement("label");
        let description = document.createTextNode(name + ": " + value);

        label.appendChild(description);
        container.appendChild(label);

        return container;
    },
    "Spinbox": (name, value) => {
        let container = document.createElement("container");

        let label = document.createElement("label");
        let description = document.createTextNode(name + ": " + value);

        label.appendChild(description);
        container.appendChild(label);

        return container;
    },
    "Image": (name, value) => {
        let container = document.createElement("container");

        let label = document.createElement("label");
        let description = document.createTextNode(name + ": ");

        const image = new Image();
        image.style.maxWidth = 200;
        image.style.maxHeight = 200;
        image.src = value;  // a Base64 encoded String, e.g. "data:image/jpg;base64,BINARY"

        label.appendChild(description);
        label.appendChild(document.createElement("br"))
        label.appendChild(image);
        container.appendChild(label);

        return container;
    },
    "Radio": (name, value) => {
        let container = document.createElement("container");

        let label = document.createElement("label");
        let description = document.createTextNode(name + ": " + value);

        label.appendChild(description);
        container.appendChild(label);

        return container;
    },
    "Checkbox": (name, value) => {
        let container = document.createElement("container");

        let label = document.createElement("label");
        let description = document.createTextNode(name + ": " + value);

        label.appendChild(description);
        container.appendChild(label);

        return container;
    }
} 


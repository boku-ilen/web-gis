function createLabel(name) {
    let label = document.createElement("label");
    label.setAttribute("for", name)
    let description = document.createTextNode(name);
    label.appendChild(description);
    
    return label
} 

const type_gui_reflections = {
    "Boolean": (name, value) => {
        let label = createLabel(name)

        let checkbox = document.createElement("select");
        checkbox.setAttribute("name", name)
        checkbox.type = "select";
        let yesOption = document.createElement("option");
        yesOption.setAttribute("value", 1)
        yesOption.innerHTML = "yes"
        let noOption = document.createElement("option");
        noOption.setAttribute("value", 0)
        noOption.innerHTML = "no"
        checkbox.appendChild(noOption)
        checkbox.appendChild(yesOption)

        return {"label": label, "input": checkbox};
    },
    "String": (name, value) => {
        let label = createLabel(name)

        let textInput = document.createElement("input");
        textInput.setAttribute("name", name)
        textInput.type = "text";

        return {"label": label, "input": textInput};
    },
    "Integer": (name, value) => {
        let label = createLabel(name)

        let numberInput = document.createElement("input");
        numberInput.setAttribute("name", name)
        numberInput.type = "number";

        return {"label": label, "input": numberInput};
    },
    "HTMLImageElement": (name, value) => {
        let label = createLabel(name)

        let imageButton = document.createElement("input");
        imageButton.setAttribute("name", name)
        imageButton.type = "file";
        imageButton.accept = "image"; 

        return {"label": label, "input": imageButton};
    },
    "Radio": (name, value) => {
        let label = createLabel(name)

        let radio = document.createElement("input");
        radio.setAttribute("name", name)
        radio.type = "radio";

        return {"label": label, "input": radio};
    },
    "Checkbox": (name, value) => {
        let label = createLabel(name)

        let checkbox = document.createElement("input");
        checkbox.setAttribute("name", name)
        checkbox.type = "checkbox";

        return {"label": label, "input": checkbox};
    }
} 

const type_display_reflections = {
    "Boolean": (name, value) => {
        let container = document.createElement("container");

        var value_string = value ? "Ja" : "Nein";

        let label = document.createElement("label");
        let description = document.createTextNode(name + ": " + value_string);

        label.appendChild(description);
        container.appendChild(label);

        return container;
    },
    "String": (name, value) => {
        let container = document.createElement("container");

        let label = document.createElement("label");
        let description = document.createTextNode(name + ": " + value);

        label.appendChild(description);
        container.appendChild(label);

        return container;
    },
    "Integer": (name, value) => {
        let container = document.createElement("container");

        let label = document.createElement("label");
        let description = document.createTextNode(name + ": " + value);

        label.appendChild(description);
        container.appendChild(label);

        return container;
    },
    "HTMLImageElement": (name, value) => {
        let container = document.createElement("container");

        let label = document.createElement("label");
        let description = document.createTextNode(name + ": ");

        const image = new Image();
        image.style.width = 200;
        image.src = value;

        label.appendChild(description);
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


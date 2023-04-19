const type_gui_reflections = {
    "Boolean": (name, value) => {
        let container = document.createElement("container"); 

        let label = document.createElement("label");
        let description = document.createTextNode(name);
        label.appendChild(description);

        let checkbox = document.createElement("input");
        checkbox.type = "checkbox";

        container.appendChild(label);
        container.appendChild(checkbox);

        return container;
    },
    "String": (name, value) => {
        let container = document.createElement("container"); 

        let label = document.createElement("label");
        let description = document.createTextNode(name);
        label.appendChild(description);

        let text_input = document.createElement("input");
        text_input.type = "text";

        container.appendChild(label);
        container.appendChild(text_input);

        return container;
    },
    "Integer": (name, value) => {
        let container = document.createElement("container"); 

        let label = document.createElement("label");
        let description = document.createTextNode(name);
        label.appendChild(description);

        let number_input = document.createElement("input");
        number_input.type = "number";

        container.appendChild(label);
        container.appendChild(number_input);

        return container;
    },
    "HTMLImageElement": (name, value) => {
        let container = document.createElement("container"); 

        let label = document.createElement("label");

        let imageButton = document.createElement("input");
        imageButton.type = "file";
        imageButton.accept = "image"; 

        container.appendChild(label);
        container.appendChild(imageButton);

        return container;
    },
} 


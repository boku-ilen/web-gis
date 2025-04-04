function createTextElement(text, type="label") {
    let label = document.createElement(type);
    label.setAttribute("for", text)
    let description = document.createTextNode(text);
    label.appendChild(description);
    
    return label
}

// How the form to apply a new entry will look like
const type_gui_reflections = {
    "Dropdown": (name, params, form) => {
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

        return {"input": dropdown};
    },
    "Comment": (name, value, form) => {
        let textInput = document.createElement("input");
        textInput.setAttribute("name", name)
        textInput.type = "text";
        let div = document.createElement("div");
        div.appendChild(textInput);

        return {"input": div};
    },
    "MultiLineText": (name, params, form) => {
        let textInput = document.createElement("textarea");
        textInput.setAttribute("name", name)
        textInput.rows = params["rows"];

        let div = document.createElement("div");
        div.appendChild(textInput);

        return {"input": div};
    },
    "Spinbox": (name, value, form) => {
        let numberInput = document.createElement("input");
        numberInput.setAttribute("name", name)
        numberInput.type = "number";
        let div = document.createElement("div");
        div.appendChild(numberInput)

        return {"input": div};
    },
    "Image": (name, value, form) => {
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

        return {"input": parent};
    },
    "Radio": (name, params, form) => {
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

        return {"input": fieldset};
    },
    "Checkbox": (name, params, form) => {
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

        return {"input": fieldset};
    },
    "SemanticDifferential": (name, params, form) => {
        let fieldset = document.createElement("fieldset");
        fieldset.setAttribute("id", name);
        fieldset.setAttribute("class", "form-check");
        let table = document.createElement("table");
        fieldset.appendChild(table);
        let trScale = document.createElement("tr");
        trScale.appendChild(document.createElement("th"));
        table.appendChild(trScale);

        // The "heading" (e.g. sehr, eher, teils)
        params.scales.forEach(scale => {
            let th = document.createElement("th");
            th.innerHTML = scale
            trScale.appendChild(th);
        });

        // The actual radios in the differential
        let i = 0
        let keys = []
        params.rowDefinitions.forEach(definition => {
            let tr = document.createElement("tr");
            let tdDef0 = document.createElement("td");
            tdDef0.className = "sd-descriptor"
            tdDef0.innerHTML = definition[0];
            tr.appendChild(tdDef0);
            
            // Save keys for later, as we have to alter the submit data slightly
            let radioName = (`${definition[0]}/${definition[1]}`)
            keys.push(radioName);

            for (const dataNum of Array(params.scales.length).keys()) {
                let td = document.createElement("td");
                let radio = document.createElement("input");
                let attributes = {"type": "radio", "name": radioName, "value": String(dataNum)};
                Object.entries(attributes).forEach(([key, val]) => radio.setAttribute(key, val));
                td.appendChild(radio);
                tr.appendChild(td)
            }

            let tdDef1 = document.createElement("td");
            tdDef1.innerHTML = definition[1];            
            tr.appendChild(tdDef1);

            table.appendChild(tr);
            i += 1;
        });

        // Before the input is sent, catch it and alter it to be one entry only instead of multiple,
        // otherwise the server will reject the entry
        // i.e. from radioName1: val1, radioName2: val2 to formName: [val1, val2]
        form.addEventListener('formdata', (e) => {
            let values = []
            keys.forEach((key) => { 
                values.push(e.formData.get(key)); 
                e.formData.delete(key);
            });
            e.formData.append(name, values);
        });

        return {"input": fieldset}
    },
    "MatrixQuestions": (name, params, form) => {
        let fieldset = document.createElement("fieldset");
        fieldset.setAttribute("id", name);   
        fieldset.setAttribute("class", "form-check");
        let table = document.createElement("table");
        fieldset.appendChild(table);
        let trScale = document.createElement("tr");
        trScale.appendChild(document.createElement("th"));
        table.appendChild(trScale);

        // The "heading" (e.g. sehr, eher, teils)
        params.scales.forEach(scale => {
            let th = document.createElement("th");
            th.innerHTML = scale
            trScale.appendChild(th);
        });

        // The actual radios in the differential
        let i = 0

        var keys = []
        params.questions.forEach(question => {
            let trQuestion = document.createElement("tr");
            let tdQuestion = document.createElement("td");
            tdQuestion.setAttribute("colspan", 999);
            tdQuestion.innerHTML = question;
            trQuestion.appendChild(tdQuestion);
            table.appendChild(trQuestion);

            let tr = document.createElement("tr");
            
            // Save keys for later, as we have to alter the submit data slightly
            keys.push(question);

            // Add empty column for spacing
            tr.appendChild(document.createElement("td"));
            for (const dataNum of Array(params.scales.length).keys()) {
                let td = document.createElement("td");
                let radio = document.createElement("input");
                let attributes = {"type": "radio", "name": question, "value": String(dataNum)};
                Object.entries(attributes).forEach(([key, val]) => radio.setAttribute(key, val));
                td.appendChild(radio);
                tr.appendChild(td)
            }

            table.appendChild(tr);
            i += 1;
        });

        // Before the input is sent, catch it and alter it to be one entry only instead of multiple,
        // otherwise the server will reject the entry
        // i.e. from radioName1: val1, radioName2: val2 to formName: [val1, val2]
        document.querySelector("form").addEventListener('formdata', (e) => {
            let values = []
            keys.forEach((key) => { 
                values.push(e.formData.get(key)); 
                e.formData.delete(key);
            });
            e.formData.append(name, values);
        });

        return {"input": fieldset}
    }
} 

// How an applied entry will be displayed
const type_display_reflections = {
    "Dropdown": (name, value, fieldDef) => {
        let container = document.createElement("div");
        let label = document.createElement("label");
        label.textContent = `${name}:`;

        let selected = document.createElement("p");
        selected.textContent = fieldDef.params?.values?.includes(value) ? value : "N/A";

        container.appendChild(label);
        container.appendChild(selected);
        return container;
    },
    "Comment": (name, value, fieldDef) => {
        let container = document.createElement("div");
        let label = document.createElement("label");
        label.textContent = `${name}:`;

        let paragraph = document.createElement("p");
        paragraph.textContent = value;

        container.appendChild(label);
        container.appendChild(paragraph);
        return container;
    },
    "MultiLineText": (name, value, fieldDef) => {
        let container = document.createElement("div");
        let label = document.createElement("label");
        label.textContent = `${name}:`;

        let pre = document.createElement("pre");
        pre.textContent = value;

        container.appendChild(label);
        container.appendChild(pre);
        return container;
    },
    "Spinbox": (name, value, fieldDef) => {
        let container = document.createElement("div");
        let label = document.createElement("label");
        label.textContent = `${name}:`;

        let valueNode = document.createElement("p");
        valueNode.textContent = value;

        container.appendChild(label);
        container.appendChild(valueNode);
        return container;
    },
    "Image": (name, value, fieldDef) => {
        let container = document.createElement("div");
        let label = document.createElement("label");
        label.textContent = `${name}:`;

        const image = new Image();
        image.style.maxWidth = "200px";
        image.style.maxHeight = "200px";
        image.src = value;

        container.appendChild(label);
        container.appendChild(image);
        return container;
    },
    "Radio": (name, value, fieldDef) => {
        let container = document.createElement("div");
        let label = document.createElement("label");
        label.textContent = `${name}:`;

        let val = document.createElement("p");
        val.textContent = value;

        container.appendChild(label);
        container.appendChild(val);
        return container;
    },
    "Checkbox": (name, value, fieldDef) => {
        let container = document.createElement("div");
        let label = document.createElement("label");
        label.textContent = `${name}:`;

        let list = document.createElement("ul");
        (Array.isArray(value) ? value : value.split(",")).forEach(v => {
            let item = document.createElement("li");
            item.textContent = v;
            list.appendChild(item);
        });

        container.appendChild(label);
        container.appendChild(list);
        return container;
    },
    "SemanticDifferential": (name, values, fieldDef) => {
        let container = document.createElement("div");
        let label = document.createElement("label");
        label.textContent = `${name}:`;

        let list = document.createElement("ul");
        const splitValues = values[0].split(",");

        fieldDef.params.rowDefinitions.forEach((definition, index) => {
            let item = document.createElement("li");
            let val = fieldDef.params.scales[splitValues[index]] || "-";
            item.textContent = `${definition[0]} – ${definition[1]}: ${val}`;
            list.appendChild(item);
        });

        container.appendChild(label);
        container.appendChild(list);
        return container;
    },
    "MatrixQuestions": (name, values, fieldDef) => {
        let container = document.createElement("div");
        let label = document.createElement("label");
        label.textContent = `${name}:`;

        let list = document.createElement("ul");
        const splitValues = values[0].split(",");

        fieldDef.params.questions.forEach((question, index) => {
            let item = document.createElement("li");
            let val = fieldDef.params.scales[splitValues[index]] || "-";
            item.textContent = `${question}: ${val}`;
            list.appendChild(item);
        });

        container.appendChild(label);
        container.appendChild(list);
        return container;
    }
}

export class TextLecture {
    constructor (fillFields) {
        this.fillFields = fillFields;
    }
    initLecture(file){
        this.getFileContentJSON(file); 
    }

    getFileContentJSON(file) {
        let jsonContent = null;
        this.clearFormatWarning();

        if (file == undefined || file.length === 0 || file[0] == undefined) return jsonContent;

        if (file[0].type != 'text/plain') {
            this.showInvalidExtensionWarning();
            return jsonContent;
        }else {
            try {
                this.readFileContent(file, (content)=> {
                    this.fillFields(content.data); // este metodo rellena los fields del template
                    jsonContent = content.data 
                });               
            }catch(e){
                console.log('Error al leer el texto: '+ e);
            }
        }
        return jsonContent;
    }

    readFileContent(file, callback) {
        const reader = new FileReader();
        reader.onload = (e) => {
            callback(this.parseTxtJson(e.target.result));
        };
        reader.readAsText(file[0]);
    }

    parseTxtJson(result) {
        // recorrer el archivo y sacar datos 
        let dataJson = {};
        let hasInvalidFormat = false;
        let validFields = this.getValidFields();
        const lines = result.split('\n');
        lines.forEach((line, index) => {
            let cleanLine = line.trim();
            if (cleanLine === '') return;

            let commentPosition = cleanLine.indexOf('#');
            if (commentPosition === -1) {
                hasInvalidFormat = true;
                return;
            }

            let fieldContent = cleanLine.slice(0, commentPosition).trim();
            if (fieldContent === '') return;

            let separatorPosition = fieldContent.indexOf('=');
            if (separatorPosition === -1) {
                hasInvalidFormat = true;
                return;
            }

            let fieldName = fieldContent.slice(0, separatorPosition).trim();
            let fieldValue = fieldContent.slice(separatorPosition + 1).trim();

            if (fieldName === '' || fieldValue === '') {
                hasInvalidFormat = true;
                return;
            }

            if (!validFields.has(fieldName)) {
                hasInvalidFormat = true;
                return;
            }

            dataJson = {
                ...dataJson,
                [fieldName]: fieldValue
            };
        });
        return {
            "data": dataJson,
            "hasInvalidFormat": hasInvalidFormat
        };
    }

    showInvalidExtensionWarning() {
        let warning = document.getElementById('warning');
        if (warning == undefined) return;

        warning.dataset.source = 'file-extension';
        warning.innerText = 'The selected file must be a .txt file.';
        warning.style.display = 'block';
        warning.classList.remove('alert-success', 'alert-danger');
        warning.classList.add('alert-warning');
    }

    clearFormatWarning() {
        let warning = document.getElementById('warning');
        if (warning == undefined || !['file-format', 'file-extension'].includes(warning.dataset.source)) return;

        warning.innerText = '';
        warning.style.display = 'none';
        delete warning.dataset.source;
    }

    getValidFields() {
        let fields = new Set();
        document.querySelectorAll('.inputAjax').forEach((input) => fields.add(input.id));
        return fields;
    }

}

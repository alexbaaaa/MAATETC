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
            this.showFormatWarning();
        }else {
            try {
                this.readFileContent(file, (content)=> {
                    this.fillFields(content.data); // este metodo rellena los fields del template
                    if (content.hasInvalidFormat) this.showFormatWarning();
                    jsonContent = content.data 
                });               
            }catch(e){
                console.log('Error al leer el texto: '+ e);
                this.showFormatWarning();
            }
        }
        return jsonContent;
    }

    readFileContent(file, callback) {
        const reader = new FileReader();
        reader.onload = (e) => {
            callback(this.parseTxtJson(e.target.result));
        };
        reader.onerror = () => {
            this.showFormatWarning();
        };
        reader.readAsText(file[0]);
    }

    parseTxtJson(result) {
        // recorrer el archivo y sacar datos 
        let dataJson = {};
        let hasInvalidFormat = false;
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

    showFormatWarning() {
        let warning = document.getElementById('warning');
        if (warning == undefined) return;

        warning.dataset.source = 'file-format';
        warning.innerText = 'The selected file has an invalid format. Some fields may have been loaded, but malformed lines were ignored.';
        warning.style.display = 'block';
    }

    clearFormatWarning() {
        let warning = document.getElementById('warning');
        if (warning == undefined || warning.dataset.source != 'file-format') return;

        warning.innerText = '';
        warning.style.display = 'none';
        delete warning.dataset.source;
    }

}

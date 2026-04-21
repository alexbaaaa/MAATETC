// Import provisional para pruebas 
// Cambiar los lugares donde se ejecuta
export class TextLecture {
    constructor (fillFields) {
        this.file = null;
        this.fillFields = fillFields;
    }
    initLecture(file){
        this.file = file;
        this.getFileContentJSON(this.file); 
    }

    getFileContentJSON(file) {
        let jsonContent = null;
        if (file[0].type != 'text/plain') {
            // Implementar mensaje en html
            console.log('formato de archivo invalido');
        }else {
            this.readFileContent(file, (content)=> {
                this.fillFields(content); // este metodo rellena los fields del template
                jsonContent = content 
            });
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
        let dataJson = {}
        const lines = result.split('\n');
        lines.forEach((line, index) => {
            let line2 = line.split('#');
            let element = line2[0].split("=");
            dataJson = {
                ...dataJson,
                [element[0].trim()]: element[1].trim()
            }
        });
        return dataJson;
    }

}
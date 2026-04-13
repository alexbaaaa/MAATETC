// Import provisional para pruebas 
// Cambiar los lugares donde se ejecuta
export class TextLecture {
    constructor (prueba1) {
        this.file = null;
        this.prueba1 = prueba1;
    }
    initLecture(file){
        this.file = file;
        this.getFileContentJSON(this.file); 
    }

    getFileContentJSON(file) {
        if (file[0].type != 'text/plain') {
            // Implementar mensaje en html
            console.log('formato de archivo invalido');
        }else {
            this.readFileContent(file, (content)=> {
                this.prueba1(content);
            });
        }
    }

    readFileContent(file, callback) {
        const reader = new FileReader();
        reader.onload = () => {
            callback(reader.result);
        };
        reader.readAsText(file[0]);
    }

}
import {RequestHandler} from './requestHandler.js'
class FormatData {
    constructor (uic) {
        this.uic = uic;
    }

    init(data) {
        new RequestHandler(this.#getData(data), this.uic.printData);
    }

    #getData(data) {
        // validacion aqui si o si antes de mandar los datos al request
        return this.#structuringData(data);
    }

    #structuringData(data) {
        console.log(data)
        let dataJson = {};
        let dataValue;
        data.forEach(element => {
            dataValue = element.value.trim() === "" ? "" : element.value ; 
            if (element.name === 'wvinflux') element.name = 'refwv';
            if (element.name === 'sedtemplate' & element.value != 'ones') {
                let sedtemplate  = document.getElementById('sedtemplate_'+element.value);
                (element.value == 'blackbody')? dataValue+= ' ' + sedtemplate.value :  dataValue+= '_' + sedtemplate.value 
            }
            dataJson = {
                ...dataJson,
                [element.name]: dataValue
            }
            
            
        });
        return dataJson;
    }
}
export {FormatData}
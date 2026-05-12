import {RequestHandler} from './requestHandler.js'
import { Validation } from './validation.js';
class FormatData {
    constructor (uic) {
        this.uic = uic;
        this.requestHandler = new RequestHandler(this.uic.printData);
    }

    init(data) {
        this.requestHandler.init(this.#getData(data));
    }

    #getData(data) {
        // Si todo ok
        // if (!Validation.isValid(data).success) {
        //     
        // } else {
        //     // Lamamos al ui y mostramos error o warnning
        // }

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
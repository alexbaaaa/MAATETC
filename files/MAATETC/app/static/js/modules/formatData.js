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
        let psf = document.getElementById('psf')?.value;
        data.forEach(element => {
            let fieldName = element.name;
            dataValue = element.value.trim() === "" ? "" : element.value ; 
            if (fieldName === 'area' && psf == 'pointsource' && dataValue === "") dataValue = "0";
            if (fieldName === 'seeing' && psf == 'extended' && dataValue === "") dataValue = "0";
            if (fieldName === 'wvinflux') fieldName = 'refwv';
            if (fieldName === 'sedtemplate' && element.value != 'ones') {
                let sedtemplate  = document.getElementById('sedtemplate_'+element.value);
                if (element.value == 'blackbody') {
                    dataValue += ' ' + sedtemplate.value;
                } else if (element.value == 'custom') {
                    dataJson.customSedContent = document.getElementById('sedtemplate_custom_content')?.value || '';
                    dataJson.customSedFilename = document.getElementById('sedtemplate_custom_filename')?.value || '';
                } else {
                    dataValue += '_' + sedtemplate.value;
                }
            }
            dataJson = {
                ...dataJson,
                [fieldName]: dataValue
            }
            
            
        });
        return dataJson;
    }
}
export {FormatData}

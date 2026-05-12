import {validationJSON} from './json/validationJson.js'
import {RequestHandler} from './requestHandler.js'
/**
 * Clase para mostrar los warnning y validar los datos de entrada
 * 
 */
export class Validation {
    constructor () {
        this.validationJson = validationJSON
        // Special values
        this.gratings = RequestHandler.getGratingsJson()
    }

    static isValid (data) {
        let isvalid
        this.validationJson.forEach((object) => {
            let input = Array.from(data).find((value) => value.name == object.name)
            if (object.validation(input.value)) {
                isvalid = false 
                object.success = false
            }
        })
        return {
            "success" : isvalid,
            "jsonValid" : this.validationJson
        }
    }

    
}
import {RequestHandler} from './requestHandler.js'

class FormatData {
    constructor (uic) {
        this.uic = uic;
    }

    init(data) {
        new RequestHandler(this.#getData(data), this.uic.printData);
    }

    /** modificar para dos entradas
     *  1 Entrada desde los fields
     *  @return structuringData()
     *  2 Entrada desde texto
     *  @return 
    */ 
    #getData(data) {
        return this.#structuringData(data);
    }

    #structuringData(data) {
        let dataJson = {}
        data.forEach(element => {
            if (element.name === 'wvinflux') element.name = 'refwv' 
            dataJson = {
                ...dataJson,
                [element.name]: element.value.trim() === "" ? "" : element.value
            }
        });
        return dataJson;
    }
}
export {FormatData}
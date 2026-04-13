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
            dataJson = {
                ...dataJson,
                [element.name]: element.value
            }
        });
        return dataJson;
    }
}
export {FormatData}
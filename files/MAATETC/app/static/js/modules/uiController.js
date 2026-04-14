export class UiController {
    constructor () {

    }
    // printDataResult?? metodo pintar graficas futuras
    printData(data) {
        let textresult = document.querySelectorAll('.textResult');
        let dataArray = Object.entries(data);        
        // Provisional ajustar mas adelante
/*         textresult.forEach( element => {
            let result = dataArray.find((data) => data[0] == element.id);
            let htmlObject = document.getElementById(element.id);
            htmlObject.innerHTML = result[1];
            console.log(result);
        })
 */
    }
    /**
     * Method para rellenar campos a traves de un .txt
     */
    fillFields(dataJson) {
        let inputAjax = document.querySelectorAll('.inputAjax');
        let dataJsonArray = Object.entries(dataJson);
        inputAjax.forEach( element => {
            let result = dataJsonArray.find((data) => data[0] == element.id);
            element.value = result[1];
            console.log(result[0] + ' = ' + element.value);
        }) 

    }

    // Metodo provisional para el pintado de las pruebas de .text
    prueba1(dataJson) {
        let dataJson2 = JSON.stringify(dataJson)
        let textoFinal = document.getElementById('final');
        textoFinal.innerHTML = dataJson2;
    }
    
}
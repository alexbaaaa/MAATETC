export class UiController {
    constructor () {

    }
    // printDataResult?? metodo pintar graficas futuras
    printData(data) {
        let img = document.getElementById('imgGrafica');
        let text = document.getElementById('text');
        text.innerHTML = data['text']
        img.src = 'data:image/png;base64,' + data['imagen']
        console.log("Datos en el ui: ",data['imagen'])
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
        }) 

    }

    // Metodo provisional para el pintado de las pruebas de .text
    prueba1(dataJson) {
        let dataJson2 = JSON.stringify(dataJson)
        let textoFinal = document.getElementById('final');
        textoFinal.innerHTML = dataJson2;
    }
    
}
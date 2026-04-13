export class UiController {
    constructor () {

    }
    printData(data) {
        let textresult = document.querySelectorAll('.textResult');
        let dataArray = Object.entries(data);
        
        // Provisional ajustar mas adelante
        textresult.forEach( element => {
            let result = dataArray.find((data) => data[0] == element.id);
            let htmlObject = document.getElementById(element.id);
            htmlObject.innerHTML = result[1];
            console.log(result);
        })

    }
    // Metodo provisional para el pintado de las pruebas de .text
    prueba1(content) {
        console.log(content);
        let textoFinal = document.getElementById('final');
        textoFinal.innerHTML = content;
    }
    
}
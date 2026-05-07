import { componenetesForm } from "./json/componentesForm.js";
import {messages} from "./json/messagesJson.js";
export class UiController {
    constructor () {
        this.componentes = componenetesForm;
        this.father = document.getElementById('sedtemplateFather');
    }
    // printDataResult?? metodo pintar graficas futuras
    printData(data) {
        let img = document.getElementById('imgGrafica');
        let text = document.getElementById('text');
        let url = 'data:image/png;base64,' + data['imagen'];
        text.innerHTML = data['text'];
        img.src = url;
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
        inputAjax[5].dispatchEvent(new Event("change"));
    }
    // Tengo que arreglarlo 
    showAlert (jsonValid) {
        let warning = document.getElementById("warning");
        let display = 'none'
        jsonValid.forEach((element) => {
            console.log(element.name, element.success)
            if (element.success === false) {
                console.log(element.message, window.GRATINGS[0]['grating'][0]);
                warning.innerHTML += element.message + '.  ';
                display = 'block';
            }
        })
        warning.style.display = display;
    }
    showSelectSedTemplate (selectValue) {
        let component = this.componentes.find((comp) => comp.name == selectValue);
        if(component == undefined) component = this.componentes.at(-1);
        document.querySelector('[id^="sedtemplate_"]')?.remove();
        component.create(this.father);
    }

    addMessageToTooplist (targets) {
        Array.from(targets).forEach((target) => {
            let componet = messages.find((element) => element.name == target.id)
            target.setAttribute('data-bs-toggle', 'tooltip');
            target.setAttribute('data-bs-placement', 'top');
            target.setAttribute('data-bs-title', componet.message);
        })
    }
    
}
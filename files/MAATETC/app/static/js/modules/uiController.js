import { componenetesForm } from "./json/componentesForm.js";
import { componenetesGraph } from "./json/componentesGraph.js";
import {messages} from "./json/messagesJson.js";
export class UiController {
    constructor () {
        this.componentes = componenetesForm;
        this.father = document.getElementById('sedtemplateFather');
    }

    colourGrid() {
        
    }

    printData(data) {
        let graph = document.getElementById('graphContent');
        let text = document.getElementById('textContent');

        if (data.success === false) {
            document.getElementById('imgGrafica')?.remove();
            this.printSummaryText(text, data['text']);
            componenetesGraph.find(element => element.name == 'imageDownload').create(text);
            componenetesGraph.find(element => element.name == 'download').create(text);
            return;
        }

        componenetesGraph.find(element => element.name == 'image').create(graph, data['imagen']);
        this.printSummaryText(text, data['text']);
        componenetesGraph.find(element => element.name == 'imageDownload').create(text, data['imagen']);
        componenetesGraph.find(element => element.name == 'download').create(text, data['resultFile']);
    }

    printSummaryText(father, summaryText) {
        componenetesGraph.find(element => element.name == 'text').create(father, summaryText);
        this.formatSummaryText();
    }

    formatSummaryText() {
        let text = document.getElementById('text');
        if (text == undefined) return;

        let lines = text.textContent.split('\n');
        text.textContent = '';
        text.classList.add('summary-text');

        let indentNextLines = false;
        lines.forEach((line) => {
            let cleanLine = line.trimStart();
            if (cleanLine === '') return;

            if (cleanLine.includes('resulting from') && !cleanLine.endsWith(':')) {
                cleanLine += ':';
            }

            let lineElement = document.createElement('span');
            lineElement.classList = 'summary-line';
            if (indentNextLines) lineElement.classList.add('summary-line-indent');
            lineElement.textContent = cleanLine;
            text.appendChild(lineElement);

            if (cleanLine.includes('resulting from') && cleanLine.endsWith(':')) {
                indentNextLines = true;
            }
        });
    }

    /**
     * Method para rellenar campos a traves de un .txt
     */
    fillFields(dataJson) {
        if (dataJson == undefined) return;

        let inputAjax = document.querySelectorAll('.inputAjax');
        let sedtemplate = document.getElementById('sedtemplate');
        let dataJsonArray = Object.entries(dataJson);
        inputAjax.forEach( element => {
            let result = dataJsonArray.find((data) => data[0] == element.id);
            if (result == undefined) return;

            element.value = result[1];
            
            if(element.id == 'sedtemplate') {
                sedtemplate.dispatchEvent(new Event("change"));
            }
        })
        
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
    hiedeTooplist(element) {
        let tooltip = bootstrap.Tooltip.getInstance(element);
        tooltip.hide();
    }
    
}

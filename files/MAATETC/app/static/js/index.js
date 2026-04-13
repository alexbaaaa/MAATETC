import {FormatData} from './modules/formatData.js'
import {TextLecture} from './modules/textLecture.js'
import {UiController} from './modules/uiController.js'

let button = document.getElementById('ajaxButton');
let data = document.querySelectorAll('.inputAjax');
let drogZone = document.getElementById('dropZone');

let uic = new UiController();
let fdata = new FormatData(uic);
let tlecture = new TextLecture(uic.prueba1);

// Quitamos el evento por defecto del buscador
['dragover', 'drop'].forEach(eventName => {
    document.addEventListener(eventName, e => e.preventDefault());
});

button.addEventListener("click", (e) => {
   fdata.init(data);
})

// Pruebas de Drag an Drop
drogZone.addEventListener('drop', (e) => {
    tlecture.initLecture(e.dataTransfer.files);
})

import {FormatData} from './modules/formatData.js'
import {TextLecture} from './modules/textLecture.js'
import {UiController} from './modules/uiController.js'

let button = document.getElementById('ajaxButton');
let data = document.querySelectorAll('.inputAjax');
let drogZone = document.getElementById('dropZone');
let computeSelect = document.getElementById('compute');
let fileUpload = document.getElementById('fileUpload');
let computeLabel = document.getElementById('computeLabel');


let uic = new UiController();
let fdata = new FormatData(uic);
let tlecture = new TextLecture(uic.fillFields);

// Quitamos el evento por defecto del buscador
['dragover', 'drop'].forEach(eventName => {
    document.addEventListener(eventName, e => e.preventDefault());
});

button.addEventListener("click", (e) => {
   fdata.init(data);
})

drogZone.addEventListener('drop', (e) => {
    tlecture.initLecture(e.dataTransfer.files);
})

fileUpload.addEventListener('change', (e) => {
    console.log(e.target.files)
    tlecture.initLecture(e.target.files);
})

computeSelect.addEventListener('change', () => {
    console.log(computeSelect.value);
    computeLabel.innerHTML = computeSelect.value
})


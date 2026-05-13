import {FormatData} from './modules/formatData.js' 
import {TextLecture} from './modules/textLecture.js'
import {UiController} from './modules/uiController.js'
import {Validation} from './modules/validation.js'

/**
 * Variables glovales
 */
window.GRATINGS
/*----------------*/ 

let button = document.getElementById('ajaxButton');
let data = document.querySelectorAll('.inputAjax');
let sedtemplate = document.getElementById('sedtemplate');
let drogZone = document.getElementById('dropZone');
let computeSelect = document.getElementById('compute');
let fileUpload = document.getElementById('fileUpload');
let computeLabel = document.getElementById('computeLabel');
let psf = document.getElementById('psf');
let area = document.getElementById('areaDiv');
let seeing = document.getElementById('seeingDiv');
let fileMessage = document.getElementById('fileMessage');


let uic = new UiController();
let fdata = new FormatData(uic);
let tlecture = new TextLecture(uic.fillFields);
let validation = new Validation();

// Rellenamos el mensage de los tooltips
uic.addMessageToTooplist(data)
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));



/**
 * Eventos necesarios para el funcionamiento de la web
 * Estos eventos los extrere a su respectiva clases mas adelante
 */

// Quitamos el evento por defecto del buscador
['dragover', 'drop'].forEach(eventName => {
    document.addEventListener(eventName, e => e.preventDefault());
});

button.addEventListener("click", (e) => {
    fdata.init(data);
    document.getElementById('imgGrafica').classList = 'rounded mx-auto d-block w-75';
})

drogZone.addEventListener('drop', (e) => {
    fileMessage.innerHTML = e.dataTransfer.files[0]['name']
    tlecture.initLecture(e.dataTransfer.files);
})

fileUpload.addEventListener('change', (e) => {
    console.log(fileMessage);
    fileMessage.innerHTML = e.target.files[0]['name'];
    tlecture.initLecture(e.target.files);
})

computeSelect.addEventListener('change', () => {
    console.log(computeSelect.value);
    computeLabel.innerHTML = computeSelect.value
})

psf.addEventListener('change', (e) => {
    area.style.display = (e.target.value == 'extended') ? 'block' : 'none';
    seeing.style.display = (e.target.value == 'extended') ? 'none' : 'block' ;
})

sedtemplate.addEventListener('change', () => {
    uic.showSelectSedTemplate(sedtemplate.value);
})

/**
 * Evento para el estilado de los fields del form
 */
window.addEventListener('resize', () => {
    uic.colourGrid(window.innerWidth);
});


   
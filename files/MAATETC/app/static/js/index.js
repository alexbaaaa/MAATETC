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
let grating = document.getElementById('grating');
let breadth = document.getElementById('breadth');


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
    e.preventDefault();
    if (!validation.validate(data).success) return;

    fdata.init(data);
})

drogZone.addEventListener('drop', (e) => {
    if (e.dataTransfer.files.length === 0) return;

    fileMessage.innerHTML = e.dataTransfer.files[0]['name']
    tlecture.initLecture(e.dataTransfer.files);
})

fileUpload.addEventListener('change', (e) => {
    if (e.target.files.length === 0) return;

    console.log(fileMessage);
    fileMessage.innerHTML = e.target.files[0]['name'];
    tlecture.initLecture(e.target.files);
})

computeSelect.addEventListener('change', () => {
    console.log(computeSelect.value);
    computeLabel.innerHTML = computeSelect.value == "SN"? "texpo" : "S/N";
})

function updateBreadthFromGrating() {
    if (!window.GRATINGS || !grating || !breadth) return;

    let selectedGrating = window.GRATINGS.find((element) => element[' name'] == grating.value);
    if (selectedGrating == undefined) return;

    breadth.value = selectedGrating.dispersion;
}

window.addEventListener('gratingsLoaded', updateBreadthFromGrating);
grating.addEventListener('change', updateBreadthFromGrating);
updateBreadthFromGrating();

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

/**
 * Evento para elimniar los tooplist
 */
[...data].forEach((element) => {
    element.addEventListener('click', () => {
        uic.hiedeTooplist(element);
    })
    element.addEventListener('input', () => {
        validation.clearField(element);
    })
    element.addEventListener('change', () => {
        validation.clearField(element);
    })
})

   

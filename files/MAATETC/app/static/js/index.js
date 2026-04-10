console.log("Estoy funcionando")

const FORM = document.getElementById('ajaxForm')
const BUTTON = document.getElementById('ajaxButton')
const TEXT = document.getElementById('ajaxResult')
const TEXTINPUT = document.getElementById('ajax')

/** evento de prueba para funcionalidad AJAX */
BUTTON.addEventListener("click", (e) => {
    let data = {data: TEXTINPUT.value};
    fetch('/testAjax', {
        "method": 'POST',
        "body": JSON.stringify(data),
        "headers": {
            "content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        TEXT.innerHTML = data.data;
    }) 
})


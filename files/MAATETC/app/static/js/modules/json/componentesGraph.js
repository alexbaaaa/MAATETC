export let componenetesGraph = [
    {
        'name' : 'image',
        'create' : (father, dataImagen) => {
            document.getElementById('imgGrafica')?.remove();
            if (dataImagen == undefined || dataImagen === '') return;

            let img = document.createElement('img');
            img.classList = 'img-fluid rounded-4 shadow-sm mx-auto d-block p-3 order-1';
            img.id = 'imgGrafica';
            img.src = 'data:image/png;base64,' + dataImagen;
            father.appendChild(img);
        } 
    },
    {
        'name' : 'text',
        'create' : (father, dataText) => {
            document.getElementById('text')?.remove();
            let text = document.createElement('p');
            text.classList = 'mb-0';
            text.id = 'text';
            text.innerHTML = dataText;
            father.firstElementChild.appendChild(text);
            
        }
    },
]

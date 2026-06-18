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
            text.textContent = dataText;
            (father.querySelector('div') || father).appendChild(text);
            
        }
    },
    {
        'name' : 'download',
        'create' : (father, resultFile) => {
            let previous = document.getElementById('resultDownload');
            if (previous?.dataset.objectUrl) {
                URL.revokeObjectURL(previous.dataset.objectUrl);
            }
            previous?.remove();

            if (resultFile == undefined || resultFile.content == undefined || resultFile.content === '') return;

            let blob = new Blob([resultFile.content], { type: 'text/plain' });
            let objectUrl = URL.createObjectURL(blob);
            let link = document.createElement('a');
            link.id = 'resultDownload';
            link.classList = 'btn btn-outline-info btn-sm mt-3';
            link.href = objectUrl;
            link.dataset.objectUrl = objectUrl;
            link.download = resultFile.filename || 'ETC_result.txt';
            link.textContent = 'Download result .txt';

            (father.querySelector('div') || father).appendChild(link);
        }
    },
]

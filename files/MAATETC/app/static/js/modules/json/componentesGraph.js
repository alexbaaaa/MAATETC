function getDownloadActions(father) {
    let actions = document.getElementById('downloadActions');
    if (actions != undefined) return actions;

    actions = document.createElement('div');
    actions.id = 'downloadActions';
    actions.classList = 'download-actions d-flex flex-wrap gap-2 px-3 pb-3';
    (father.querySelector('div') || father).appendChild(actions);
    return actions;
}

function removeDownloadAction(id) {
    let previous = document.getElementById(id);
    if (previous?.dataset.objectUrl) {
        URL.revokeObjectURL(previous.dataset.objectUrl);
    }
    previous?.remove();

    let actions = document.getElementById('downloadActions');
    if (actions != undefined && actions.children.length === 0) actions.remove();
}

function removeDownloadActions() {
    let actions = document.getElementById('downloadActions');
    if (actions == undefined) return;

    actions.querySelectorAll('[data-object-url]').forEach((element) => {
        URL.revokeObjectURL(element.dataset.objectUrl);
    });
    actions.remove();
}

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
            removeDownloadActions();
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
            removeDownloadAction('resultDownload');

            if (resultFile == undefined || resultFile.content == undefined || resultFile.content === '') return;

            let blob = new Blob([resultFile.content], { type: 'text/plain' });
            let objectUrl = URL.createObjectURL(blob);
            let link = document.createElement('a');
            link.id = 'resultDownload';
            link.classList = 'btn btn-outline-info btn-sm';
            link.href = objectUrl;
            link.dataset.objectUrl = objectUrl;
            link.download = resultFile.filename || 'ETC_result.txt';
            link.textContent = 'Download result .txt';

            getDownloadActions(father).appendChild(link);
        }
    },
    {
        'name' : 'imageDownload',
        'create' : (father, dataImagen) => {
            removeDownloadAction('graphDownload');

            if (dataImagen == undefined || dataImagen === '') return;

            let link = document.createElement('a');
            link.id = 'graphDownload';
            link.classList = 'btn btn-outline-info btn-sm';
            link.href = 'data:image/png;base64,' + dataImagen;
            link.download = 'MAAT_ETC_graph.png';
            link.textContent = 'Download graph .png';

            getDownloadActions(father).appendChild(link);
        }
    },
]

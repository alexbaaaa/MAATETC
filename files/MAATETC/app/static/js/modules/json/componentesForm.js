export let componenetesForm = [
    {
        'name' : 'ones',
        'create' : (father) => {
            console.log("No mostramos nada")
        }
    },
    {
        'name' : 'pickles',
        'create' : (father) => {
            
            let div = document.createElement('div');
            let values = ['A0V','B0V','F0V','G0V','K0V','M0V','O5V']
            let select = document.createElement('select');
            let label = document.createElement('label');
            div.id = 'sedtemplate_pickles_div';
            label.htmlFor = 'sedtemplate_pickles';
            label.id = 'sedtemplate_pickles_label';
            label.classList = 'form-label';
            label.innerHTML = 'Select one';
            select.id = 'sedtemplate_pickles';
            select.classList = 'form-select';
            values.forEach((value) => {
                let option = document.createElement('option');
                option.value = value;
                option.innerHTML = value;
                select.add(option)
            })
            div.appendChild(label);
            div.appendChild(select);
            father.appendChild(div);
        }
    },
    {
        'name' : 'blackbody',
        'create' : (father) => {
            let div = document.createElement('div');
            let input = document.createElement('input');
            let label = document.createElement('label');
            
            div.id = 'sedtemplate_blackbody_div w-auto';
            label.htmlFor = 'sedtemplate_blackbody';
            label.id = 'sedtemplate_blackbody_label';
            label.classList = 'form-label';
            label.innerHTML = 'Temperature';
            input.type = 'number';
            input.id = 'sedtemplate_blackbody';
            input.value = '5778';
            input.classList = 'form-control';
            div.appendChild(label)
            div.appendChild(input)
            father.appendChild(div)
        }
    },
    {
        'name' : 'custom',
        'create' : (father) => {
            let div = document.createElement('div');
            let label = document.createElement('label');
            let dropZone = document.createElement('div');
            let button = document.createElement('span');
            let message = document.createElement('span');
            let fileInput = document.createElement('input');
            let contentInput = document.createElement('textarea');
            let filenameInput = document.createElement('input');

            div.id = 'sedtemplate_custom_div';
            div.classList = 'sed-file-field';

            label.htmlFor = 'sedtemplate_custom_file';
            label.id = 'sedtemplate_custom_label';
            label.classList = 'form-label';
            label.textContent = 'SED file';

            dropZone.id = 'sedtemplate_custom_dropzone';
            dropZone.classList = 'dropZone sed-file-dropzone rounded-3';

            button.classList = 'choose-file-button sed-file-button';
            button.textContent = 'Choose';

            message.id = 'sedtemplate_custom_message';
            message.classList = 'file-message sed-file-message';
            message.textContent = 'or drop here';

            fileInput.id = 'sedtemplate_custom_file';
            fileInput.classList = 'file-input';
            fileInput.type = 'file';

            contentInput.id = 'sedtemplate_custom_content';
            contentInput.hidden = true;

            filenameInput.id = 'sedtemplate_custom_filename';
            filenameInput.type = 'hidden';

            dropZone.appendChild(button);
            dropZone.appendChild(message);
            dropZone.appendChild(fileInput);
            div.appendChild(label);
            div.appendChild(dropZone);
            div.appendChild(contentInput);
            div.appendChild(filenameInput);
            father.appendChild(div);

            function readSedFile(file) {
                if (file == undefined) return;

                let reader = new FileReader();
                reader.onload = (event) => {
                    contentInput.value = event.target.result;
                    filenameInput.value = file.name;
                    message.textContent = file.name;
                    document.getElementById('sedtemplate')?.dispatchEvent(new Event('input'));
                };
                reader.onerror = () => {
                    contentInput.value = '';
                    filenameInput.value = '';
                    message.textContent = 'Unable to read file';
                    document.getElementById('sedtemplate')?.dispatchEvent(new Event('input'));
                };
                reader.readAsText(file);
            }

            dropZone.addEventListener('dragover', (event) => {
                event.preventDefault();
                event.stopPropagation();
            });

            dropZone.addEventListener('drop', (event) => {
                event.preventDefault();
                event.stopPropagation();
                readSedFile(event.dataTransfer.files[0]);
            });

            fileInput.addEventListener('change', (event) => {
                readSedFile(event.target.files[0]);
            });
        }
    },
    {
        'name' : 'undefined',
        'create' : (father) => {
            return;
        }
    }
] 

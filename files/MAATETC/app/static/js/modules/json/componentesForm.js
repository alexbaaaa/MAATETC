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
        'name' : 'undefined',
        'create' : (father) => {
            let text  = document.createElement('p');
            text.id = 'sedtemplate_text';
            text.innerText = 'Oops! Something\'s gone wrong with the text file... but you can select them manually.' 
            father.appendChild(text)
        }
    }
] 
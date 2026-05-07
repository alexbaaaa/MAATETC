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
            let values = ['A0V','B0V','F0V','G0V','K0V','M0V','O5V']
            let select = document.createElement('select');
            select.id = 'sedtemplate_pickles';
            select.classList = 'inputAjax';
            values.forEach((value) => {
                let option = document.createElement('option');
                option.value = value;
                option.innerHTML = value;
                select.add(option)
            })
            father.appendChild(select);
        }
    },
    {
        'name' : 'blackbody',
        'create' : (father) => {
            let div = document.createElement('div');
            let input = document.createElement('input');
            let label = document.createElement('label');
            
            div.id = 'sedtemplate_blackbody_div';
            label.htmlFor = 'sedtemplate_blackbody';
            label.id = 'sedtemplate_blackbody_label';
            label.innerHTML = 'Temperature';
            input.type = 'number';
            input.id = 'sedtemplate_blackbody';
            input.classList = 'inputAjax';
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
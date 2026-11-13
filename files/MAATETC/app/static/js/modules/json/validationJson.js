const requiredFields = ['compute', 'texpoSN', 'fluxtype', 'fluxval', 'wvinflux', 'grating', 'sedtemplate', 'moon', 'psf'];
const optionalFields = ['airmass', 'redz', 'breadth', 'fwhmA', 'toverhd'];
const positiveFields = ['texpoSN', 'fluxval', 'seeing', 'area'];
const nonNegativeFields = ['redz', 'breadth', 'fwhmA'];
const allowedValues = {
    compute: ['SN', 'texpo'],
    fluxtype: ['continuum', 'emline'],
    moon: ['dark', 'gray', 'grey', 'bright'],
    psf: ['pointsource', 'extended'],
    grating: ['R300B', 'R300R', 'R500B', 'R500R', 'R1000B', 'R1000R', 'R2000B', 'R2500U', 'R2500V', 'R2500R', 'R2500I'],
    sedtemplate: ['ones', 'pickles', 'blackbody', 'custom']
};

function isEmpty(input) {
    return input.value.trim() === '';
}

function isOptionalEmpty(input) {
    return optionalFields.includes(input.id) && isEmpty(input);
}

function getNumber(input) {
    if (isEmpty(input)) return null;
    return Number(input.value);
}

function getPositiveFieldMessage(input, context) {
    if (input.id === 'texpoSN' && context.computeValue === 'SN') return 'Exposure time must be a positive number.';
    if (input.id === 'texpoSN') return 'Requested S/N must be a positive number.';
    if (input.id === 'fluxval') return 'Flux value must be a positive number.';
    if (input.id === 'seeing') return 'Seeing must be a positive number.';
    if (input.id === 'area') return 'Area must be a positive number.';
    return 'This field must be a positive number.';
}

export let validationJSON = [
    {
        name: 'required',
        appliesTo: (input, context) => {
            return requiredFields.includes(input.id)
                || (input.id === 'seeing' && context.psfValue === 'pointsource')
                || (input.id === 'area' && context.psfValue === 'extended');
        },
        validate: (input) => {
            return isEmpty(input) ? 'This field cannot be empty.' : null;
        }
    },
    {
        name: 'allowed-values',
        appliesTo: (input) => allowedValues[input.id] != undefined,
        validate: (input) => {
            if (isEmpty(input)) return null;
            return allowedValues[input.id].includes(input.value) ? null : 'Select a valid option.';
        }
    },
    {
        name: 'valid-number',
        appliesTo: (input) => positiveFields.includes(input.id) || nonNegativeFields.includes(input.id) || input.id === 'wvinflux' || input.id === 'airmass',
        validate: (input) => {
            if (isOptionalEmpty(input) || isEmpty(input)) return null;
            return Number.isFinite(getNumber(input)) ? null : 'This field must be a valid number.';
        }
    },
    {
        name: 'positive-number',
        appliesTo: (input) => positiveFields.includes(input.id),
        validate: (input, context) => {
            if (isEmpty(input)) return null;

            let value = getNumber(input);
            if (!Number.isFinite(value)) return null;

            return value > 0 ? null : getPositiveFieldMessage(input, context);
        }
    },
    {
        name: 'non-negative-number',
        appliesTo: (input) => nonNegativeFields.includes(input.id),
        validate: (input) => {
            if (isOptionalEmpty(input)) return null;

            let value = getNumber(input);
            if (!Number.isFinite(value)) return null;

            return value >= 0 ? null : 'This field cannot be negative.';
        }
    },
    {
        name: 'airmass-positive',
        appliesTo: (input) => input.id === 'airmass',
        validate: (input) => {
            if (isOptionalEmpty(input)) return null;

            let value = getNumber(input);
            if (!Number.isFinite(value)) return null;

            return value > 0 ? null : 'Air mass must be greater than 0.';
        }
    },
    {
        name: 'wvinflux-range',
        appliesTo: (input) => input.id === 'wvinflux',
        validate: (input, context) => {
            if (isEmpty(input)) return null;

            let selectedGrating = context.gratings.find((element) => element[' name'] == context.gratingValue);
            if (selectedGrating == undefined) return null;

            let wavelength = getNumber(input);
            if (!Number.isFinite(wavelength)) return null;

            let minWavelength = Number(selectedGrating.grating[0]);
            let maxWavelength = Number(selectedGrating.grating[1]);

            if (wavelength < minWavelength || wavelength > maxWavelength) {
                return `Reference wavelength must be between ${minWavelength} and ${maxWavelength} for ${context.gratingValue}.`;
            }

            return null;
        }
    },
    {
        name: 'emline-flux',
        appliesTo: (input) => input.id === 'fluxval',
        validate: (input, context) => {
            if (context.fluxtypeValue !== 'emline' || isEmpty(input)) return null;

            let value = getNumber(input);
            if (!Number.isFinite(value)) return null;

            return value <= 0.1 ? null : 'Emission-line flux must use physical flux values, not magnitudes.';
        }
    },
    {
        name: 'blackbody-temperature',
        appliesTo: (input) => input.id === 'sedtemplate',
        validate: (input) => {
            if (input.value !== 'blackbody') return null;

            let temperatureInput = document.getElementById('sedtemplate_blackbody');
            if (temperatureInput == undefined || temperatureInput.value.trim() === '') return 'Blackbody temperature cannot be empty.';

            let temperature = Number(temperatureInput.value);
            if (!Number.isFinite(temperature)) return 'Blackbody temperature must be a valid number.';

            return temperature > 0 ? null : 'Blackbody temperature must be a positive number.';
        }
    },
    {
        name: 'custom-sed-file',
        appliesTo: (input) => input.id === 'sedtemplate',
        validate: (input) => {
            if (input.value !== 'custom') return null;

            let sedContent = document.getElementById('sedtemplate_custom_content')?.value || '';
            return sedContent.trim() !== '' ? null : 'Select a SED file.';
        }
    }
]

export let validationJSON = [
    {
        name: 'required',
        appliesTo: () => true,
        validate: (input) => {
            return input.value.trim() === '' ? 'This field cannot be empty.' : null;
        }
    },
    {
        name: 'wvinflux-range',
        appliesTo: (input) => input.id === 'wvinflux',
        validate: (input, context) => {
            if (input.value.trim() === '') return null;

            let selectedGrating = context.gratings.find((element) => element[' name'] == context.gratingValue);
            if (selectedGrating == undefined) return null;

            let wavelength = Number(input.value);
            if (!Number.isFinite(wavelength)) return 'Reference wavelength must be a valid number.';

            let minWavelength = Number(selectedGrating.grating[0]);
            let maxWavelength = Number(selectedGrating.grating[1]);

            if (wavelength < minWavelength || wavelength > maxWavelength) {
                return `Reference wavelength must be between ${minWavelength} and ${maxWavelength} for ${context.gratingValue}.`;
            }

            return null;
        }
    }
]

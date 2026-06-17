import {validationJSON} from './json/validationJson.js'
import {RequestHandler} from './requestHandler.js'
/**
 * Clase para mostrar los warnning y validar los datos de entrada
 * 
 */
export class Validation {
    constructor () {
        this.validationJson = validationJSON
        // Special values
        this.gratings = RequestHandler.getGratingsJson()
    }

    validate(data) {
        let inputs = Array.from(data).filter((input) => this.#shouldValidate(input));
        let context = this.#getContext();
        let errors = [];

        inputs.forEach((input) => {
            this.clearField(input);

            let message = this.#getFieldError(input, context);
            if (message != null) {
                errors.push({
                    "name": input.name,
                    "message": message
                });
                this.#showFieldError(input, message);
            }
        });

        return {
            "success": errors.length === 0,
            "errors": errors
        }
    }

    clearField(input) {
        input.classList.remove('field-invalid');
        input.removeAttribute('aria-invalid');
        input.removeAttribute('aria-describedby');

        let errorMessage = document.getElementById(`${input.id}-error`);
        errorMessage?.remove();
    }

    #shouldValidate(input) {
        return !input.disabled && input.offsetParent !== null;
    }

    #getContext() {
        let grating = document.getElementById('grating');

        return {
            "gratings": window.GRATINGS || [],
            "gratingValue": grating?.value
        }
    }

    #getFieldError(input, context) {
        for (let rule of this.validationJson) {
            if (!rule.appliesTo(input, context)) continue;

            let message = rule.validate(input, context);
            if (message != null) return message;
        }

        return null;
    }

    #showFieldError(input, message) {
        let errorMessage = document.createElement('small');
        errorMessage.classList = 'field-error-message';
        errorMessage.id = `${input.id}-error`;
        errorMessage.innerText = message;

        input.classList.add('field-invalid');
        input.setAttribute('aria-invalid', 'true');
        input.setAttribute('aria-describedby', errorMessage.id);
        input.insertAdjacentElement('afterend', errorMessage);
    }

    static isValid(data) {
        return new Validation().validate(data);
    }
}

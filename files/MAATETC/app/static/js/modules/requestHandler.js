import {Validation} from './validation.js'
class RequestHandler {
    constructor (printdata) {
        this.printData = printdata;
    }

    init(dataJson) {
        this.getJsonFromController(dataJson);
    }

    async getJsonFromController(dataJson) {
        await fetch('/etc', {
            "method": 'POST',
            "body": JSON.stringify(dataJson),
            "headers": {
                "content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            this.printData(data);
        })
    }

    static getGratingsJson() {
        fetch('/gratings', {
            "method": 'GET',
            "headers": {
                "content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            window.GRATINGS = data;
            window.dispatchEvent(new CustomEvent('gratingsLoaded', { detail: data }));
        })
    }
}
export {RequestHandler}

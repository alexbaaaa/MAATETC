class RequestHandler {
    constructor (printdata) {
        this.printData = printdata;
    }

    init(dataJson) {
        this.getJsonFromController(dataJson);
    }

    async getJsonFromController(dataJson) {
        try {
            let response = await fetch('/etc', {
                "method": 'POST',
                "body": JSON.stringify(dataJson),
                "headers": {
                    "Content-Type": "application/json"
                }
            });

            let contentType = response.headers.get('content-type') || '';
            if (!contentType.includes('application/json')) {
                throw new Error('The server returned a non-JSON response.');
            }

            let data = await response.json();
            if (!response.ok) {
                data.success = false;
            }

            this.printData(data);
        } catch (error) {
            console.error(error);
            this.printData({
                "success": false,
                "text": "The selected values cannot produce a valid graph. Please adjust the input parameters."
            });
        }
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

class RequestHandler {
    constructor (dataJson, printdata) {
        this.printData = printdata;
        this.init(dataJson);    
    }

    init(dataJson) {
        //console.log("Prueba",dataJson)
        this.getJsonFromController(dataJson);
    }

    getJsonFromController(dataJson) {
        fetch('/etc', {
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
}
export {RequestHandler}
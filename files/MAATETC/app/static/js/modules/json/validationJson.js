// Tengo que darle una vuelta... o varias :( 
export  let validationJSON =  [
        {
            "name" : "wvinflux",
            "success" : true,
            "message" : "Has puesto mal la referencia",
            "validation" : (data, grating) => data >= window.GRATINGS[1]['grating'][0] && data <= GRATINGS[1]['grating'][0]
        },
        {
            "name" : "fluxval",
            "success" : true,
            "message" : "Has puesto mal el valor de flux",
            "validation" : (data) => data === "5000"
        },
    
]
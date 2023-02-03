function getEfficacyColors(insight, metric, value){
    var efficacyClass = getEfficacyClass(insight, metric, value);
    switch(efficacyClass){
        case "danger": return "#e74c3c";
        case "warning": return "#f1c40f";
        case "success": return "#2ecc71";
        case "secondary": return "lightgray";
        default: return "lightgray";
    }
}

function getEfficacyClass(insight, metric, value){
    if(value == undefined || value == null){
        return "secondary";
    }
    switch(insight){
        case "quality_insights": 
            // Handle Freshness Differently
            if(value >= 90){ // high
                return "success"
            }else if(value >=  68){ // medium
                return "warning"
            }else { // low
                return "danger"
            }
        case "usage_insights":
            if(value > 90){ // high
                return "success"
            }else if(value >=  68){ // medium
                return "warning"
            }else { // low
                return "danger"
            }
        default: 
            return "success"
    }
}
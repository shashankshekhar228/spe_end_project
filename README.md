function jsonToXml(json) {
    let xml = '';

    function convert(obj, parentElement) {
        for (let key in obj) {
            if (obj.hasOwnProperty(key)) {
                let value = obj[key];
                if (typeof value === 'object' && !Array.isArray(value)) {
                    xml += `<${key}>`;
                    convert(value, key);
                    xml += `</${key}>`;
                } else if (Array.isArray(value)) {
                    value.forEach(item => {
                        xml += `<${key}>`;
                        convert(item, key);
                        xml += `</${key}>`;
                    });
                } else {
                    xml += `<${key}>${value}</${key}>`;
                }
            }
        }
    }

    if (typeof json === 'object') {
        convert(json, '');
    } else {
        throw new Error('Input must be a valid JSON object');
    }

    return xml;
}

// Example usage
const json = {
    "note": {
        "to": "Tove",
        "from": "Jani",
        "heading": "Reminder",
        "body": "Don't forget me this weekend!",
        "items": [
            {"item": "item1"},
            {"item": "item2"}
        ]
    }
};

console.log(jsonToXml(json));

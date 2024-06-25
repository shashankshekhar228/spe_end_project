function xmlToJson(xml) {
    function parseElement(element) {
        const obj = {};

        // Match opening tag, attributes, and content (including self-closing tags)
        const tagRegex = /^<([\w-]+)([^>]*)>([\s\S]*)<\/\1>$|^<([\w-]+)([^>]*)\/>$/;
        const match = element.match(tagRegex);
        if (!match) return obj;

        const [, tagName, attributes, innerXml, selfClosingTag, selfClosingAttributes] = match;
        if (selfClosingTag) {
            // Handle self-closing tag
            obj[selfClosingTag] = {};
            if (selfClosingAttributes.trim()) {
                // Process attributes
                const attrRegex = /([\w-]+)="([^"]*)"/g;
                let attrMatch;
                while ((attrMatch = attrRegex.exec(selfClosingAttributes)) !== null) {
                    const [, attrName, attrValue] = attrMatch;
                    obj[selfClosingTag]['@attributes'] = obj[selfClosingTag]['@attributes'] || {};
                    obj[selfClosingTag]['@attributes'][attrName] = attrValue;
                }
            }
            return obj;
        }

        obj[tagName] = {};

        // Process attributes
        const attrRegex = /([\w-]+)="([^"]*)"/g;
        let attrMatch;
        while ((attrMatch = attrRegex.exec(attributes)) !== null) {
            const [, attrName, attrValue] = attrMatch;
            obj[tagName]['@attributes'] = obj[tagName]['@attributes'] || {};
            obj[tagName]['@attributes'][attrName] = attrValue;
        }

        // Process inner XML content (child elements or text content)
        const childRegex = /<([\w-]+)([^>]*)>([\s\S]*?)<\/\1>|<([\w-]+)([^>]*)\/>/g;
        let childMatch;
        while ((childMatch = childRegex.exec(innerXml)) !== null) {
            const [, childTagName, childAttributes, childInnerXml, selfClosingChildTag, selfClosingChildAttributes] = childMatch;
            if (selfClosingChildTag) {
                // Handle self-closing child tag
                const childElement = `<${selfClosingChildTag}${selfClosingChildAttributes}/>`;
                const childObj = parseElement(childElement);

                if (obj[tagName][selfClosingChildTag]) {
                    if (!Array.isArray(obj[tagName][selfClosingChildTag])) {
                        obj[tagName][selfClosingChildTag] = [obj[tagName][selfClosingChildTag]];
                    }
                    obj[tagName][selfClosingChildTag].push(childObj[selfClosingChildTag]);
                } else {
                    obj[tagName][selfClosingChildTag] = childObj[selfClosingChildTag];
                }
                continue;
            }

            const childElement = `<${childTagName}${childAttributes}>${childInnerXml}</${childTagName}>`;
            const childObj = parseElement(childElement);

            if (obj[tagName][childTagName]) {
                if (!Array.isArray(obj[tagName][childTagName])) {
                    obj[tagName][childTagName] = [obj[tagName][childTagName]];
                }
                obj[tagName][childTagName].push(childObj[childTagName]);
            } else {
                obj[tagName][childTagName] = childObj[childTagName];
            }
        }

        // If no child elements, store inner text content
        if (!Object.keys(obj[tagName]).length) {
            obj[tagName] = innerXml.trim();
        } else {
            // If there are child elements, check for mixed content
            const textContent = innerXml.replace(childRegex, '').trim();
            if (textContent) {
                obj[tagName]['#text'] = textContent;
            }
        }

        return obj;
    }

    // Clean up the XML string
    const cleanedXml = xml.replace(/\n/g, '').replace(/\s{2,}/g, ' ').trim();

    // Find the root element
    const rootElementMatch = cleanedXml.match(/<([\w-]+)([^>]*)>([\s\S]*?)<\/\1>|<([\w-]+)([^>]*)\/>/);
    if (!rootElementMatch) return {};

    return parseElement(rootElementMatch[0]);
}

// Example usage
const xml = `
<note>
  <to>Tove</to>
  <from>Jani</from>
  <heading>Reminder</heading>
  <body>
    <ar><title>Don't forget me this weekend!</title></ar>
    <ar><title>divsbi</title></ar>
  </body>
  <selfClosingTag attribute="value"/>
</note>
`;

const json = xmlToJson(xml);
console.log(JSON.stringify(json, null, 2));
console.log(json.note.to);

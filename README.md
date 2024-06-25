 function xmlToJson(xml) {
    function parseElement(xml) {
        const obj = {};

        // Match opening tag, attributes, and content (including self-closing tags)
        const tagRegex = /<([\w-]+)([^>]*)>([\s\S]*?)<\/\1>|<([\w-]+)([^>]*)\/>/;
        const match = xml.match(tagRegex);
        if (!match) return xml.trim(); // Return text content directly if no match

        const [, tagName, attributes, innerXml, selfClosingTag, selfClosingAttributes] = match;
        const currentTag = tagName || selfClosingTag;
        const currentAttributes = attributes || selfClosingAttributes;

        obj[currentTag] = {};

        // Process attributes
        if (currentAttributes) {
            const attrRegex = /([\w-]+)="([^"]*)"/g;
            let attrMatch;
            while ((attrMatch = attrRegex.exec(currentAttributes)) !== null) {
                const [, attrName, attrValue] = attrMatch;
                obj[currentTag]['@attributes'] = obj[currentTag]['@attributes'] || {};
                obj[currentTag]['@attributes'][attrName] = attrValue;
            }
        }

        if (selfClosingTag) {
            // Handle self-closing tag
            return obj;
        }

        // Process inner XML content (child elements or text content)
        const childRegex = /<([\w-]+)([^>]*)>([\s\S]*?)<\/\1>|<([\w-]+)([^>]*)\/>/g;
        let childMatch;
        let textContent = '';

        while ((childMatch = childRegex.exec(innerXml)) !== null) {
            const [, childTagName, childAttributes, childInnerXml, selfClosingChildTag, selfClosingChildAttributes] = childMatch;
            const childElement = childMatch[0];
            const childObj = parseElement(childElement);

            if (obj[currentTag][childTagName]) {
                if (!Array.isArray(obj[currentTag][childTagName])) {
                    obj[currentTag][childTagName] = [obj[currentTag][childTagName]];
                }
                obj[currentTag][childTagName].push(childObj[childTagName]);
            } else {
                obj[currentTag][childTagName] = childObj[childTagName];
            }
        }

        // Check for text content if no child elements
        if (!Object.keys(obj[currentTag]).length && innerXml.trim()) {
            textContent = innerXml.trim();
        }

        if (textContent) {
            obj[currentTag]['#text'] = textContent;
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

// Example usage:
const xmlString = `
<status>
  <result>success</result>
  <status>success</status>
</status>
`;

const jsonObj = xmlToJson(xmlString);
console.log(JSON.stringify(jsonObj, null, 2));

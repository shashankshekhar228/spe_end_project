function xmlToJson(xml) {
    function parseElement(element) {
        const obj = {};

        // Match opening tag, attributes, and content (including self-closing tags)
        const tagRegex = /^<([\w-]+)([^>]*)>([\s\S]*?)<\/\1>$|^<([\w-]+)([^>]*)\/>$/;
        const match = element.match(tagRegex);
        if (!match) return obj;

        const [, tagName, attributes, innerXml, selfClosingTag, selfClosingAttributes] = match;
        const currentTag = tagName || selfClosingTag;
        const currentAttributes = attributes || selfClosingAttributes;

        obj[currentTag] = {};

        // Process attributes
        const attrRegex = /([\w-]+)="([^"]*)"/g;
        let attrMatch;
        while ((attrMatch = attrRegex.exec(currentAttributes)) !== null) {
            const [, attrName, attrValue] = attrMatch;
            obj[currentTag]['@attributes'] = obj[currentTag]['@attributes'] || {};
            obj[currentTag]['@attributes'][attrName] = attrValue;
        }

        if (selfClosingTag) {
            // Handle self-closing tag
            return obj;
        }

        // Process inner XML content (child elements or text content)
        const childRegex = /<([\w-]+)([^>]*)>([\s\S]*?)<\/\1>|<([\w-]+)([^>]*)\/>/g;
        let childMatch;
        while ((childMatch = childRegex.exec(innerXml)) !== null) {
            const [, childTagName, childAttributes, childInnerXml, selfClosingChildTag, selfClosingChildAttributes] = childMatch;
            const childElement = `<${childTagName || selfClosingChildTag}${childAttributes || selfClosingChildAttributes}${selfClosingChildTag ? ' /' : ''}>${childInnerXml || ''}</${childTagName || selfClosingChildTag}>`;
            const childObj = parseElement(childElement);

            const tagName = childTagName || selfClosingChildTag;
            if (obj[currentTag][tagName]) {
                if (!Array.isArray(obj[currentTag][tagName])) {
                    obj[currentTag][tagName] = [obj[currentTag][tagName]];
                }
                obj[currentTag][tagName].push(childObj[tagName]);
            } else {
                obj[currentTag][tagName] = childObj[tagName];
            }
        }

        // If no child elements, store inner text content
        if (!Object.keys(obj[currentTag]).length) {
            obj[currentTag] = innerXml.trim();
        } else {
            // If there are child elements, check for mixed content
            const textContent = innerXml.replace(childRegex, '').trim();
            if (textContent) {
                obj[currentTag]['#text'] = textContent;
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
  <abc>shashank</abc>
</note>
`;

const json = xmlToJson(xml);
console.log(JSON.stringify(json, null, 2));
console.log(json.note.to);

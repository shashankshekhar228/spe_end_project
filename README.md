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
        const children = [];
        let lastIndex = 0;
        while ((childMatch = childRegex.exec(innerXml)) !== null) {
            children.push({ match: childMatch, index: childMatch.index });
            lastIndex = childMatch.index + childMatch[0].length;
        }

        if (children.length) {
            for (let i = 0; i < children.length; i++) {
                const { match, index } = children[i];
                const [, childTagName, childAttributes, childInnerXml, selfClosingChildTag, selfClosingChildAttributes] = match;
                const childElement = innerXml.substring(index, index + match[0].length);
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

            // If there are child elements, check for mixed content
            const textContent = innerXml.slice(lastIndex).trim();
            if (textContent) {
                obj[currentTag]['#text'] = textContent;
            }
        } else {
            // If no child elements, store inner text content
            obj[currentTag] = innerXml.trim();
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

let xml = '<root><abc:def>content</abc:def><abc:ghi>more content</abc:ghi></root>';

let cleanedXml = xml.replace(/\n/g, '').replace(/\s{2,}/g, ' ').trim();
cleanedXml = cleanedXml.replace(/<([^>]+):([^>]+)>/g, '<$2>').replace(/<\/([^>]+):([^>]+)>/g, '</$2>');

console.log(cleanedXml);

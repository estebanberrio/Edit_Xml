from lxml import etree
from datetime import datetime

# variable que se carga por medio del web services
value1 = "107967752"
value2 = ""
value3 = ""

# Obtener la fecha y hora actual
now = datetime.now()
# Formatear la fecha y hora en el formato deseado
formatted_date = now.strftime("%Y%m%d_%H%M%S")

# ruta archivo original
input_file_path = 'X:\\Solicitudes\\Documentos para xml\\XML_Original.xml'
# ruta archivo modificado
output_file_path = 'X:\\Solicitudes\\Documentos para xml\\XML_Modificado_{0}.xml'.format(formatted_date)

# Definir el mapeo de namespaces
nsmap = {
    'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
    'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'
}

# Leer el archivo XML
tree = etree.parse(input_file_path)
root = tree.getroot()

# Recorrer solo lo que está dentro de los tag invoiceLine
for invoice_line in root.xpath('.//cac:invoiceline', namespaces=nsmap):
    # Modificar atributos 'schemeid'
    for id_tag in invoice_line.xpath('.//cbc:id[@schemeid="0" or @schemeid="999"]', namespaces=nsmap):
        id_tag.attrib['schemeid'] = "1"

    # Función para actualizar los atributos 'unitcode' y multiplicar su valor por 1000
    def update_quantity(tag_name):
        for tag in invoice_line.xpath('.//cbc:' + tag_name + '[@unitcode="NT"]', namespaces=nsmap):
            tag.attrib['unitcode'] = "KGM"
            tag.text = str(int(tag.text) * 1000)
            if tag_name == "basequantity":
                value2 = tag.text

    # Actualizar 'invoicedquantity', 'valuequantity', 'basequantity'
    update_quantity('invoicedquantity')
    update_quantity('valuequantity')
    update_quantity('basequantity')

    # Modificar <cac:sellersitemidentification>
    for seller in invoice_line.xpath('.//cac:sellersitemidentification', namespaces=nsmap):
        id_tag = seller.find('.//cbc:id', namespaces=nsmap)
        if id_tag is not None:
            id_tag.text = id_tag.text.replace("-", "-2-")
            value3 = id_tag.text

    # Modificar y agregar etiquetas en <cac:item>
    for item in invoice_line.xpath('.//cac:item', namespaces=nsmap):
        names_values = [("01", value1), ("02", value2), ("03", value3)]
        additional = item.find('.//cac:additionalitemproperty', namespaces=nsmap)
        for name, value in names_values:
            additional_item_property = etree.SubElement(additional, 'cac:AdditionalItemProperty')
            name_tag = etree.SubElement(additional_item_property, 'cbc:Name')
            name_tag.text = name
            value_tag = etree.SubElement(additional_item_property, 'cbc:Value')
            value_tag.text = value

# Escribe el XML seguro en el archivo
with open(output_file_path, 'wb') as f:
    f.write(etree.tostring(tree, pretty_print=True, encoding='utf-8'))

import os
from datetime import datetime
import lxml.etree as etree

# Variable que se carga por medio del web services
value1 = "107967752"

# Obtener la fecha y hora actual
now = datetime.now()
# Formatear la fecha y hora en el formato deseado
formatted_date = now.strftime("%Y%m%d_%H%M%S")

# Ruta archivo original
input_file_path = 'X:\\Solicitudes\\Documentos para xml\\XML_Original.xml'

# Ruta archivo modificado
output_file_path = f'X:/Solicitudes/Documentos para xml/XML_Modificado_{0}.xml'.format(formatted_date)

# Valida si el archivo existe
if not os.path.isfile(input_file_path): raise FileNotFoundError("El archivo: {input_file_path} no existe")

# Valida si el archivo se puede leer
if not os.access(input_file_path, os.R_OK): raise PermissionError("No se tiene permiso para leer el archivo: {input_file_path}")

# Leer el archivo XML
#with open(input_file_path, 'r', encoding='utf-8') as f: contents = f.read()

# Utilizar el parser 'lxml' para XML
tree = etree.parse(input_file_path)
root = tree.getroot()

namespaces = {'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2', 'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'}

# Buscar todas las etiquetas 'invoiceline' en el archivo XML
invoice_lines = root.xpath('cac:InvoiceLine', namespaces=namespaces)
print(len(invoice_lines))

# Recorrer solo lo que esta dentro de los tag invoiceLine
for invoice_line in invoice_lines:
    # Buscar todas las etiquetas 'ID' en el archivo XML
    ids = invoice_line.findall('cbc:ID')
    print(len(ids))

    # Validar que existan datos
    if ids:
        # Recorrer cada etiqueta 'ID'
        for id in ids:
            # Si el atributo 'schemeid' es igual a 0 o a 999, cambio a 1
            if id.get('schemeid') == "0" or id.get('schemeid') == "999":
                id['schemeid'] = "1"

    # Buscar todas las etiquetas 'quantitys' en el archivo XML
    quantitys = invoice_line.findall('cbc:invoicedquantity')

    # Validar que existan datos
    if quantitys:
        # Recorrer cada etiqueta 'quantity'
        for quantity in quantitys:
            # Si el atributo 'quantitys' es igual a 'NT', cambiarlo a 'KGM'
            if quantity.get('unitcode') == "NT":
                quantity['unitcode'] = "KGM"
                # Cambiar el value multiplicandolo por 1k
                quantity_value = quantity.text
                invoicedquantity = int(quantity_value) * 1000
                new_quantity = etree.Element('cbc:InvoicedQuantity')
                new_quantity.text = str(invoicedquantity)
                quantity.append(new_quantity)

    # Buscar todas las etiquetas 'valuequantitys' en el archivo XML
    valuequantitys = invoice_line.findall('cbc:valuequantity')

    # Validar que existan datos
    if valuequantitys:
        # Recorrer cada etiqueta 'valuequantitys'
        for valuequantity in valuequantitys:
            # Si el atributo 'unitcode' es igual a 'NT', cambiarlo a 'KGM'
            if valuequantity.get('unitcode') == "NT":
                valuequantity['unitcode'] = "KGM"
                # Cambiar el value multiplicandolo por 1k
                valuequantity_value = valuequantity.text
                tag_valuequantity = int(valuequantity_value) * 1000
                new_valuequantity = etree.Element('cbc:ValueQuantity')
                new_valuequantity.text = str(tag_valuequantity)
                valuequantity.append(new_valuequantity)

    # Buscar todas las etiquetas 'unitcode' en el archivo XML
    basequantitys = invoice_line.findall('cbc:basequantity')
    # Validar que existan datos
    if len(basequantitys) != 0:
        # Recorrer cada etiqueta 'basequantitys'
        for basequantity in basequantitys:
            # Si el atributo 'unitcode' es igual a 'NT', cambiarlo a 'KGM'
            if basequantity.get('unitcode') == "NT":
                basequantity['unitcode'] = "KGM"
                #cambiar el value multiplicandolo por 1k
                basequantity_value = basequantity.text
                tag_basequantity = int(basequantity_value) * 1000
                value3 = str(tag_basequantity)
                new_basequantity = etree.Element('cbc:BaseQuantity')
                new_basequantity.text = value3
                basequantity.append(new_basequantity)

    # Busca el nodo <cac:sellersitemidentification>
    sellers = invoice_line.findall('cac:sellersitemidentification')
    for seller in sellers:
        id_tag = seller.find('cbc:id')
        if id_tag is not None:
            new_id_value = id_tag.text.replace("-", "-2-")
            value2 = new_id_value
            id_tag.text = new_id_value

    # Busca el nodo <cac:Item>
    items = invoice_line.xpath('.//cac:Item', namespaces=namespaces)
    # si <cac:Item> existe
    if items is not None:
        for item in items:
            # Array con datos temporales para testear
            names_values = [("01", value1), ("02", value2), ("03", value3)]
            # Buscar la additionalitemproperty etiqueta en el nodo
            additional = item.find('cac:additionalitemproperty')
            # Crea una nueva etiqueta <cac:AdditionalItemProperty>
            additional_item_property = etree.Element('cac:AdditionalItemProperty')
            # ciclo de recorrido de creación de tag
            for name, value in names_values:
                # Crea una etiqueta <cbc:Name> y añade el nombre
                name_tag = etree.Element('cbc:Name')
                name_tag.text = name
                additional_item_property.append(name_tag)
                # Crea una etiqueta <cbc:Value> y añade el valor
                value_tag = etree.Element('cbc:Value')
                value_tag.text = value
                additional_item_property.append(value_tag)
                # Añade la etiqueta <cac:AdditionalItemProperty> al nodo <cac:Item>
            additional.append(additional_item_property)
            
            
    # Genera el XML como un string
    xml = str(invoice_lines)

    # buscar caracteres a eliminar
    xml = xml.replace(']]&gt;', '')
    # buscar caracteres a eliminar
    xml = xml.replace('<html>', '')
    # buscar caracteres a eliminar
    xml = xml.replace('<body>', '')
    # buscar caracteres a eliminar
    xml = xml.replace('</html>', '')
    # buscar caracteres a eliminar
    safe = xml.replace('</body>', '')        

#Escribe el XML seguro en el archivo
#safe.write(output_file_path, pretty_print=False, encoding='utf-8')

#Escribe el XML seguro en el archivo
#with open(output_file_path, 'r') as f: f.write(safe)
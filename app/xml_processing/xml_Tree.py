import xml.etree.ElementTree as ET
from datetime import datetime

def xml_convert():
    # Variable que se carga por medio del web services
    value1 = "107967752"

    # Obtener la fecha y hora actual
    now = datetime.now()
    # Formatear la fecha y hora en el formato deseado
    formatted_date = now.strftime("%Y%m%d_%H%M%S")

    # Leer el archivo XML
    input_file_path = 'X:/Solicitudes/Documentos para xml/XML_Original.xml'
    output_file_path = 'X:/Solicitudes/Documentos para xml/XML_Modificado_{0}.xml'.format(formatted_date)
    
    # cargar archivo en variable
    with open(input_file_path, 'r', encoding='utf-8') as f:
        contents = f.read()

    # asignacion del archivo
    root = ET.fromstring(contents)
    
    # Genera el XML como un string
    xml = ET.tostring(root, encoding='utf-8', xml_declaration=True).decode()

    # buscar caracteres a eliminar
    xml1 = xml.replace(']]&gt;', '')
    # buscar caracteres a eliminar
    xml2 = xml1.replace('<html>', '')
    # buscar caracteres a eliminar
    xml3 = xml2.replace('<body>', '')
    # buscar caracteres a eliminar
    xml4 = xml3.replace('</html>', '')
    # buscar caracteres a eliminar
    safe = xml4.replace('</body>', '')
    
    safe = ET.fromstring(safe)
    
    # Busqueda tag invoice_line
    invoice_lines = safe.findall('cac:invoiceline')
    print(len(invoice_lines))
    
    # Recorrer las etiquetas 'invoiceline'
    for invoice_line in invoice_lines:
        # Obtener todas las etiquetas 'ID'
        for id in invoice_line.findall('cbc:id'):
            # Si el atributo 'schemeid' es igual a 0 o a 999, cambiar a 1
            if id.get('schemeid') == "0" or id.get('schemeid') == "999":
                id.set('schemeid', "1")

        # Obtener todas las etiquetas 'quantitys'
        for quantity in invoice_line.findall('.//cbc:invoicedquantity'):
            # Si el atributo 'quantitys' es igual a 'NT', cambiarlo a 'KGM'
            if quantity.get('unitcode') == "NT":
                quantity.set('unitcode', "KGM")
                # Cambiar el valor multiplicando por 1k
                quantity_value = quantity.text
                invoicedquantity = int(quantity_value) * 1000
                quantity.text = str(invoicedquantity)

        # Obtener todas las etiquetas 'valuequantitys'
        for valuequantity in invoice_line.findall('bc:valuequantity'):
            # Si el atributo 'unitcode' es igual a 'NT', cambiarlo a 'KGM'
            if valuequantity.get('unitcode') == "NT":
                valuequantity.set('unitcode', "KGM")
                # Cambiar el valor multiplicando por 1k
                valuequantity_value = valuequantity.text
                tag_valuequantity = int(valuequantity_value) * 1000
                valuequantity.text = str(tag_valuequantity)

        # Obtener todas las etiquetas 'unitcode'
        for basequantity in invoice_line.findall('cbc:basequantity'):
            # Si el atributo 'unitcode' es igual a 'NT', cambiarlo a 'KGM'
            if basequantity.get('unitcode') == "NT":
                basequantity.set('unitcode', "KGM")
                # Cambiar el valor multiplicando por 1k
                basequantity_value = basequantity.text
                tag_basequantity = int(basequantity_value) * 1000
                basequantity.text = str(tag_basequantity)

        # Busca el nodo <cac:sellersitemidentification>
        for seller in invoice_line.findall('cac:sellersitemidentification'):
            id_tag = seller.find('cbc:id')
            if id_tag is not None:
                new_id_value = id_tag.text.replace("-", "-2-")
                id_tag.text = new_id_value

        # Busca el nodo <cac:Item>
        for item in invoice_line.findall('cac:item'):
            # Array con datos temporales para testear
            names_values = [("01", value1), ("02", new_id_value), ("03", basequantity.text)]

            # Buscar la etiqueta <cac:AdditionalItemProperty> en el nodo
            additional = item.find('cac:additionalitemproperty')

            # Crea una nueva etiqueta <cac:AdditionalItemProperty>
            additional_item_property = ET.SubElement(additional, 'cac:AdditionalItemProperty')

            # ciclo de recorrido de creación de etiquetas
            for name, value in names_values:
                # Crea una etiqueta <cbc:Name> y añade el nombre
                name_tag = ET.SubElement(additional_item_property, 'cbc:Name')
                name_tag.text = name

                # Crea una etiqueta <cbc:Value> y añade el valor
                value_tag = ET.SubElement(additional_item_property, 'cbc:Value')
                value_tag.text = value

            # Añade la etiqueta <cac:AdditionalItemProperty> al nodo <cac:Item>
            additional.append(additional_item_property)

    # Escribir el XML en el archivo
    #with open(output_file_path, 'w', encoding='utf-8') as f: f.write(str(safe))

# Llamada a la función
xml_convert()
from bs4 import BeautifulSoup
from datetime import datetime

#variable que se carga por medio del web services
value1 = "107967752"

# Obtener la fecha y hora actual
now = datetime.now()
# Formatear la fecha y hora en el formato deseado
formatted_date = now.strftime("%Y%m%d_%H%M%S")

# ruta archivo original
input_file_path = 'X:\Solicitudes\Documentos para xml\XML_Original.xml'
# ruta archivo modificado
output_file_path = 'X:\Solicitudes\Documentos para xml\XML_Modificado_{0}.xml'.format(formatted_date)

# Leer el archivo XML
with open('X:\Solicitudes\Documentos para xml\XML_Original.xml', 'r', encoding='utf-8') as f: contents = f.read()

# Utilizar el parser 'lxml' para XML
soup = BeautifulSoup(contents)  

# Buscar todas las etiquetas 'invoiceline' en el archivo XML
invoice_lines = soup.find_all('cac:invoiceline')

# Recorrer solo lo que esta dentro de los tag invoiceLine
for invoice_line in invoice_lines:
    # Buscar todas las etiquetas 'ID' en el archivo XML
    ids = invoice_line.find_all('cbc:id') 
    # Validar que existan datos
    if(len(ids)!=0):
        # Recorrer cada etiqueta 'ID'
        for id in ids:
            # Si el atributo 'schemeid' es igual a 0 o a 999, cambio a 1
            if id.get('schemeid') == "0" or  id.get('schemeid') == "999":
                id['schemeid'] = "1"

    # Buscar todas las etiquetas 'quantitys' en el archivo XML
    quantitys = invoice_line.find_all('cbc:invoicedquantity') 
    # Validar que existan datos
    if(len(quantitys)!=0):
        # Recorrer cada etiqueta 'quantity'
        for quantity in quantitys:
            # Si el atributo 'quantitys' es igual a 'NT', cambiarlo a 'KGM'
            if quantity.get('unitcode') == "NT":
                quantity['unitcode'] = "KGM"
                #cambiar el value multiplicandolo por 1k
                quantity_value = quantity.text 
                invoicedquantity = (int(quantity_value) * 1000)
                new_quantity = soup.new_string(str(invoicedquantity))
                quantity.string = str(new_quantity)

    # Buscar todas las etiquetas 'valuequantitys' en el archivo XML
    valuequantitys = invoice_line.find_all('cbc:valuequantity') 
    # Validar que existan datos
    if(len(valuequantitys)!=0):
        # Recorrer cada etiqueta 'valuequantitys'
        for valuequantity in valuequantitys:
            # Si el atributo 'unitcode' es igual a 'NT', cambiarlo a 'KGM'
            if valuequantity.get('unitcode') == "NT":
                valuequantity['unitcode'] = "KGM"
                #cambiar el value multiplicandolo por 1k
                valuequantity_value = valuequantity.text            
                tag_valuequantity = (int(valuequantity_value) * 1000)
                new_valuequantity = soup.new_string(str(tag_valuequantity))
                valuequantity.string = str(new_valuequantity)

    # Buscar todas las etiquetas 'unitcode' en el archivo XML
    basequantitys = invoice_line.find_all('cbc:basequantity') 
    # Validar que existan datos
    if(len(basequantitys)!=0):
        # Recorrer cada etiqueta 'basequantitys'
        for basequantity in basequantitys:
            # Si el atributo 'unitcode' es igual a 'NT', cambiarlo a 'KGM'
            if basequantity.get('unitcode') == "NT":
                basequantity['unitcode'] = "KGM"
                #cambiar el value multiplicandolo por 1k
                basequantity_value = basequantity.text 
                tag_basequantity = (int(basequantity_value) * 1000)
                value3 = str(tag_basequantity)
                new_basequantity = soup.new_string(str(tag_basequantity))
                basequantity.string = str(new_basequantity)

    # Busca el nodo <cac:sellersitemidentification>
    sellers = invoice_line.find_all('cac:sellersitemidentification')
    for seller in sellers:
        id_tag = seller.find('cbc:id')
        if id_tag is not None:
            new_id_value = id_tag.text.replace("-", "-2-")
            value2 = new_id_value
            id_tag.string = new_id_value

    # Busca el nodo <cac:Item>
    items = invoice_line.find_all('cac:item')    
    # si <cac:Item> existe
    if items is not None:
        for item in items:
            # Array con datos temporales para testear
            names_values = [("01", value1), ("02", value2), ("03", value3)]
            # Buscar la additionalitemproperty etiqueta en el nodo
            additional = item.find('cac:additionalitemproperty')
            # Crea una nueva etiqueta <cac:AdditionalItemProperty>
            additional_item_property = soup.new_tag('cac:AdditionalItemProperty')
            # ciclo de recorrido de creación de tag
            for name, value in names_values:                
                # Crea una etiqueta <cbc:Name> y añade el nombre
                name_tag = soup.new_tag('cbc:Name')
                name_tag.string = name
                additional_item_property.append(name_tag)
                # Crea una etiqueta <cbc:Value> y añade el valor
                value_tag = soup.new_tag('cbc:Value')
                value_tag.string = value
                additional_item_property.append(value_tag)
                # Añade la etiqueta <cac:AdditionalItemProperty> al nodo <cac:Item>
            additional.append(additional_item_property)

    # Genera el XML como un string
    xml = str(soup)

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

# Escribe el XML seguro en el archivo
with open(output_file_path, 'w', encoding='utf-8') as f: f.write(str(safe))
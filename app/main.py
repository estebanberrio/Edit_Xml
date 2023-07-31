import sys
from xml_processing import xml_convert
from xml_processing import xml_convert2

def main():
    #xml_convert.xml_convert()
    xml_convert2.xml_convert2()

if __name__ == "__main__":
    sys.path.append("xml_processing")


    main()
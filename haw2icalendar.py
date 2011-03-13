from hawParser import HawParser
from hawDispatchProcessor import HawDispatchProcessor

if __name__ == "__main__":
    file = open("/home/theno/hawicalendar/muster.txt", "r")
    text = file.read()
    file.close()
    
    success, resultList, strIndex = HawParser.parse(text, processor=HawDispatchProcessor())
    ereignisList = resultList[0]
    
    print "result:"
    for e in ereignisList:
        print e

    # filtern

    # icalendar erzeugen
    # ausgeben

    


from googletrans import Translator

#fonction de traduction 
def trad(text):

    try:
        translator=Translator()
        traduction=translator.translate(text,dest='fr')
        return traduction.text
    
    except Exception as e:
        return({"Error during the traduction":str(e)})
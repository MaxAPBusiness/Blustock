class Auto():
    def __init__(self):
        self.color="Negro"
        self.ruedas= 4
        self.ventanas= 8
        self.patente=""
        self.motor="A gas"
        self.cajaDeCambios="Manual"
        self.palancaDeCambios=False
        self.encendido=False
        self.guinoIzquierdo=False
        self.guinoDerecho=False
        self.balizas=False
    
    def encender(self):
        print("Se encendió el auto")
        self.encendido=True
    
    def acelerar(self):
        if self.encendido:
            print("Se aeleró el auto y está empezando a tirar cortes")
        else:
            print("Prendé el auto antes de acelerar, boludo")
    
    def puntoMuerto(self):
        print("El auto está parado y en punto muerto")
    
    def apagar(self):
        print("El auto se apagó")
        self.apagar=True
    
    def prenderBalizas(self):
        if self.encendido:
            print("Se prendieron las balizas")
            self.balizas=True
        else:
            print("Prendè el auto, forro.")

    
    def apagarBalizas(self):
        print("Se apagaron las balizas")
        self.balizas=False
    
    def encenderGuinoIzquierdo(self):
        print("Se encendió el guiño izquierdo")
        self.guinoIz=True
    
    def encenderGuinoDerecho(self):
        print("Se encendió el guiño derecho")
        self.guinoDerecho=True

tiziConchudo=Auto()
tiziConchudo.color="Gris bordó"
tiziConchudo.patente="AG 000 AA"
tiziConchudo.motor="Eléctrico"
tiziConchudo.cajaDeCambios="Automático"
tiziConchudo.encender()
tiziConchudo.acelerar()
tiziConchudo.encenderGuinoIzquierdo()
tiziConchudo.encenderGuinoDerecho()
tiziConchudo.apagar()
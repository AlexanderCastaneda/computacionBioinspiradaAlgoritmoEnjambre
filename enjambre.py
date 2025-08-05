## pip install pygame


'''
Importacn de la libreria pygame con el objetivo de ayudar a la gestion de graficos en 2 d
aporta funcionalidades como grafico y sprites, gestion de eventos, soporte multiplataforma
'''
import pygame
'''
Importacion de libreria random Creacion de intervalos numerico aleatorios, simulaciones de sistemas, crear movimientos aleatorios
y distribuciones de elemento aleatorios.
'''
import random
import math

# ----------------------- Configuración Inicial -----------------------

'''
En esta configuracion inicial, se establece el ancho y alto de la ventana de ejecucion tambien el numero de peces que se van a renderizar,
por otro lado, el radio de vision de los peces y la velocidad maxima que pude alcanzar un pez, tambien la distancia de separacion entre peces y las distancia a la
que el pez inicia la huida del mouse (Tiburon), es importante detallar el valor de cada constante se establece como enteres logicamente, pero su representacion
de unidades de medidas en el motor grafico se define como pixeles...
Ejemplo DISTACIA_SEPARACION = 20 px =D.
'''
ANCHO, ALTO = 800, 600
NUM_PECES = 30 # exepto esta se marca como la cantidad de peces >.<
RADIO_VISION = 100
VELOCIDAD_MAXIMA = 2
DISTANCIA_SEPARACION = 20
DISTANCIA_HUIDA = 100


#Creacion de la clase pez
class Pez:
    def __init__(self, x, y):
        '''
        Ensta funcion, actua como constructor de los pescados
        estleciendo por medio de sefl.pos la posicion de creacion del pescado y se han,
        de guardar las pociciones respecto a la creacion de cada pez de forma independiente.
        Por otro lado, self.vel estable una de desplazamiento aleatoria para el pez donde esta
        se enmarca en un intervalo de -1 y 1.
        '''
        # Posición y velocidad inicial agrupada
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))

    def actualizar(self, peces, tiburon_pos):
        '''
        Esta funicon es la responsable del comportamien de los peces en base a sus vecinos
        se establecen 6 variables donde:
        Cohesion: actua como fuerza que obliga al pez a buscar el centro de sus vecinos, generando de cierto modo la aglomeracion del cardumen (puntos), 
             pygame.Vector2 actua como un tipo de dato que almacen los datos del vector en este caso una posicion bidimencional.
        Separacion: Para este caso se establece con el objetivo de evitar coliciones entre los peces pero si que se distancien de forma abrupta los unos de los otros
        Alineación: Se implementa con el objetivo de mantener una velocidad par a la del resto de integrantes del cardumen.
        Total: Esto se implementa como un cotandor, cuyo obejtivo sirve a cada pez para motinerear cuantos peces tiene proximos a su radio de vision, en base a este contardor
            se establece los valore de cohesion, separacion y alineacion.
        '''
        cohesion = pygame.Vector2(0, 0)
        separacion = pygame.Vector2(0, 0)
        alineacion = pygame.Vector2(0, 0)
        total = 0

        # Regla de evasión del tiburón (el mouse)

        '''
        la siguente dos variables se establen con el objetiv de evadir el cursor (tiburon) en base a la distancia de aproximacion de este este mismo (distancia_al_tiburon)
        '''
        evadir = pygame.Vector2(0, 0)
        distancia_al_tiburon = self.pos.distance_to(tiburon_pos)
        '''
        En el primer condicional se implementa con el objetivo de activar la evasion por parte de los peces hacia el tiburon.
        es decir si... distancia_al_tiburon es menor que DISTANCIA_HUIDA se actualizar los valores de la variable evadir. Donde
        evadir sera igual a la posicion del pez menos la posicion del tiburon 🦈

        Por otro lado esta la linea  evadir.scale_to_length(VELOCIDAD_MAXIMA * 2) en esta parte del codig sabemos que evadir es un pygame.Vector2, por consiguente,
        representa un direccion enla que el pez debe huir del tiburon, cabe recalcar que la longitud de este vector es la distancia actual del pez y el tiburon
        donde los peces buscaran mantenerse alejados del tiburon es decir una distancia mayor a 100 px. En si se busca establecer una velocidad de huida al multiplicar la velocidad maxima por 2
        donde esta velocidad mazima llegaria a ser igual a 4
        '''

        if distancia_al_tiburon < DISTANCIA_HUIDA:
            # Huir del tiburón
            evadir = self.pos - tiburon_pos
            evadir.scale_to_length(VELOCIDAD_MAXIMA * 2)

        # Reglas de comportamiento del cardumen
        '''
        A continuacion esta un ciclor for se inica a hacer una comparacion para poder realizar el comportamiento de los peces, en caso qeu un pez de la lista peces,
        por consiguiente, un pez no puede interactuarl con sigo mismo, entonces si otro (pez de la posicion 0 de la lista de peces) es igual a 0 (0 como referecia
        de laposicion en memorioa dentro de la lista), da a enteder que un pez no puede intaractuar con sigo mismo po rlo cual xontinua y no se ejecuta el resto del
        bloque del if, de lo contario se establece una distacia, para el pez en base a la posicion del otro.
        '''
        for otro in peces:
            if otro == self:
                continue
            distancia = self.pos.distance_to(otro.pos)

            '''
            En este if se busca analizar sila distancia es menor que el RADIO_VISION, recordado que el radio de vision de los peces es de 100 px, si esto se evalua como
            verdadero la coecion y alineacion ha de acumularse, donde otro es un pez de la lista que esta haciendo comparaciones con los peces en su
            alrededor.
            Dentor de este if se encuetra otro if anidado, donde si sel logra cumplir esa primera condicion, se pasa a anlizar la distancia de separacion, por lo tanto la
            variable distancia tiene un determinado valor vectorial para este momento de la iteracion si este valor de distancia es menor que la DISTACIA_SEPARACION
            el valor de separacion se a de actualiar a la resta del otro pez de la lista en respecto a la posicion del pez propio que se esta actualizando, actuando con una
            fuerza opuesta y separando este de los vecinos.
            '''
            if distancia < RADIO_VISION:
                cohesion += otro.pos
                alineacion += otro.vel
                if distancia < DISTANCIA_SEPARACION:
                    separacion -= (otro.pos - self.pos)
                total += 1

        '''
        El siguente blouque if tiene la responsabilidad de analizar si total es mayor que 0 esto con el objetivo de evitar dividir por cero y evitar entar en una
        ideterminacion, por consiguiente si total (esto total hace referencia al total delos peces vecinos) es mayor que cero, la cohecion.
        Entonces, la poeracion cahesion / total hace una divicion con el objetivo de encotrar el centro de la masa (donde masa el la concentracin de peces)
        es importante tneer en cuetna que cohecion tiene almacenado la posicion de todos los peces vecionos dado que esto se an acutaolizado por medio de acumuladores anteriormente.
        En este oden de idias se resta self.pos que es el valor del venctor de ubicacion del pez en el plano 2d ya acecarse sutilmente al centro del cardumen
        y contener la forma de masa (cardumen 😊) el valor de multimplicacin que se le da es un valor fijo a criterio propio para que la acercacion sea sutil,
        y no de saltos exagerados en la pantalla.

        estemismo efecto ocurre para la alineacion pero en este caso se divide por la diferencia del total con la velocidad propia del pez multiplicada por 0.05,
        y asi poder continuar con ese movimiento armonico a la misma velocidad para todos en base al cardumen.
        '''

        if total > 0:
            cohesion = (cohesion / total - self.pos) * 0.05
            alineacion = (alineacion / total - self.vel) * 0.05
            separacion *= 0.1

        # Velocidad resultante
        self.vel += cohesion + alineacion + separacion + evadir

        '''
        El siguente fi hace una evaluacion de la longitud del vector de velocidad del pez actual, es decir el pez que se esta evaluando, si esto es mayor a
        la velocidad maxima, entocnes se scala la velociad maxima del pez a los limites establecidos y posterio a esto fuera del if se acumula la la velocidad
        '''
        # Limitar la velocidad
        if self.vel.length() > VELOCIDAD_MAXIMA:
            self.vel.scale_to_length(VELOCIDAD_MAXIMA)

        self.pos += self.vel
        '''
        Lo siguetne si ya es algo sencillo de procesar establece un control para evitar que los peces se desvorden de la pantalla. y la siguente funcion entonce al
        detectar los limites maximos guiado por ANCHO Y ALTO  basicamente los peso no pasaran y rebotaran dentro del stanque (interfaz)💧  
        '''
        # Evitar salir de la pantalla
        self.pos.x = max(0, min(ANCHO, self.pos.x))
        self.pos.y = max(0, min(ALTO, self.pos.y))

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, (0, 150, 255), self.pos, 5)


# ---------------------- Función Principal ----------------------
def main():

    '''
    El siguiente bloque basicamente consta de inicializarla ventana que no gestiona pygame, del mismo modo le damos valores a la pantalla enmarcados
    en las constantes declaradas al principio de ANCHO Y ALTO.
    poru ultimo se le asigna un nombre a la ventana con un par de emogis
    '''
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Simulación de Cardumen Bioinspirado 🐟🦈")

    '''
    El proximo bloque, se utliza para hacer el punto de spawn o de aparicion de los peces, el la variable centro se busca hallar vector cercana al centro.
    El apartado de lso peces es para hacer una postura aleatoria de los peces cerca al centro recordemos que se hace de forma aleatoria esta aparicion de peces
    pertenecientes al cardumen lo hace en base al rango de peces que deseemos en nuestro caso 30.
    '''
    centro = pygame.Vector2(ANCHO / 2, ALTO / 2)
    peces = [Pez(centro.x + random.uniform(-30, 30), centro.y + random.uniform(-30, 30)) for _ in range(NUM_PECES)]

    '''
    En el siguietne bloque para la variable reloj, a pricinpio no logre entender esta variable, pero esta resulta de ser un un variable tipo objec del la clase 
    pygame.time.Clock() esto ayuda a que en caso que el calculo venctorial de la pocion de la lista de los peces se haga de forma rapidisima (ejemplo 5 ms) este calculo se va
    a ver reflejado en la interfaz dentro del tiempo que tenga este reloj es decir dentro de los fps establecidos.

    Por otro lado la variable booleana corriendo acutua como una bandera de señal para las iteraciones del ciclo while que comienza mas adelante
    '''
    reloj = pygame.time.Clock()
    corriendo = True

    '''
    En el ciclo wile establece que mientras que corriedo se a true, a la pantalla se le va a asignar un fondo negro (25,25,25)
    dentro de esta while se anida un ciclo for que analiza cada evento en pypygame.event.get() para tener encuenta que si paygame se cierra se hace un quit
    la bandera corriendo pasa a estado false y el programa se dejaria de ejcutar.
    '''

    while corriendo:
        pantalla.fill((25, 25, 25))  # Fondo

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        tiburon_pos = pygame.Vector2(pygame.mouse.get_pos())

        # Dibujar el tiburón (mouse)
        pygame.draw.circle(pantalla, (255, 0, 0), tiburon_pos, 10)

        # Actualizar y dibujar peces
        '''
        Este for se encarga de hacer la creacioh y actializacion de los pesces en pantalla
        '''
        for pez in peces:
            pez.actualizar(peces, tiburon_pos)
            pez.dibujar(pantalla)

        pygame.display.flip()
        '''
        Se le asigan unvalor de 60 al objeto de reloj.
        '''
        reloj.tick(60)

    pygame.quit()

# ---------------------- Ejecutar ----------------------
if __name__ == "__main__":
    main()
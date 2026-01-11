import json
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px



def cargar_datos(path):
    with open(path, 'r' ,encoding='utf-8') as file:
        return json.load(file)
    
#======================Funciones para procesar los datos==========================================================

def convertir_usd_a_cup (datos, usd_to_cup):
    """
       Agrega la 'key' price_cup al diccionario de categorias por producto de la tienda online

    Args:
        datos (dict): datos recopilados de la tienda online
    
    Returns:
        dict
        Un diccionario con estructura similar a datos solo que agregando el price_cup en todos los productos
        para cada categoria
    
    """
    
    for categoria, productos in datos.items():
        for producto in productos:
            if "price_usd" in producto:  
                producto["price_cup"] = producto["price_usd"] * usd_to_cup
    
    return datos

    

def conteo_disponibilidad_categorias(tiendas):
    """
    Verifica y cuenta la disponibilidad de categorías de la canasta en la muestra de tiendas(MIPYMES)
    
    Para cada categoría de productos, esta función cuenta en cuántas tiendas
    aparece al menos un producto de  esa categoría. Esto es útil para analizar qué
    tipos de productos son más comunes en el comercio minorista muestreado
    
    Parameters:
        tiendas : (list)
            Lista de diccionarios, donde cada diccionario representa una tienda (MIPYME).
    Returns:
        dict
            Diccionario donde las keys son nombres de categorías y los values son el número
            de MIPYMES donde esa categoría está disponible (al menos un producto)
    """
    #diccionario temporal para encontrar categorias unicas
    categorias_descubiertas = {}
    
    #Esta primera parte es para agregar todas las categorias como keys del diccionario categorias_descubiertas
    for tienda in tiendas:
        for producto in tienda['products']:
            categoria = producto['category']
            #si la categoria no esta en el diccionario: agrega
            if categoria not in categorias_descubiertas:
                categorias_descubiertas[categoria] = True # valor True como marcador
        
               
    categoria_a_verificar = list(categorias_descubiertas.keys())
    
    #contadores para cada categoria
    contadores = {}
    for categoria in categoria_a_verificar:
        contadores[categoria] = 0
    
    #Recorrer cada tienda y contar disponibilidad
    
    for tienda in tiendas:
        # Para cada tienda, crear un diccionario que registra
        # que categorias encontro
        
        categorias_encontradas_en_esta_tienda = {}
        
        for producto in tienda['products']:
            categoria = producto['category']
            # marcar que esta categoria esta en la tienda
            categorias_encontradas_en_esta_tienda[categoria] = True
        #Actualizar contadores globales
        for categoria in categoria_a_verificar:
            #si la categoria estaba en esta tienda aumenta en 1 el contador de la categoria
            if categoria in categorias_encontradas_en_esta_tienda:
                contadores[categoria] += 1
    
    return contadores 


def agrupar_productos_por_categoria(tiendas):
    """Esta función busca reordenar la lista de tiendas a un diccionario donde las keys son las categorias de los
    productos y los values son listas donde los elementos son diccionarios que represetan productos de esa categoria
    de todas la muestra  de mipymes

    Args:
        tiendas (dict): lista de tiendas, donde cada tienda es un diccionario

    Returns:
        dict : diccionario de la forma {...categoria : [{...},...{...}]...}
    """
    dic_productos_por_categoria = {}
    
    for tienda in tiendas:
        for producto in tienda['products']:
            categoria = producto['category']
            if producto['category'] not in dic_productos_por_categoria:
                dic_productos_por_categoria[categoria] = []
                
            
    
    for tienda in tiendas:
        for producto in tienda['products']:
            categoria = producto['category']
            dic_productos_por_categoria[categoria].append(producto)  
            
    return dic_productos_por_categoria 
    

def conteo_origen(tiendas):
    """
    Cuenta la cantidad de productos nacionales e importados por categoría en una muestra de tiendas.
    
    Esta función es fundamental para analizar la composicion del mercado minorista según el origen de los productos permitiendo
    identificar patrones de dependencia importadora o fortaleza productiva nacional por categoria de productos de la canasta definida
    Args:
        tiendas : (list)
            Lista de diccionarios, donde cada diccionario representa una tienda (MIPYME).

    Returns:
        dict :   Diccionario anidado con el conteo estructurado por categoría y origen.
        Formato: {categoria: {'nacional': X, 'importado': Y}, ...}
    """
    conteo_por_categoria = {}
    
    for tienda in tiendas: 
        for product in tienda['products']:
            categoria = product['category']
            #En caso de no estar esta categoria, agregarla al diccionario de  conteo de origen inicializando valores del diccionario anidado en 0 en cada caso
            if categoria not in conteo_por_categoria:
                conteo_por_categoria[categoria] = {'nacional': 0, 'importado': 0}
            #Aumentar el contador  en caso de que el origen del producto de esta categoria sea nacional, si no, agregar a importado
            if product['origin'] == 'nacional':
                conteo_por_categoria[categoria]['nacional'] += 1
            if product['origin'] == 'importado':
                conteo_por_categoria[categoria]['importado'] += 1
    
    return conteo_por_categoria


def peso_minimo_por_categoria(productos_por_categoria):
    
    """Encuentra el peso mínimo(volumen)  (tamaño del envase) para cada categoría de productos en  un conjunto de datos estructurados
    Útil para identificar la presentación más pequeña disponible de cada tipo de producto en el mercado muestrado, lo que permite la estandarización de unidades de medida
    Args:
        productos_por_categoria : dict
        Diccionario donde las claves son nombres de categorias (strings) y los valores son listas de diccionarios que representan productos
          
    Returns:
        dict: Diccionario donde las claves son las mismas categorias de la entrada y los valores son el peso neto mínimo encontrado en cada categoria (float/int) 
    """
    pesos_por_categoria = {}
    
    for categoria, productos in productos_por_categoria.items():
        
        for producto in productos:
            
            # Si la categoria no existe, inicializarla entonces con lista vacia
            if categoria not in pesos_por_categoria:
                pesos_por_categoria[categoria] = []
            
            # Extraer el peso neto y agregarlo a la lista de esta categoría
            peso = producto['net_weight']
            pesos_por_categoria[categoria].append(peso)
    
    # Crear nuevo diccionario con los valores mínimos
    resultado = {}
    for categoria, lista_pesos in pesos_por_categoria.items():
        # Usar min() para encontrar el valor mas pequeño en la lista
        resultado[categoria] = min(lista_pesos)
    
    return resultado

def nombre_categorias(cansta):
    """
    Args:
        cansta (dict):  diccionario con definiciones de las cateogrias de la canasta 
    Returns:
        lista con todos los nombres de las categorias de productos defindas
    """
    categorias = []
    for k in cansta.keys():
        categorias.append(k)
        
    return categorias
    


def estandarizar_precios_unidad_modal (productos_por_categoria, canasta):
    """
    Esta funcion estandariza los precios de diferentes productos para que sean comparables
    independientemente de su tamaño de envase original. Convierte el precio de cada producto al costo
    que tendría si se vendiera en la presentación que más se repite de su categoría
    
    Parameters:
    productos_por_categoria: dict
        Diccionario donde las claves son nombres de categorias (strings) y los valores son listas de diccionarios que representan productos
    unidad_minima: dict:
        Diccionario donde las claves son categorias(strings) y los valores son pesos/volúmenes min encontrados para esa  cateogria (int)
    
    Returns:
        dict
            Diccionario donde las claves son categorias y los valores son listas de precios estandarizados a la unidad minima correspondiente
    
    Fórmula matemática:
    precio_estandarizado = precio_original / (peso_original/ unidad_minima)
    
    Notas:
        1-La funcion asume que 'net_weight y unidad_minima[categoria] estan en las mismas unidades de medida (ambos en ml, o ambos en g)
        2-Se espera que net_weight sea distino de cero, pues no se controla un error de división por cero 
        3-Si una categoria en productos por categoria no existe una unidad minima se generará un KeyError
        
    """
    precios_estandarizados_categoria = {}
    
    
    for categoria, productos in productos_por_categoria.items():
        
        unidad = canasta[categoria]["contenido_neto"]
        
        precios_estandarizados_categoria[categoria] = []
        
        for producto in productos:
            
            # Valores necesarios para el calculo de estandarizacion
            precio_original = producto['price_cup']    
            peso_original = producto['net_weight']    # (ver nota 2) 
            
            # --- FÓRMULA DE ESTANDARIZACIÓN  
            factor_conversion = peso_original / unidad
            precio_estandarizado = precio_original / factor_conversion
            
            precios_estandarizados_categoria[categoria].append(precio_estandarizado)
    
    return precios_estandarizados_categoria
    
def calcular_precio_mediano_por_categoria(precios_estandarizados):
    """Calcula la mediana de los productos de cada categoria

        precios_estandarizados (dict): los precios llevados a unidad minima observada en la muestra

    Returns:
        _type_: _
    """
    dic_medianas_catagorias = {}
    #se recorre el dicciario  de precios estandarizados y se ordena todos los precios estandarizados en cada categoria
    #para hallar la mediana
    for categoria, precios in precios_estandarizados.items():
        precios.sort()
        if len(precios) % 2 == 1:
            dic_medianas_catagorias[categoria] = precios[len(precios)// 2]
        elif len(precios) % 2 == 0:
            el1= precios[len(precios)// 2]
            el2 = precios[len(precios) // 2 -1]
            dic_medianas_catagorias[categoria] = (el1 + el2) / 2
    
    return dic_medianas_catagorias



def estandarizar_jugos_a_200ml(tiendas):
    """
    Estandariza todos los precios de los productos de la 'categoria de 'jugos' a un precio comparable
    por 200 mililitros (200 ml)
    Esta funcion  es esencial para establecer comparaciones justas entre jugos de diferentes marcas, tamaños, presentaciones
    
    Parameters:
    tiendas (list) : Lista de diccionarios donde cada diccionario representa una tienda (mipyme)
    
    Returns:
    list
        Lista de diccionario con la informacion estandarizada:
        cada diccionario contiene:
             Lista de diccionarios con la información estandarizada. Cada diccionario contiene:
        - tienda (str): Nombre de la tienda de origen
        - distancia_km (float): distancia de la tienda al hospital
        - producto (str): nombre del producto
        - marca (str): marca del producto
        - origen (str): origen/procedencia del producto (nacional/ importado)
        - precio_original(float) : precio original en CUP
        - peso_neto_original : peso (volumen) original 
        - precio_200ml(float): Precio estandarizado a 200ml (redondeado a 2 decimales)  
    
    """
    jugos_estandarizados = []
    
    for tienda in tiendas:
        for producto in tienda['products']:
            if producto['category'] == 'jugos':
                # Calcular precio para 200ml
                
                precio_por_200ml = (producto['price_cup'] / producto['net_weight']) * 200
                
                jugos_estandarizados.append({
                    'tienda': tienda['name'],
                    'distancia_km': tienda['distance_to_hospital'],
                    'producto': producto['name'],
                    'marca': producto['brand'],
                    'origen': producto['origin'],
                    'precio_original': producto['price_cup'],
                    'peso_neto_original': producto['net_weight'],
                    'precio_200ml': round(precio_por_200ml, 2)
                })
    
    return jugos_estandarizados

def calcular_costos_totales_por_categoria_canasta(canasta, precio_mediano_por_categoria):
    """
    Calcula el costo total por categoria para la canasta semanal
    
    Args:
        cantidades_semanales: dict con {categoria: cantidad_semanal}
        precios_estandarizados: dict con precios por unidad estandarizada
    """
    costos_totales = {}
    
    for categoria, precio_mediano in precio_mediano_por_categoria.items():
        if categoria in precio_mediano_por_categoria:
            # Costo total = cantidad semanal × precio estandarizado
            costo_total = canasta[categoria]['cantidad_semanal'] * precio_mediano
            costos_totales[categoria] = round(costo_total, 2)
    
    return costos_totales

def costo_total_canasta(canasta,precio_mediano_categoria):
    """
    Suma todos los precios medianos de todas la categoria multiplicados respectivamente por la cantidad
    que demanda la canasta  
    
    :param canasta: canasta definida para el proyecto
    :param precio_mediano_categoria (dict): diccionario con el precio mediano de todas las categorias
    
    Returns:
        float : El Costo total de la canasta semanal hospitalaria para pacientes pediatricos 
    """
    costo_total = 0
    
    for categoria, precio_mediano in  precio_mediano_categoria.items():
            costo_total += canasta[categoria]['cantidad_semanal'] *  precio_mediano
    
    return costo_total


#=====================Funciones para vizualizaciones=============================================


def visuzalizar_canastas_vs_salario(costo_canasta_mipymes, costo_canasta_tienda_estatal ,salario_estatal):
    """ 
    Gráfico  de barras  que compara el salario estatal mensual con el costo semanal de la canasta
    infantil hospitalaria
    Parameters:
    -costo_canasta_mipymes (int): costo total semanal de la canasta infantil en la muestra de mipymes
    -costo_canasta_tienda_estatal (int): costo total de la canasta infantil en una tienda de Cimex (tienda estatal en dólar) 
    -salario_estatal (float): salario mensual de referencia
    """
    etiquetas = ["Canasta en mipymes", "Canasta en SuperMarket23"]
    valores= [costo_canasta_mipymes, costo_canasta_tienda_estatal]
    colores = ["#3CABEB", "#ECF3CC"] 
    
    plt.figure(figsize=(8,6))
    barras = plt.bar(etiquetas, valores, color=colores)
    
    #Linea Horizontal de referencia: Salario medio estatal
    plt.axhline(salario_estatal, color = 'red', linestyle=':', linewidth=1)
    plt.text(1.05, salario_estatal + 100 , "Salario estatal", color = 'red')
    
    #Etiqueta encima de cada barra
    for barra in barras:
        altura = barra.get_height()
        plt.text(barra.get_x() + barra.get_width()/2, altura, f"{int(altura)}CUP", ha = "center", fontsize =10)

    # TITULO y ejes
        plt.title("Costo semanal de la canasta infantil vs salario estatal")
        plt.ylabel("CUP")
        plt.ylim(0, max(valores) + 1500)
        

def vizualizar_origen_de_productos_por_categoria(origen_por_categoria):
    """
    Crea un gráfico interactivo de tipo pastel  con menú desplegable que muestra ka 
    proporción de productos nacionales vs. importados para diferentes categorías
    

    Parameters:
        origen_por_categoria : dict
            Diccionario anidado con la estructura:
            { 
                ... categoria_i : {'nacional: X, 'importado': Y} ...
            }
            donde 'nacional' e 'importados' son conteos enteros de productos
            
    Returns: None
        Muestra directamente el grafico interactivo
    """
    # Una lista para almacenar botones intercativos 
    botones = []
    
    for categoria in origen_por_categoria:
        nacional = origen_por_categoria[categoria]['nacional']
        importado = origen_por_categoria[categoria]['importado']
        
        
        #Crear boton  para esta categoria
        
        boton = {
            'label': f"{categoria}",      
            'method': 'update',                   
            'args': [{                              
            'values': [[nacional, importado]],   
            'title': f'Origen: {categoria}'     
        }]
    }
        
        botones.append(boton)
        
    #creacion del grafico inicial
    # Se inicializa con datos de la categoria 'yogurt' (aqui se asume que la categoria yogurt siempre existe)
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels= ['Nacional', 'Importado'],
        values= [origen_por_categoria['yogurt']['nacional'], origen_por_categoria['yogurt']['importado'] ],
        hole=0.5,
        marker=dict(colors=["#7df3ae", "#2297e6"]),
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Productos: %{value}<br>Porcentaje: %{percent}'
    ))
    
    
    
    #Aqui se configura el layout interactivo
    fig.update_layout(
    title={
        'text': 'Origen de Productos por Categoría de la Canasta',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 20}
    },
    
    #Menu desplegable que permite cambiar entre categorias
    updatemenus=[dict(
        type="dropdown",
        direction="down",
        x=0.3, 
        y=1.15,
        buttons=botones
    )],
    
    # Texto de intruccion (seleccionar categoría)
    annotations=[
        dict(
            text="Selecciona categoría:",
            x=0.1,
            y=1.25,
            xref="paper", # aqui las coordenadas son relativas al lienzo
            yref="paper", 
            showarrow=False,
            font=dict(size=14, color='#2c3e50')
        )
    ],
    height=500, # Altura fija del gráfico
    showlegend=True
    )
    
    fig.show()
    


def visualizar_distancia_vs_precios_jugos(jugos_estandarizados):
    """
    Crea un gráfico de dispersión que analiza la relación entre la distancia
    al  hospital de referencia y el precio de los jugos estandarizados a 200ml

    Parameters
        jugos_estandarizados : list
        Lista de diccionarios con la información estandarizada. Cada diccionario contiene:
            - tienda (str): Nombre de la tienda de origen
            - distancia_km (float): distancia de la tienda al hospital
            - producto (str): nombre del producto
            - marca (str): marca del producto
            - origen (str): origen/procedencia del producto (nacional/ importado)
            - precio_original(float) : precio original en CUP
            - peso_neto_original : peso (volumen) original 
            - precio_200ml(float): Precio estandarizado a 200ml (redondeado a 2 decimales)
    Returns : None
    Muestra directamente el scatter plot
    """
    
    # Extraer datos para el análisis
    # listas paralelas de distancias y precios correspondientes
    distancias = [dato['distancia_km'] for dato in jugos_estandarizados]
    precios = [dato['precio_200ml'] for dato in jugos_estandarizados]
    
    # Crear el gráfico de dispersión:
    
    plt.figure(figsize=(10, 6))
    # -alpha= 0.7 : transparencia para ver superposiciones
    # -s = 60: tamaño de los puntos
    plt.scatter(distancias, precios, alpha=0.7, s=60, color='blue')
    
    # Personalizar
    plt.xlabel('Distancia al Hospital (km)')
    plt.ylabel('Precio (CUP/200ml)')
    plt.title('Precio de Jugos vs Distancia al Hospital')
    plt.grid(True, alpha=0.3) # grid semitransparente
    
    # Mostrar
    plt.tight_layout() # ajustar automáticamente los márgenes
    plt.show()


def visualizar_costo_total_canasta(canasta, costos_totales):
    """
    Crea un gráfico de treemap interactivo que muestra la composición 
    del costo semanal de una canasta para una de hospitalización (durante una semana) de un niño en condiciones estables
    

    Parameters:
        canasta: dict
            Diccionario que define la canasta
        costos_totales : dict
            Diccionario con los costos totales por categoría
    
    Returns: None
        Muestra directamente el Treemap interactivo
            
        
    """
    # Preparacion del grafico (etiquetas informativas que se colocan en cada rectangulo)
    #Las etiquetas combinan informacion de canasta y costo
    etiquetas = []
    for categoria, costo in costos_totales.items():
        cantidad = canasta[categoria]['cantidad_semanal']
        etiqueta = f"{categoria}<br>{cantidad} unidades<br>{costo} CUP"
        etiquetas.append(etiqueta)
    
    # Usando Plotly Express para crear treemap jerarquico
    fig = px.treemap(
        names=etiquetas, # aqui las etiquetas para cada rectangulo
        parents=[""] * len(costos_totales), # todas son raices 
        values=list(costos_totales.values()), # valores que determinan el tamanno del rectagulo
        title="Costo Total Semanal por Categoría - Canasta Hospitalaria",
        color=list(costos_totales.values()), # color por valor (escala continua de colores)
        color_continuous_scale='RdYlBu_r', # escala rojo-amarillo-azul ... rojo= costo alto, azul = costo bajo
        labels={'value': 'Costo Total Semanal (CUP)', 'color': 'Costo (CUP)'}
    )
    
    # Personalizar el layout
    fig.update_layout(
        margin=dict(t=50, l=25, r=25, b=25), #margenes , tpo, lef, rightm bottom
        title_x=0.5, # Centra el titulo horizontalmente
        title_font_size=14
    )
    
    fig.show()

def visualizar_disponibilidad(productos_disponibilidad, total_tiendas):
    """
        Crea un gráfico de barras horizontales que muestra el pociento de disponibilidad de cada producto de la
        canasta de hospitalización

    Parameters:
        productos_disponibilidad: dict
            diccionario cuyas claves son las categorias de productos de la canasta (str) y cuyos valores son el conteo (int)
            en la muestgra de esas cateogrías
        total_tiendas: int
            Total de la muestra de mipymes 
        
        Returns: None
            Muestra directamente el gráfico de barras horizontales
    """
    #Tener por separado las categorias y el conteo de disponibilidad y hallar el porciento con
    categorias = list(productos_disponibilidad.keys())
    disponibles = list(productos_disponibilidad.values())
    porcentajes = [(d/total_tiendas)*100 for d in disponibles]
    
    #Queremos Ordenar los datos para mostrar las barras de menor porciento a mayor
    #Para ello primero empaquetemos las 3 listas creadas en una lista de triplos ordenados
    empaquetado = []
    for i in range(len(categorias)):
        paquete = (
            categorias[i],
            disponibles[i],
            porcentajes[i]
        )
        empaquetado.append(paquete)
    
    #Ahora ordenamos la lista empaquetado por el tercer elemento del triplo (por porciento) de manera ascendente (con ordenacion por minimos sucesivos)
    n = len(empaquetado)
    for i in range(n):
        min_actual = i
        for j in range(i+1, n):
            if empaquetado[j][2] < empaquetado[min_actual][2]:
                min_actual = j
        empaquetado[i],empaquetado[min_actual] = empaquetado[min_actual], empaquetado[i]
        
    datos_ordenados = empaquetado # Ya estan ordenados los datos
    
    #Finalmente, desempaquetamos en listas ordenadas
    categorias_ordenadas = []
    disponibles_ordenados = []
    porcentajes_ordenados = []
    
    for cat, disp, porc in datos_ordenados:
        categorias_ordenadas.append(cat)
        disponibles_ordenados.append(disp)
        porcentajes_ordenados.append(porc)
    
        
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(categorias_ordenadas, porcentajes_ordenados, color='skyblue', height=0.6)
    
    plt.xlim(right=100) # Fijar el limite del grafico a 100 (ya que es %)
    # titulos
    ax.set_xlabel('Disponibilidad (%)')
    ax.set_title('Disponibilidad de Productos en Muestra de 30 MIPYMES')
    
    # Añadir porcentajes al final de cada barra
    for bar, porcentaje in zip(bars, porcentajes_ordenados):
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2,
               f'{porcentaje:.1f}%', va='center')
    
    plt.tight_layout()
    plt.show()


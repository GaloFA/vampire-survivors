import random
import pygame


class Item:
    """Clase base que representa un ítem genérico con niveles y efectos."""

    def __init__(self, nombre, descripcion, tipo_efecto, mejoras, imagen=None, sprite_config=None):
        """
        Inicializa un ítem con nombre, descripción, tipo de efecto, mejoras por nivel,
        y opcionalmente una imagen o sprite con configuración.
        """
        self.nombre = nombre
        self.descripcion = descripcion
        self.tipo_efecto = tipo_efecto
        self.mejoras = mejoras
        self.nivel = 1
        self.imagen = imagen  # Ruta de la imagen o sprite sheet
        self.sprite_config = sprite_config or {}  # Configuración del sprite
        self.frames = []  # Lista para almacenar los frames del sprite

    def configurar_sprite(self, ancho=16, alto=16, filas=1, columnas=1):
        """Configura las propiedades del sprite, como ancho y alto."""
        self.sprite_config['ancho'] = ancho
        self.sprite_config['alto'] = alto
        self.sprite_config['filas'] = filas
        self.sprite_config['columnas'] = columnas

        if self.imagen:
            hoja_sprite = pygame.image.load(self.imagen).convert_alpha()
            for fila in range(filas):
                for columna in range(columnas):
                    x = columna * ancho
                    y = fila * alto
                    frame = hoja_sprite.subsurface((x, y, ancho, alto))
                    self.frames.append(frame)

    def obtener_frame(self, indice):
        """Devuelve un frame específico de la lista de frames."""
        if 0 <= indice < len(self.frames):
            return self.frames[indice]
        return None

    def subir_nivel(self):
        """Sube el nivel del ítem si no ha alcanzado el nivel máximo."""
        if self.nivel < len(self.mejoras):
            self.nivel += 1
            return f"{self.nombre} ha subido al nivel {self.nivel}!"
        else:
            return f"{self.nombre} ya está en el nivel máximo."

    def obtener_valor_efecto(self):
        return self.mejoras[self.nivel - 1]

    def aplicar_efecto(self, jugador):
        pass

    def __str__(self):
        """Devuelve una representación en cadena del ítem."""
        return f"{self.nombre} (Nivel {self.nivel}): {self.descripcion}"


class ItemSalud(Item):
    """Ítem que proporciona mejoras en salud."""

    def __init__(self):
        super().__init__(
            nombre="Elixir de Salud",
            descripcion="Aumenta la salud del jugador.",
            tipo_efecto="salud",
            mejoras=[20, 40, 60, 80, 100],
            imagen=self.obtener_frame_inicial()
        )
        self.configurar_sprite(ancho=16, alto=16, filas=1, columnas=4)

    def aplicar_efecto(self, jugador):
        jugador.salud += self.obtener_valor_efecto()

    def obtener_frame_inicial(self):
        """Devuelve el frame inicial del sprite configurado."""
        return self.obtener_frame(0)


class ItemVelocidad(Item):
    """Ítem que proporciona mejoras en velocidad."""

    def __init__(self):
        super().__init__(
            nombre="Bota de Velocidad",
            descripcion="Aumenta la velocidad de movimiento del jugador.",
            tipo_efecto="velocidad",
            mejoras=[2, 4, 6, 8, 10],
            imagen=self.obtener_frame_inicial()
        )
        self.configurar_sprite(ancho=16, alto=16, filas=1, columnas=4)

    def aplicar_efecto(self, jugador):
        jugador.velocidad += self.obtener_valor_efecto()

    def obtener_frame_inicial(self):
        """Devuelve el frame inicial del sprite configurado."""
        return self.obtener_frame(0)


class ItemDaño(Item):
    """Ítem que proporciona mejoras en daño."""

    def __init__(self):
        super().__init__(
            nombre="Furia del Guerrero",
            descripcion="Aumenta el daño infligido por el jugador.",
            tipo_efecto="daño",
            mejoras=[5, 10, 15, 20, 25],
            imagen=self.obtener_frame_inicial()
        )
        self.configurar_sprite(ancho=16, alto=16, filas=1, columnas=4)

    def aplicar_efecto(self, jugador):
        jugador.danio += self.obtener_valor_efecto()

    def obtener_frame_inicial(self):
        """Devuelve el frame inicial del sprite configurado."""
        return self.obtener_frame(0)


class ItemDefensa(Item):
    """Ítem que proporciona mejoras en defensa."""

    def __init__(self):
        super().__init__(
            nombre="Escudo del Valiente",
            descripcion="Aumenta la defensa del jugador.",
            tipo_efecto="defensa",
            mejoras=[3, 6, 9, 12, 15],
            imagen=self.obtener_frame_inicial()
        )
        self.configurar_sprite(ancho=16, alto=16, filas=1, columnas=4)

    def aplicar_efecto(self, jugador):
        jugador.defensa += self.obtener_valor_efecto()

    def obtener_frame_inicial(self):
        """Devuelve el frame inicial del sprite configurado."""
        return self.obtener_frame(0)


class ItemExperiencia(Item):
    """Ítem que proporciona mejoras en experiencia ganada."""

    def __init__(self):
        super().__init__(
            nombre="Amuleto de Sabiduría",
            descripcion="Aumenta la experiencia ganada por el jugador.",
            tipo_efecto="experiencia",
            mejoras=[50, 100, 150, 200, 250],
            imagen=self.obtener_frame_inicial()
        )
        self.configurar_sprite(ancho=16, alto=16, filas=1, columnas=4)

    def aplicar_efecto(self, jugador):
        jugador.experiencia += self.obtener_valor_efecto()

    def obtener_frame_inicial(self):
        """Devuelve el frame inicial del sprite configurado."""
        return self.obtener_frame(0)


class ItemAutocuracion(Item):
    """Ítem que mejora la autocuración del jugador."""

    def __init__(self):
        super().__init__(
            nombre="Anillo de Autocuración",
            descripcion="Aumenta la cantidad de salud recuperada automáticamente.",
            tipo_efecto="autocuracion",
            mejoras=[1, 2, 3, 4, 5],
            imagen=self.obtener_frame_inicial()
        )
        self.configurar_sprite(ancho=16, alto=16, filas=1, columnas=4)

    def aplicar_efecto(self, jugador):
        jugador.autocuracion += self.obtener_valor_efecto()

    def obtener_frame_inicial(self):
        """Devuelve el frame inicial del sprite configurado."""
        return self.obtener_frame(0)


class ItemCriticos(Item):
    """Ítem que aumenta la probabilidad de ataques críticos."""

    def __init__(self):
        super().__init__(
            nombre="Capa de Sombra",
            descripcion="Aumenta la probabilidad de infligir daño crítico.",
            tipo_efecto="critico",
            mejoras=[1, 2, 3, 4, 5],  # Porcentaje o puntos de probabilidad
            imagen=self.obtener_frame_inicial()
        )
        self.configurar_sprite(ancho=16, alto=16, filas=1, columnas=4)

    def aplicar_efecto(self, jugador):
        jugador.probabilidad_critico += self.obtener_valor_efecto()

    def obtener_frame_inicial(self):
        """Devuelve el frame inicial del sprite configurado."""
        return self.obtener_frame(0)


class ItemVelocidadAtaque(Item):
    """Ítem que mejora la velocidad de ataque del jugador."""

    def __init__(self):
        super().__init__(
            nombre="Guantes de Agilidad",
            descripcion="Aumenta la velocidad de ataque del jugador.",
            tipo_efecto="velocidad_ataque",
            mejoras=[1, 2, 3, 4, 5],
            imagen=self.obtener_frame_inicial()
        )
        self.configurar_sprite(ancho=16, alto=16, filas=1, columnas=4)

    def aplicar_efecto(self, jugador):
        jugador.velocidad_ataque += self.obtener_valor_efecto()

    def obtener_frame_inicial(self):
        """Devuelve el frame inicial del sprite configurado."""
        return self.obtener_frame(0)


class DiccionarioClass:
    def __init__(self):
        # Asegúrate de que estos ítems sean instancias correctas de tus clases
        self.items_dict = {
            "item_salud": ItemSalud(),
            "item_velocidad": ItemVelocidad(),
            "item_danio": ItemDaño(),
            "item_defensa": ItemDefensa(),
            "item_experiencia": ItemExperiencia(),
            "item_autocuracion": ItemAutocuracion(),
            "item_criticos": ItemCriticos(),
            "item_velocidad_ataque": ItemVelocidadAtaque(),
        }
        self.selected_items = {}  # Diccionario para almacenar ítems seleccionados

    def select_random_items(self):
        """Selecciona 3 ítems únicos aleatorios del diccionario de ítems."""
        # Selecciona 3 claves únicas aleatorias del diccionario
        unique_keys = random.sample(list(self.items_dict.keys()), 3)

        # Crear el diccionario con los ítems seleccionados
        self.selected_items = {
            key: self.items_dict[key] for key in unique_keys}
        return self.selected_items

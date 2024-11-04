import random
import pygame
import settings
from business.entities.player import Player
from presentation.sprite import PlayerSprite


class Item:
    """Clase base que representa un ítem genérico con niveles y efectos."""

    def __init__(self, nombre, descripcion, tipo_efecto, mejoras, imagen_path):
        """
        Inicializa un ítem con nombre, descripción, tipo de efecto, mejoras por nivel,
        y opcionalmente una imagen o sprite con configuración.
        """
        self.nombre = nombre
        self.descripcion = descripcion
        self.tipo_efecto = tipo_efecto
        self.mejoras = mejoras
        self.nivel = 1
        self.imagen_path = imagen_path
        x, y = settings.WORLD_WIDTH//2, settings.WORLD_HEIGHT//2
        self.player = Player(x, y, PlayerSprite(x, y), 100)

    def subir_nivel(self, jugador):
        """Sube el nivel del ítem si no ha alcanzado el nivel máximo y aplica la mejora."""
        if self.nivel < len(self.mejoras):
            self.nivel += 1  # Incrementa el nivel
            self.aplicar_efecto(jugador)  # Aplica el efecto del nuevo nivel
            return f"{self.nombre} ha subido al nivel {self.nivel} y ahora otorga {self.obtener_valor_efecto()} de efecto!"
        else:
            return f"{self.nombre} ya está en el nivel máximo."

    def obtener_valor_efecto(self):
        return self.mejoras[self.nivel - 1]

    def aplicar_efecto(self, jugador):
        """Método a implementar en las subclases para aplicar el efecto específico al jugador."""
        pass

    def __str__(self):
        """Devuelve una representación en cadena del ítem."""
        return f"{self.nombre} - Nivel {self.nivel}"


class ItemSalud(Item):
    """Ítem que proporciona mejoras en salud."""

    def __init__(self):
        super().__init__(
            nombre="Amuleto de Salud",
            descripcion="Aumenta la salud del jugador.",
            tipo_efecto="salud",
            mejoras=[20, 40, 60, 80, 100],
            imagen_path="./assets/items/sprite-items/item2.png"
        )

    def aplicar_efecto(self):
        self.player.__max_health += self.obtener_valor_efecto()


class ItemVelocidad(Item):
    """Ítem que proporciona mejoras en velocidad."""

    def __init__(self):
        super().__init__(
            nombre="Bota de Velocidad",
            descripcion="Aumenta la velocidad de movimiento del jugador.",
            tipo_efecto="velocidad",
            mejoras=[2, 4, 6, 8, 10],
            imagen_path="./assets/items/sprite-items/item7.png"
        )

    def aplicar_efecto(self):
        self.player.__velocidad_incrementada += self.obtener_valor_efecto()


class ItemDaño(Item):
    """Ítem que proporciona mejoras en damage."""

    def __init__(self):
        super().__init__(
            nombre="Espada del Guerrero",
            descripcion="Aumenta el damage infligido por el jugador.",
            tipo_efecto="damage",
            mejoras=[5, 10, 15, 20, 25],
            imagen_path="./assets/items/sprite-items/item5.png"
        )

    def aplicar_efecto(self):
        self.player.__damage_incrementada += self.obtener_valor_efecto()


class ItemDefensa(Item):
    """Ítem que proporciona mejoras en defensa."""

    def __init__(self):
        super().__init__(
            nombre="Escudo del Valiente",
            descripcion="Aumenta la defensa del jugador.",
            tipo_efecto="defensa",
            mejoras=[3, 6, 9, 12, 15],
            imagen_path="./assets/items/sprite-items/item8.png"
        )

    def aplicar_efecto(self):
        self.player.__defensa_incrementada += self.obtener_valor_efecto()


class ItemExperiencia(Item):
    """Ítem que proporciona mejoras en experiencia ganada."""

    def __init__(self):
        super().__init__(
            nombre="Libro de Sabiduría",
            descripcion="Aumenta la experiencia ganada por el jugador.",
            tipo_efecto="experiencia",
            mejoras=[2, 3, 4, 5, 10],
            imagen_path="./assets/items/sprite-items/item9.png"
        )

    def aplicar_efecto(self):
        self.player.__multexperience += self.obtener_valor_efecto()


class ItemAutocuracion(Item):
    """Ítem que mejora la autocuración del jugador."""

    def __init__(self):
        super().__init__(
            nombre="Petalos de Luz",
            descripcion="Aumenta la cantidad de salud recuperada automáticamente.",
            tipo_efecto="autocuracion",
            mejoras=[1, 2, 3, 4, 5],
            imagen_path="./assets/items/sprite-items/item11.png"
        )

    def aplicar_efecto(self):
        self.player.__autocuracion += self.obtener_valor_efecto()


class ItemCriticos(Item):
    """Ítem que aumenta la probabilidad de ataques críticos."""

    def __init__(self):
        super().__init__(
            nombre="Anillo de Juicio",
            descripcion="Aumenta la probabilidad de infligir damage crítico.",
            tipo_efecto="critico",
            mejoras=[1, 2, 3, 4, 5],  # Porcentaje o puntos de probabilidad
            imagen_path="./assets/items/sprite-items/item1.png"
        )

    def aplicar_efecto(self):
        self.player.__probabilidad_critico += self.obtener_valor_efecto()


class ItemVelocidadAtaque(Item):
    """Ítem que mejora la velocidad de ataque del jugador."""

    def __init__(self):
        super().__init__(
            nombre="Elixir de Asalto Rápido",
            descripcion="Aumenta la velocidad de ataque del jugador.",
            tipo_efecto="velocidad_ataque",
            mejoras=[1, 2, 3, 4, 5],
            imagen_path="./assets/items/sprite-items/item10.png"
        )

    def aplicar_efecto(self):
        self.player.__velocidad_ataque_incrementada += self.obtener_valor_efecto()


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

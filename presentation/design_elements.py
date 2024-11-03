""" Module that contains representation of buttons in the pause menu. """
import pygame
import settings


class Button():
    """Class that represents buttons in the pause menu."""

    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        """Draws the button on the given screen."""
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        """Determines if the button is clicked based on the mouse position."""
        return self.rect.collidepoint(mouse_pos)


class Title:
    """Clase que representa un título en la pantalla."""

    def __init__(self, text, x, y, font_size, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.font = pygame.font.Font(None, font_size)

    def draw(self, screen):
        """Dibuja el título en la pantalla en la posición especificada."""
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        screen.blit(text_surface, text_rect)


class Container:
    """Clase que representa un contenedor que puede tener otros elementos visuales."""

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        """Dibuja el contenedor en la pantalla con el color especificado."""
        pygame.draw.rect(screen, self.color, self.rect)


class ItemCard:
    """Clase que representa una tarjeta de ítem con imagen, nombre y descripción."""

    def __init__(self, x, y, width, height, item_name, description, image_path, is_new=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.item_name = item_name
        self.description = description
        self.image_path = image_path
        self.is_new = is_new

        # Cargar la imagen del ítem
        self.image = pygame.image.load(image_path)
        # Redimensionar la imagen si es necesario
        self.image = pygame.transform.scale(self.image, (50, 50))

        # Definir las fuentes
        self.font_name = pygame.font.Font(None, 36)
        self.font_description = pygame.font.Font(None, 24)
        self.font_new = pygame.font.Font(None, 24)

        # Definir colores
        self.background_color = (150, 150, 150)  # Gris claro
        self.border_color = (200, 100, 0)  # Naranja
        self.text_color = (255, 255, 255)  # Blanco
        self.new_color = (255, 255, 0)  # Amarillo

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        """Dibuja la tarjeta de ítem en la pantalla."""
        # Dibujar el fondo y el borde
        pygame.draw.rect(screen, self.border_color, (self.x - 2,
                         self.y - 2, self.width + 4, self.height + 4))  # Borde
        pygame.draw.rect(screen, self.background_color,
                         (self.x, self.y, self.width, self.height))  # Fondo

        # Dibujar la imagen
        screen.blit(self.image, (self.x + 10, self.y + 10))

        # Dibujar el nombre del ítem
        name_surface = self.font_name.render(
            self.item_name, True, self.text_color)
        screen.blit(name_surface, (self.x + 70, self.y + 10))

        # Dibujar la descripción
        description_surface = self.font_description.render(
            self.description, True, self.text_color)
        screen.blit(description_surface, (self.x + 10, self.y + 70))

        # Dibujar el texto "New!" si es un ítem nuevo
        if self.is_new:
            new_surface = self.font_new.render("New!", True, self.new_color)
            screen.blit(new_surface, (self.x + self.width - 45, self.y + 10))

    def is_clicked(self, mouse_pos):
        """Determines if the button is clicked based on the mouse position."""
        return self.rect.collidepoint(mouse_pos)

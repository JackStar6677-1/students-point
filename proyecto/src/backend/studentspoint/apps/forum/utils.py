"""Utilidades para el módulo de foros."""

import re


# Palabras que no se permiten en títulos o cuerpos de posts. Si una
# aparece, el post queda en estado de "revisión". Ajusta esta lista para
# modificar las reglas de moderación.
BANNED_WORDS = {
    "malo", "ofensivo", "odio", "violencia", "drogas", "alcohol", 
    "sexo", "pornografia", "spam", "estafa", "fraude", "hack",
    "virus", "malware", "phishing", "scam", "fake", "mentira"
}

# Palabras que requieren moderación manual
MODERATION_WORDS = {
    "política", "religión", "discriminación", "racismo", "sexismo",
    "homofobia", "transfobia", "bullying", "acoso", "amenaza"
}

# Palabras ofensivas que deben ser censuradas parcialmente
OFFENSIVE_WORDS = {
    "mierda", "puta", "pendejo", "idiota", "estupido", "imbecil",
    "carajo", "maldito", "joder", "coño", "cabron", "gilipollas",
    "huevon", "weón", "weon", "ctm", "conchetumare", "culiao"
}


def censurar_texto(texto):
    """Censura parcialmente palabras ofensivas en el texto.
    
    Ejemplo: 'mierda' se convierte en 'm#####'
    
    Args:
        texto (str): Texto a censurar
        
    Returns:
        str: Texto con palabras ofensivas censuradas
    """
    if not texto:
        return texto
        
    texto_censurado = texto
    for palabra in OFFENSIVE_WORDS:
        # Buscar la palabra completa (case insensitive)
        patron = re.compile(r'\b' + re.escape(palabra) + r'\b', re.IGNORECASE)
        
        def reemplazar(match):
            palabra_encontrada = match.group(0)
            # Mantener primera letra y reemplazar resto con #
            if len(palabra_encontrada) > 1:
                return palabra_encontrada[0] + '#' * (len(palabra_encontrada) - 1)
            return '#'
        
        texto_censurado = patron.sub(reemplazar, texto_censurado)
    
    return texto_censurado


def contiene_palabras_prohibidas(texto):
    """Verifica si el texto contiene palabras prohibidas.
    
    Args:
        texto (str): Texto a verificar
        
    Returns:
        bool: True si contiene palabras prohibidas
    """
    if not texto:
        return False
        
    texto_lower = texto.lower()
    return any(bad in texto_lower for bad in BANNED_WORDS)


def contiene_palabras_moderacion(texto):
    """Verifica si el texto contiene palabras que requieren moderación manual.
    
    Args:
        texto (str): Texto a verificar
        
    Returns:
        bool: True si requiere moderación
    """
    if not texto:
        return False
        
    texto_lower = texto.lower()
    return any(mod in texto_lower for mod in MODERATION_WORDS)


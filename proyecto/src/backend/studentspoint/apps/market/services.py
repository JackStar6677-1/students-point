"""Servicios para el módulo de marketplace."""

import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class OpenGraphService:
    """Servicio para obtener metadatos OpenGraph de URLs."""
    
    @staticmethod
    def obtener_metadatos_opengraph(url: str) -> Dict[str, Optional[str]]:
        """Obtiene metadatos OpenGraph de una URL.
        
        Args:
            url: URL de la cual obtener metadatos
            
        Returns:
            dict: Diccionario con metadatos (og_title, og_description, og_image, og_site_name)
        """
        try:
            import requests
            from requests.exceptions import Timeout, RequestException
            from bs4 import BeautifulSoup
            from urllib.parse import urljoin
            
            response = requests.get(
                url, 
                timeout=10, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                },
                allow_redirects=True
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            metadatos = {}
            
            # Obtener metadatos OpenGraph
            og_title = soup.find('meta', property='og:title')
            if og_title:
                metadatos['og_title'] = og_title.get('content', '')[:200]
            
            og_description = soup.find('meta', property='og:description')
            if og_description:
                metadatos['og_description'] = og_description.get('content', '')[:500]
            
            og_image = soup.find('meta', property='og:image')
            if og_image:
                imagen_url = og_image.get('content', '')
                # Convertir URLs relativas a absolutas si es necesario
                if imagen_url and not imagen_url.startswith('http'):
                    imagen_url = urljoin(url, imagen_url)
                metadatos['og_image'] = imagen_url
            
            og_site_name = soup.find('meta', property='og:site_name')
            if og_site_name:
                metadatos['og_site_name'] = og_site_name.get('content', '')[:100]
            
            # Fallback a metadatos HTML estándar si no hay OpenGraph
            if not metadatos.get('og_title'):
                title = soup.find('title')
                if title:
                    metadatos['og_title'] = title.get_text().strip()[:200]
            
            if not metadatos.get('og_description'):
                description = soup.find('meta', attrs={'name': 'description'})
                if description:
                    metadatos['og_description'] = description.get('content', '')[:500]
            
            # Si aún no hay imagen, buscar la primera imagen grande en el HTML
            if not metadatos.get('og_image'):
                img_tag = soup.find('img', src=True)
                if img_tag:
                    img_src = img_tag.get('src', '')
                    if img_src and not img_src.startswith('data:'):
                        metadatos['og_image'] = urljoin(url, img_src)
            
            logger.info(f"Metadatos obtenidos de {url}: {list(metadatos.keys())}")
            return metadatos
            
        except Timeout:
            logger.warning(f"Timeout obteniendo metadatos de {url}")
            return {}
        except RequestException as e:
            logger.warning(f"Error de red obteniendo metadatos de {url}: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error inesperado obteniendo metadatos de {url}: {e}", exc_info=True)
            return {}


class ProductoValidationService:
    """Servicio para validaciones de productos."""
    
    @staticmethod
    def validar_url(url: str) -> bool:
        """Valida que la URL sea válida.
        
        Args:
            url: URL a validar
            
        Returns:
            bool: True si la URL es válida
        """
        try:
            from django.core.validators import URLValidator
            validator = URLValidator()
            validator(url)
            return True
        except Exception:
            return False
    
    @staticmethod
    def detectar_tipo_enlace(url: str) -> str:
        """Detecta automáticamente el tipo de enlace según el dominio.
        
        Args:
            url: URL a analizar
            
        Returns:
            str: Tipo de enlace detectado
        """
        from .models import Producto
        
        url_lower = url.lower()
        
        if 'facebook.com' in url_lower or 'facebook marketplace' in url_lower:
            return Producto.TiposEnlace.FACEBOOK
        elif 'yapo.cl' in url_lower:
            return Producto.TiposEnlace.YAPO
        elif 'mercadolibre' in url_lower or 'mercadolibre.cl' in url_lower:
            return Producto.TiposEnlace.MERCADOLIBRE
        else:
            return Producto.TiposEnlace.OTRO


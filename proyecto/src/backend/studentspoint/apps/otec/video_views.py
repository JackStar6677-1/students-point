"""Vista personalizada para servir videos con soporte de streaming."""

import os
import re
import mimetypes
from django.http import StreamingHttpResponse, HttpResponse, FileResponse
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve as django_serve


def range_file_iterator(file_obj, start, end, chunk_size=8192):
    """Iterador que lee el archivo en chunks desde una posición específica."""
    file_obj.seek(start)
    remaining = end - start + 1
    
    while remaining > 0:
        chunk_size_to_read = min(chunk_size, remaining)
        data = file_obj.read(chunk_size_to_read)
        if not data:
            break
        remaining -= len(data)
        yield data


@csrf_exempt
@require_http_methods(["GET", "HEAD"])
def serve_video(request, path):
    """
    Sirve archivos de video con soporte para HTTP Range Requests.
    Esto permite que el navegador pueda adelantar/atrasar el video.
    Si el archivo no existe, delega a la vista estándar de Django.
    """
    # Construir la ruta completa del archivo
    full_path = os.path.join(settings.MEDIA_ROOT, 'cursos', 'videos', path)
    
    # Si el archivo no existe, usar la vista estándar de Django (que mostrará 404)
    if not os.path.exists(full_path) or not os.path.isfile(full_path):
        # Delegar a la vista estándar de serve
        from pathlib import Path
        return django_serve(request, f'cursos/videos/{path}', document_root=Path(settings.MEDIA_ROOT))
    
    # Obtener el tamaño del archivo
    file_size = os.path.getsize(full_path)
    
    # Determinar el tipo MIME
    content_type, _ = mimetypes.guess_type(full_path)
    if not content_type:
        content_type = 'video/mp4'
    
    # Procesar el header Range si existe
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = re.match(r'bytes=(\d+)-(\d*)', range_header)
    
    if range_match:
        # Petición con Range (para seeking/streaming)
        start = int(range_match.group(1))
        end = int(range_match.group(2)) if range_match.group(2) else file_size - 1
        
        # Validar el rango
        if start >= file_size or end >= file_size or start > end:
            response = HttpResponse(status=416)  # Range Not Satisfiable
            response['Content-Range'] = f'bytes */{file_size}'
            return response
        
        # Abrir el archivo y crear la respuesta con streaming
        file_obj = open(full_path, 'rb')
        response = StreamingHttpResponse(
            range_file_iterator(file_obj, start, end),
            status=206,  # Partial Content
            content_type=content_type
        )
        response['Content-Length'] = str(end - start + 1)
        response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
        response['Accept-Ranges'] = 'bytes'
        
    else:
        # Petición completa (sin Range) - usar FileResponse para mejor rendimiento
        file_obj = open(full_path, 'rb')
        response = FileResponse(
            file_obj,
            content_type=content_type
        )
        response['Content-Length'] = str(file_size)
        response['Accept-Ranges'] = 'bytes'
    
    # Headers adicionales para caching
    response['Cache-Control'] = 'public, max-age=3600'  # 1 hora
    
    return response


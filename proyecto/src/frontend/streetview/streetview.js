/**
 * RECORRIDOS VIRTUALES - STUDENTSPOINT
 * Sistema de navegación con diapositivas para recorridos virtuales
 */

// ========================================
// VARIABLES GLOBALES
// ========================================

let currentSlide = 0;
let totalSlides = 0;
let currentRecorrido = null;
let touchStartX = 0;
let touchEndX = 0;
let banosCurrentRecorrido = null;
let banosCurrentFloor = null;
let banosLastView = null;

// Datos de recorridos disponibles
const recorridosData = {
    'maipu': {
        nombre: 'DuocUC Sede Maipú',
        recorridos: [
            {
                id: 'biblioteca',
                titulo: 'Biblioteca',
                descripcion: 'Explora nuestra biblioteca con recursos académicos',
                icono: 'fa-book',
                disponible: true,
                imagenes: [
                    {
                        url: '/imagenes/mapa/biblioteca/img1biblioteca.jpeg',
                        titulo: 'Entrada a la Biblioteca',
                        descripcion: 'Vista principal de la entrada a la biblioteca DuocUC'
                    },
                    {
                        url: '/imagenes/mapa/biblioteca/img2biblioteca.jpeg',
                        titulo: 'Zona de Recepción',
                        descripcion: 'Área de recepción y atención al usuario'
                    },
                    {
                        url: '/imagenes/mapa/biblioteca/img3biblioteca.jpeg',
                        titulo: 'Sala de Lectura',
                        descripcion: 'Amplio espacio de estudio y lectura silenciosa'
                    },
                    {
                        url: '/imagenes/mapa/biblioteca/img4biblioteca.jpeg',
                        titulo: 'Estantería de Libros',
                        descripcion: 'Colección de libros y material bibliográfico'
                    },
                    {
                        url: '/imagenes/mapa/biblioteca/img5biblioteca.jpeg',
                        titulo: 'Zona de Computadores',
                        descripcion: 'Área equipada con computadores para investigación'
                    },
                    {
                        url: '/imagenes/mapa/biblioteca/img6biblioteca.jpeg',
                        titulo: 'Salas de Estudio Grupal',
                        descripcion: 'Espacios para trabajo colaborativo y en equipo'
                    },
                    {
                        url: '/imagenes/mapa/biblioteca/img7biblioteca.jpeg',
                        titulo: 'Vista General',
                        descripcion: 'Vista panorámica de la biblioteca completa'
                    }
                ]
            },
            {
                id: 'casino',
                titulo: 'Casino',
                descripcion: 'Recorrido por el casino y espacios de alimentación',
                icono: 'fa-utensils',
                disponible: true,
                imagenes: [
                    {
                        url: '/imagenes/mapa/casino/img1casino.jpeg',
                        titulo: 'Entrada al Casino',
                        descripcion: 'Vista principal de la entrada al casino estudiantil'
                    },
                    {
                        url: '/imagenes/mapa/casino/img2casino.jpeg',
                        titulo: 'Área de Servicio',
                        descripcion: 'Zona de servicio y atención del casino'
                    },
                    {
                        url: '/imagenes/mapa/casino/img3casino.jpeg',
                        titulo: 'Comedor Principal',
                        descripcion: 'Amplio espacio del comedor para estudiantes'
                    },
                    {
                        url: '/imagenes/mapa/casino/img4casino.jpeg',
                        titulo: 'Zona de Mesas',
                        descripcion: 'Área de mesas y asientos para disfrutar tus alimentos'
                    },
                    {
                        url: '/imagenes/mapa/casino/img5casino.jpeg',
                        titulo: 'Vista General',
                        descripcion: 'Vista panorámica del casino estudiantil'
                    }
                ]
            },
            {
                id: 'administracion',
                titulo: 'Administración',
                descripcion: 'Conoce las oficinas administrativas',
                icono: 'fa-building',
                disponible: true,
                imagenes: [
                    {
                        url: '/imagenes/mapa/administracion/img1administracion.jpeg',
                        titulo: 'Entrada a Administración',
                        descripcion: 'Vista principal de la entrada a las oficinas administrativas'
                    },
                    {
                        url: '/imagenes/mapa/administracion/img2administracion.jpeg',
                        titulo: 'Recepción Administrativa',
                        descripcion: 'Área de recepción y atención al público'
                    },
                    {
                        url: '/imagenes/mapa/administracion/img3administracion.jpeg',
                        titulo: 'Oficinas Administrativas',
                        descripcion: 'Espacios de trabajo del personal administrativo'
                    },
                    {
                        url: '/imagenes/mapa/administracion/img4administracion.jpeg',
                        titulo: 'Sala de Reuniones',
                        descripcion: 'Espacio para reuniones y sesiones administrativas'
                    },
                    {
                        url: '/imagenes/mapa/administracion/img5administracion.jpeg',
                        titulo: 'Vista General',
                        descripcion: 'Vista panorámica de las oficinas administrativas'
                    }
                ]
            },
            {
                id: 'banos',
                titulo: 'Baños',
                descripcion: 'Ubica los baños por nivel y sector',
                icono: 'fa-restroom',
                disponible: true,
                tieneSubmenu: true,
                submenu: [
                    {
                        id: 'banos-subterraneo',
                        titulo: 'Baño Subterráneo',
                        descripcion: 'Selecciona la torre del subterráneo',
                        icono: 'fa-arrow-turn-down',
                        opciones: [
                            {
                                id: 'banos-subterraneo-a',
                                titulo: 'Baño Subterráneo - Torre 2',
                                descripcion: 'Cercano a laboratorios y salas técnicas',
                                icono: 'fa-toilet',
                                disponible: true,
                                imagenes: [
                                    {
                                        url: '/imagenes/mapa/baños/bañosubterraneo1/bañosubterraneoimg1.jpeg',
                                        titulo: 'Acceso Subterráneo Torre 2',
                                        descripcion: 'Ingreso principal al baño del subterráneo Torre 2'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañosubterraneo1/bañosubterraneoimg2.jpeg',
                                        titulo: 'Pasillo Subterráneo',
                                        descripcion: 'Pasillo que conecta con las salas del subterráneo'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañosubterraneo1/bañosubterraneoimg3.jpeg',
                                        titulo: 'Lavamanos Subterráneo Torre 2',
                                        descripcion: 'Zona de lavamanos e higienización'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañosubterraneo1/bañosubterraneoimg4.jpeg',
                                        titulo: 'Cubículos Subterráneo Torre 2',
                                        descripcion: 'Vista de los cubículos individuales'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañosubterraneo1/bañosubterraneoimg5.jpeg',
                                        titulo: 'Salida de Emergencia',
                                        descripcion: 'Salida cercana al baño del subterráneo'
                                    }
                                ]
                            },
                            {
                                id: 'banos-subterraneo-b',
                                titulo: 'Baño Subterráneo - Torre 3',
                                descripcion: 'Sector cercano al hub estudiantil subterráneo',
                                icono: 'fa-toilet',
                                disponible: true,
                                imagenes: [
                                    {
                                        url: '/imagenes/mapa/baños/banosubterraneo2/bañosubterraneoimg1.jpeg',
                                        titulo: 'Entrada Subterráneo Torre 3',
                                        descripcion: 'Ingreso al baño del subterráneo Torre 3'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/banosubterraneo2/bañosubterraneoimg2.jpeg',
                                        titulo: 'Pasillo Principal Torre 3',
                                        descripcion: 'Conexión hacia los servicios del subterráneo'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/banosubterraneo2/bañosubterraneoimg3.jpeg',
                                        titulo: 'Lavamanos Subterráneo Torre 3',
                                        descripcion: 'Área de lavamanos y espejos'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/banosubterraneo2/bañosubterraneoimg4.jpeg',
                                        titulo: 'Cubículos Subterráneo Torre 3',
                                        descripcion: 'Cubículos independientes de la Torre 3'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/banosubterraneo2/bañosubterraneoimg5.jpeg',
                                        titulo: 'Vista General Subterráneo Torre 3',
                                        descripcion: 'Panorámica del baño subterráneo Torre 3'
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        id: 'banos-piso1',
                        titulo: 'Baño Piso 1',
                        descripcion: 'Baños junto a recepción y admisiones',
                        icono: 'fa-layer-group',
                        opciones: [
                            {
                                id: 'banos-piso1-central',
                                titulo: 'Baño Piso 1',
                                descripcion: 'Punto sanitario principal del primer piso',
                                icono: 'fa-toilet-paper',
                                disponible: true,
                                imagenes: [
                                    {
                                        url: '/imagenes/mapa/baños/bañoprimerpiso/bañoprimerpisoimg1.jpeg',
                                        titulo: 'Entrada Piso 1',
                                        descripcion: 'Acceso principal a los baños del primer piso'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañoprimerpiso/bañoprimerpisoimg2.jpeg',
                                        titulo: 'Pasillo Piso 1',
                                        descripcion: 'Pasillo que conecta con la sala de espera'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañoprimerpiso/bañoprimerpisoimg3.jpeg',
                                        titulo: 'Lavamanos Piso 1',
                                        descripcion: 'Espacio de lavamanos y dispensadores'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañoprimerpiso/bañoprimerpisoimg4.jpeg',
                                        titulo: 'Cubículos Piso 1',
                                        descripcion: 'Zona de cubículos individuales'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañoprimerpiso/bañoprimerpisoimg5.jpeg',
                                        titulo: 'Acceso Universal',
                                        descripcion: 'Entrada adaptada para personas con movilidad reducida'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañoprimerpiso/bañoprimerpisoimg6.jpeg',
                                        titulo: 'Zona de Secado',
                                        descripcion: 'Secadores de mano y dispensadores de papel'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañoprimerpiso/bañoprimerpisoimg7.jpeg',
                                        titulo: 'Vista General Piso 1',
                                        descripcion: 'Panorámica completa del baño del primer piso'
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        id: 'banos-piso2',
                        titulo: 'Baño Piso 2',
                        descripcion: 'Selecciona la torre del segundo piso',
                        icono: 'fa-stairs',
                        opciones: [
                            {
                                id: 'banos-piso2-a',
                                titulo: 'Baño Piso 2 - Torre 2',
                                descripcion: 'Frente a las salas de innovación',
                                icono: 'fa-toilet',
                                disponible: true,
                                imagenes: [
                                    {
                                        url: '/imagenes/mapa/baños/bañosegundopiso1/bañosegundopisoimg1.jpeg',
                                        titulo: 'Entrada Piso 2 - Torre 2',
                                        descripcion: 'Ingreso principal a la Torre 2'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañosegundopiso1/bañosegundopisoimg2.jpeg',
                                        titulo: 'Pasillo Piso 2 - Torre 2',
                                        descripcion: 'Pasillo que conecta con las salas del nivel'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañosegundopiso1/bañosegundopisoimg3.jpeg',
                                        titulo: 'Lavamanos Piso 2 - Torre 2',
                                        descripcion: 'Área de lavamanos iluminada'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañosegundopiso1/bañosegundopisoimg4.jpeg',
                                        titulo: 'Cubículos Piso 2 - Torre 2',
                                        descripcion: 'Cubículos individuales de la Torre 2'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañosegundopiso1/bañosegundopisoimg5.jpeg',
                                        titulo: 'Zona Accesible Piso 2 - Torre 2',
                                        descripcion: 'Espacio adaptado para accesibilidad'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañosegundopiso1/bañosegundopisoimg6.jpeg',
                                        titulo: 'Pasillo Trasero Torre 2',
                                        descripcion: 'Conexión hacia los lockers'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañosegundopiso1/bañosegundopisoimg7.jpeg',
                                        titulo: 'Señalética Torre 2',
                                        descripcion: 'Referencia visual para ubicar la Torre 2'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañosegundopiso1/bañosegundopisoimg8.jpeg',
                                        titulo: 'Vista General Piso 2 - Torre 2',
                                        descripcion: 'Panorámica completa del baño Torre 2'
                                    }
                                ]
                            },
                            {
                                id: 'banos-piso2-b',
                                titulo: 'Baño Piso 2 - Torre 3',
                                descripcion: 'Sector cercano a las salas de docencia',
                                icono: 'fa-toilet',
                                disponible: true,
                                imagenes: [
                                    {
                                        url: '/imagenes/mapa/baños/bañosegundopiso2/bañosegundopisoimg1.jpeg',
                                        titulo: 'Entrada Piso 2 - Torre 3',
                                        descripcion: 'Ingreso a la Torre 3 del segundo piso'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañosegundopiso2/bañosegundopisoimg2.jpeg',
                                        titulo: 'Pasillo Piso 2 - Torre 3',
                                        descripcion: 'Pasillo principal de la Torre 3'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañosegundopiso2/bañosegundopisoimg3.jpeg',
                                        titulo: 'Lavamanos Piso 2 - Torre 3',
                                        descripcion: 'Zona de lavamanos amplia'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañosegundopiso2/bañosegundopisoimg4.jpeg',
                                        titulo: 'Cubículos Piso 2 - Torre 3',
                                        descripcion: 'Cubículos de la Torre 3'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañosegundopiso2/bañosegundopisoimg5.jpeg',
                                        titulo: 'Pasillo Posterior Torre 3',
                                        descripcion: 'Conexión hacia salas cercanas'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañosegundopiso2/bañosegundopisoimg6.jpeg',
                                        titulo: 'Señalética Torre 3',
                                        descripcion: 'Indicaciones de ubicación del baño'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañosegundopiso2/bañosegundopisoimg7.jpeg',
                                        titulo: 'Vista Cubículos Torre 3',
                                        descripcion: 'Detalle de los cubículos de la Torre 3'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañosegundopiso2/bañosegundopisoimg8.jpeg',
                                        titulo: 'Área de Higiene Torre 3',
                                        descripcion: 'Dispensadores y sanitización'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañosegundopiso2/bañosegundopisoimg9.jpeg',
                                        titulo: 'Corredor Torre 3',
                                        descripcion: 'Conexión hacia la escalera principal'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañosegundopiso2/bañosegundopisoimg10.jpeg',
                                        titulo: 'Lavamanos Secundario Torre 3',
                                        descripcion: 'Segunda área de lavamanos'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañosegundopiso2/bañosegundopisoimg11.jpeg',
                                        titulo: 'Zona Accesible Torre 3',
                                        descripcion: 'Espacio adaptado para accesibilidad'
                                    },
                                    {
                                        url: '/imagenes/mapa/baños/bañosegundopiso2/bañosegundopisoimg12.jpeg',
                                        titulo: 'Vista General Piso 2 - Torre 3',
                                        descripcion: 'Panorámica completa de la Torre 3'
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                id: 'punto-estudiantil',
                titulo: 'Punto Estudiantil',
                descripcion: 'Centro de atención y servicios estudiantiles',
                icono: 'fa-info-circle',
                disponible: true,
                imagenes: [
                    {
                        url: '/imagenes/mapa/puntoestudiantil/img1puntoestudiantil.jpeg',
                        titulo: 'Entrada al Punto Estudiantil',
                        descripcion: 'Vista principal del acceso al centro de atención estudiantil'
                    },
                    {
                        url: '/imagenes/mapa/puntoestudiantil/img2puntoestudiantil.jpeg',
                        titulo: 'Área de Atención',
                        descripcion: 'Zona de recepción y atención personalizada para estudiantes'
                    },
                    {
                        url: '/imagenes/mapa/puntoestudiantil/img3puntoestudiantil.jpeg',
                        titulo: 'Servicios Estudiantiles',
                        descripcion: 'Espacio de servicios y asesoría para la comunidad estudiantil'
                    },
                    {
                        url: '/imagenes/mapa/puntoestudiantil/img4puntoestudiantil.jpeg',
                        titulo: 'Vista General',
                        descripcion: 'Vista panorámica del punto de servicios estudiantiles'
                    }
                ]
            },
            {
                id: 'salas',
                titulo: 'Salas',
                descripcion: 'Busca y explora las salas de clases',
                icono: 'fa-chalkboard-teacher',
                disponible: true,
                tieneBuscador: true,
                imagenes: []
            }
        ]
    }
};

// Datos de salas disponibles organizadas por piso
const salasData = {
    // Piso 2 - Salas 200 a 211
    'piso2': {
        rango: '200-211',
        salas: {
            '200': {
                disponible: true,
                imagenes: [
                    { url: '/imagenes/mapa/Torre 1/Piso 2 - salas 200 a 211/torre1img1.webp', titulo: 'Entrada Sala 200', descripcion: 'Acceso principal a la sala 200' },
                    { url: '/imagenes/mapa/Torre 1/Piso 2 - salas 200 a 211/torre1img2.webp', titulo: 'Vista Interior Sala 200', descripcion: 'Vista del interior de la sala' },
                    { url: '/imagenes/mapa/Torre 1/Piso 2 - salas 200 a 211/torre1img3.webp', titulo: 'Área de Trabajo Sala 200', descripcion: 'Espacio de trabajo y estudio' },
                    { url: '/imagenes/mapa/Torre 1/Piso 2 - salas 200 a 211/torre1img4.webp', titulo: 'Equipamiento Sala 200', descripcion: 'Equipamiento y recursos disponibles' },
                    { url: '/imagenes/mapa/Torre 1/Piso 2 - salas 200 a 211/torre1img5.webp', titulo: 'Vista Panorámica Sala 200', descripcion: 'Vista completa de la sala' },
                    { url: '/imagenes/mapa/Torre 1/Piso 2 - salas 200 a 211/torre1img6.webp', titulo: 'Detalle Sala 200', descripcion: 'Detalles adicionales de la sala' },
                    { url: '/imagenes/mapa/Torre 1/Piso 2 - salas 200 a 211/torre1img7.webp', titulo: 'Área de Proyección Sala 200', descripcion: 'Zona de proyección y presentaciones' },
                    { url: '/imagenes/mapa/Torre 1/Piso 2 - salas 200 a 211/torre1img8.webp', titulo: 'Vista Final Sala 200', descripcion: 'Vista final del recorrido' }
                ]
            },
            '201': {
                disponible: true,
                imagenes: [
                    { url: '/imagenes/mapa/Torre 1/Piso 2 - salas 200 a 211/torre1img1.webp', titulo: 'Entrada Sala 201', descripcion: 'Acceso principal a la sala 201' },
                    { url: '/imagenes/mapa/Torre 1/Piso 2 - salas 200 a 211/torre1img2.webp', titulo: 'Vista Interior Sala 201', descripcion: 'Vista del interior de la sala' },
                    { url: '/imagenes/mapa/Torre 1/Piso 2 - salas 200 a 211/torre1img3.webp', titulo: 'Área de Trabajo Sala 201', descripcion: 'Espacio de trabajo y estudio' },
                    { url: '/imagenes/mapa/Torre 1/Piso 2 - salas 200 a 211/torre1img4.webp', titulo: 'Equipamiento Sala 201', descripcion: 'Equipamiento y recursos disponibles' },
                    { url: '/imagenes/mapa/Torre 1/Piso 2 - salas 200 a 211/torre1img5.webp', titulo: 'Vista Panorámica Sala 201', descripcion: 'Vista completa de la sala' },
                    { url: '/imagenes/mapa/Torre 1/Piso 2 - salas 200 a 211/torre1img6.webp', titulo: 'Detalle Sala 201', descripcion: 'Detalles adicionales de la sala' },
                    { url: '/imagenes/mapa/Torre 1/Piso 2 - salas 200 a 211/torre1img7.webp', titulo: 'Área de Proyección Sala 201', descripcion: 'Zona de proyección y presentaciones' },
                    { url: '/imagenes/mapa/Torre 1/Piso 2 - salas 200 a 211/torre1img8.webp', titulo: 'Vista Final Sala 201', descripcion: 'Vista final del recorrido' }
                ]
            }
            // Nota: Las salas 202-211 usarían las mismas imágenes por ahora
            // Se pueden agregar más salas específicas cuando haya imágenes dedicadas
        }
    },
    // Piso 3 - Salas 300 a 319
    'piso3': {
        rango: '300-319',
        salas: {
            '300': {
                disponible: true,
                imagenes: [
                    { url: '/imagenes/mapa/Torre 1/Piso 3 - salas 300 a 319/torre1img1.webp', titulo: 'Entrada Sala 300', descripcion: 'Acceso principal a la sala 300' },
                    { url: '/imagenes/mapa/Torre 1/Piso 3 - salas 300 a 319/torre1img2.webp', titulo: 'Vista Interior Sala 300', descripcion: 'Vista del interior de la sala' },
                    { url: '/imagenes/mapa/Torre 1/Piso 3 - salas 300 a 319/torre1img3.webp', titulo: 'Área de Trabajo Sala 300', descripcion: 'Espacio de trabajo y estudio' },
                    { url: '/imagenes/mapa/Torre 1/Piso 3 - salas 300 a 319/torre1img4.webp', titulo: 'Equipamiento Sala 300', descripcion: 'Equipamiento y recursos disponibles' },
                    { url: '/imagenes/mapa/Torre 1/Piso 3 - salas 300 a 319/torre1img5.webp', titulo: 'Vista Panorámica Sala 300', descripcion: 'Vista completa de la sala' },
                    { url: '/imagenes/mapa/Torre 1/Piso 3 - salas 300 a 319/torre1img6.webp', titulo: 'Detalle Sala 300', descripcion: 'Detalles adicionales de la sala' },
                    { url: '/imagenes/mapa/Torre 1/Piso 3 - salas 300 a 319/torre1img7.webp', titulo: 'Área de Proyección Sala 300', descripcion: 'Zona de proyección y presentaciones' },
                    { url: '/imagenes/mapa/Torre 1/Piso 3 - salas 300 a 319/torre1img8.webp', titulo: 'Vista Final Sala 300', descripcion: 'Vista final del recorrido' },
                    { url: '/imagenes/mapa/Torre 1/Piso 3 - salas 300 a 319/torre1img9.webp', titulo: 'Vista Adicional Sala 300', descripcion: 'Vista adicional de la sala' },
                    { url: '/imagenes/mapa/Torre 1/Piso 3 - salas 300 a 319/torre1img10.webp', titulo: 'Detalle Equipamiento Sala 300', descripcion: 'Detalle del equipamiento' },
                    { url: '/imagenes/mapa/Torre 1/Piso 3 - salas 300 a 319/torre1img11.webp', titulo: 'Vista Lateral Sala 300', descripcion: 'Vista lateral de la sala' },
                    { url: '/imagenes/mapa/Torre 1/Piso 3 - salas 300 a 319/torre1img12.webp', titulo: 'Vista General Sala 300', descripcion: 'Vista general completa' }
                ]
            }
            // Nota: Las salas 301-319 usarían las mismas imágenes por ahora
        }
    },
    // Piso 4 - Salas 401 a 403
    'piso4': {
        rango: '401-403',
        salas: {
            '401': {
                disponible: true,
                imagenes: [
                    { url: '/imagenes/mapa/Torre 1/Piso 4 - salas 401 a 403/torre1img1.webp', titulo: 'Entrada Sala 401', descripcion: 'Acceso principal a la sala 401' },
                    { url: '/imagenes/mapa/Torre 1/Piso 4 - salas 401 a 403/torre1img2.webp', titulo: 'Vista Interior Sala 401', descripcion: 'Vista del interior de la sala' },
                    { url: '/imagenes/mapa/Torre 1/Piso 4 - salas 401 a 403/torre1img3.webp', titulo: 'Área de Trabajo Sala 401', descripcion: 'Espacio de trabajo y estudio' },
                    { url: '/imagenes/mapa/Torre 1/Piso 4 - salas 401 a 403/torre1img4.webp', titulo: 'Equipamiento Sala 401', descripcion: 'Equipamiento y recursos disponibles' },
                    { url: '/imagenes/mapa/Torre 1/Piso 4 - salas 401 a 403/torre1img5.webp', titulo: 'Vista Panorámica Sala 401', descripcion: 'Vista completa de la sala' },
                    { url: '/imagenes/mapa/Torre 1/Piso 4 - salas 401 a 403/torre1img6.webp', titulo: 'Detalle Sala 401', descripcion: 'Detalles adicionales de la sala' },
                    { url: '/imagenes/mapa/Torre 1/Piso 4 - salas 401 a 403/torre1img7.webp', titulo: 'Área de Proyección Sala 401', descripcion: 'Zona de proyección y presentaciones' },
                    { url: '/imagenes/mapa/Torre 1/Piso 4 - salas 401 a 403/torre1img8.webp', titulo: 'Vista Final Sala 401', descripcion: 'Vista final del recorrido' },
                    { url: '/imagenes/mapa/Torre 1/Piso 4 - salas 401 a 403/torre1img9.webp', titulo: 'Vista Adicional Sala 401', descripcion: 'Vista adicional de la sala' },
                    { url: '/imagenes/mapa/Torre 1/Piso 4 - salas 401 a 403/torre1img10.webp', titulo: 'Detalle Equipamiento Sala 401', descripcion: 'Detalle del equipamiento' },
                    { url: '/imagenes/mapa/Torre 1/Piso 4 - salas 401 a 403/torre1img11.webp', titulo: 'Vista Lateral Sala 401', descripcion: 'Vista lateral de la sala' },
                    { url: '/imagenes/mapa/Torre 1/Piso 4 - salas 401 a 403/torre1img12.webp', titulo: 'Vista General Sala 401', descripcion: 'Vista general completa' },
                    { url: '/imagenes/mapa/Torre 1/Piso 4 - salas 401 a 403/torre1img13.webp', titulo: 'Vista Completa Sala 401', descripcion: 'Vista completa adicional' },
                    { url: '/imagenes/mapa/Torre 1/Piso 4 - salas 401 a 403/torre1img14.webp', titulo: 'Detalle Final Sala 401', descripcion: 'Detalle final del recorrido' },
                    { url: '/imagenes/mapa/Torre 1/Piso 4 - salas 401 a 403/torre1img15.webp', titulo: 'Vista Panorámica Final Sala 401', descripcion: 'Vista panorámica final' }
                ]
            }
            // Nota: Las salas 402-403 usarían las mismas imágenes por ahora
        }
    }
};

// Función auxiliar para determinar el piso y obtener datos de sala
function obtenerDatosSala(numeroSala) {
    const num = parseInt(numeroSala);
    
    if (isNaN(num)) return null;
    
    // Determinar piso basado en el número
    if (num >= 200 && num <= 211) {
        const piso = 'piso2';
        // Si la sala específica existe, usarla; si no, usar la 200 como template
        if (salasData[piso].salas[numeroSala]) {
            return {
                numero: numeroSala,
                piso: 2,
                ...salasData[piso].salas[numeroSala]
            };
        } else {
            // Usar sala 200 como template para otras salas del piso 2
            return {
                numero: numeroSala,
                piso: 2,
                disponible: true,
                imagenes: salasData[piso].salas['200'].imagenes.map(img => ({
                    ...img,
                    titulo: img.titulo.replace('200', numeroSala),
                    descripcion: img.descripcion.replace('200', numeroSala)
                }))
            };
        }
    } else if (num >= 300 && num <= 319) {
        const piso = 'piso3';
        if (salasData[piso].salas[numeroSala]) {
            return {
                numero: numeroSala,
                piso: 3,
                ...salasData[piso].salas[numeroSala]
            };
        } else {
            // Usar sala 300 como template
            return {
                numero: numeroSala,
                piso: 3,
                disponible: true,
                imagenes: salasData[piso].salas['300'].imagenes.map(img => ({
                    ...img,
                    titulo: img.titulo.replace('300', numeroSala),
                    descripcion: img.descripcion.replace('300', numeroSala)
                }))
            };
        }
    } else if (num >= 401 && num <= 403) {
        const piso = 'piso4';
        if (salasData[piso].salas[numeroSala]) {
            return {
                numero: numeroSala,
                piso: 4,
                ...salasData[piso].salas[numeroSala]
            };
        } else {
            // Usar sala 401 como template
            return {
                numero: numeroSala,
                piso: 4,
                disponible: true,
                imagenes: salasData[piso].salas['401'].imagenes.map(img => ({
                    ...img,
                    titulo: img.titulo.replace('401', numeroSala),
                    descripcion: img.descripcion.replace('401', numeroSala)
                }))
            };
        }
    }
    
    return null;
}

// ========================================
// INICIALIZACIÓN
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
});

function initializeApp() {
    // Reproducir sonido de carga si está disponible
        if (window.playSound) {
        setTimeout(() => window.playSound('pageLoad'), 500);
    }

    // Habilitar selector de sede
    const sedeSelect = document.getElementById('sede-select');
    if (sedeSelect) {
        sedeSelect.addEventListener('change', function() {
            const loadBtn = document.getElementById('load-btn');
            if (loadBtn) {
                loadBtn.disabled = !this.value;
            }
        });
    }
}

function setupEventListeners() {
    // Navegación con teclado
    document.addEventListener('keydown', handleKeyPress);

    // Touch events para swipe
    const slideContainer = document.getElementById('slideshow-container');
    if (slideContainer) {
        slideContainer.addEventListener('touchstart', handleTouchStart, { passive: true });
        slideContainer.addEventListener('touchend', handleTouchEnd, { passive: true });
    }
}

// ========================================
// NAVEGACIÓN PRINCIPAL
// ========================================

function loadRecorridos() {
    const sedeSelect = document.getElementById('sede-select');
    const sedeValue = sedeSelect.value;

    if (!sedeValue) return;

    const sedeData = recorridosData[sedeValue];
    if (!sedeData) return;

    // Actualizar título
    document.getElementById('sede-title').textContent = `Recorridos Disponibles - ${sedeData.nombre}`;

    // Renderizar cards de recorridos
    renderRecorridosCards(sedeData.recorridos);

    // Cambiar vista
    document.getElementById('sede-selector').style.display = 'none';
    document.getElementById('recorridos-container').style.display = 'block';

    // Reproducir sonido
    if (window.playSound) window.playSound('click');
}

function renderRecorridosCards(recorridos) {
    const container = document.getElementById('recorridos-list');
    container.innerHTML = '';

    recorridos.forEach(recorrido => {
        const col = document.createElement('div');
        col.className = 'col-md-6 col-lg-4';

        const card = document.createElement('div');
        card.className = `recorrido-card ${!recorrido.disponible ? 'disabled' : ''}`;

        if (recorrido.disponible || recorrido.tieneSubmenu || recorrido.tieneBuscador) {
            card.onclick = () => {
                if (recorrido.tieneSubmenu) {
                    showBanosSubmenu(recorrido);
                } else if (recorrido.tieneBuscador) {
                    showSalasBuscador(recorrido);
                } else {
                    startSlideshow(recorrido);
                }
            };
        }

        card.innerHTML = `
            <div class="recorrido-icon">
                <i class="fas ${recorrido.icono}"></i>
            </div>
            <h5>${recorrido.titulo}</h5>
            <p>${recorrido.descripcion}</p>
            ${!recorrido.disponible && !recorrido.tieneSubmenu ? '<span class="badge-proximamente">Próximamente</span>' : ''}
        `;

        col.appendChild(card);
        container.appendChild(col);
    });
}

function backToSelector() {
    document.getElementById('recorridos-container').style.display = 'none';
    document.getElementById('sede-selector').style.display = 'block';

    // Reproducir sonido
    if (window.playSound) window.playSound('click');
}

// ========================================
// SUBMENU DE BAÑOS
// ========================================

function showBanosSubmenu(recorrido) {
    banosCurrentRecorrido = recorrido;
    banosCurrentFloor = null;

    // Reiniciar vista de opciones específicas
    const opcionesContainer = document.getElementById('banos-opciones');
    const opcionesList = document.getElementById('banos-opciones-list');
    if (opcionesContainer) opcionesContainer.style.display = 'none';
    if (opcionesList) opcionesList.innerHTML = '';

    renderBanosFloors(recorrido);

    // Cambiar vista
    document.getElementById('recorridos-container').style.display = 'none';
    document.getElementById('banos-submenu').style.display = 'block';

    // Reproducir sonido
    if (window.playSound) window.playSound('click');
}

function renderBanosFloors(recorrido) {
    const container = document.getElementById('banos-list');
    if (!container) return;

    container.innerHTML = '';
    banosLastView = 'floors';

    const title = document.getElementById('banos-title');
    if (title) {
        title.textContent = 'Baños - DuocUC Sede Maipú';
    }

    recorrido.submenu.forEach(floor => {
        const col = document.createElement('div');
        col.className = 'col-md-6 col-lg-4';

        const card = document.createElement('div');
        card.className = 'recorrido-card';
        card.onclick = () => handleBanosFloorSelection(floor);

        const hasMultiple = floor.opciones && floor.opciones.length > 1;

        card.innerHTML = `
            <div class="recorrido-icon">
                <i class="fas ${floor.icono || 'fa-restroom'}"></i>
            </div>
            <h5>${floor.titulo}</h5>
            <p>${floor.descripcion || ''}</p>
            ${hasMultiple ? '<span class="badge-proximamente">2 torres</span>' : ''}
        `;

        col.appendChild(card);
        container.appendChild(col);
    });
}

function handleBanosFloorSelection(floor) {
    if (!floor) return;

    banosCurrentFloor = floor;

    const opciones = floor.opciones || [];

    if (opciones.length > 1) {
        renderBanosOpciones(floor);
        return;
    }

    if (opciones.length === 1) {
        startSlideshow(opciones[0]);
        return;
    }

    if (floor.imagenes && floor.imagenes.length > 0) {
        startSlideshow(floor);
        return;
    }

    showNotification('Este recorrido aún no está disponible', 'info');
}

function renderBanosOpciones(floor) {
    const opcionesContainer = document.getElementById('banos-opciones');
    const opcionesList = document.getElementById('banos-opciones-list');

    if (!opcionesContainer || !opcionesList) return;

    opcionesList.innerHTML = '';
    banosLastView = 'options';

    const title = document.getElementById('banos-opciones-title');
    if (title) {
        title.textContent = floor.titulo;
    }

    floor.opciones.forEach(opcion => {
        const col = document.createElement('div');
        col.className = 'col-md-6 col-lg-4';

        const card = document.createElement('div');
        card.className = 'recorrido-card';

        card.onclick = () => startSlideshow(opcion);

        card.innerHTML = `
            <div class="recorrido-icon">
                <i class="fas ${opcion.icono || 'fa-toilet'}"></i>
            </div>
            <h5>${opcion.titulo}</h5>
            <p>${opcion.descripcion || ''}</p>
        `;

        col.appendChild(card);
        opcionesList.appendChild(col);
    });

    document.getElementById('banos-submenu').style.display = 'none';
    opcionesContainer.style.display = 'block';
}

function backToBanosFloors() {
    const opcionesContainer = document.getElementById('banos-opciones');
    const opcionesList = document.getElementById('banos-opciones-list');
    if (opcionesContainer) opcionesContainer.style.display = 'none';
    if (opcionesList) opcionesList.innerHTML = '';

    banosCurrentFloor = null;
    banosLastView = 'floors';

    document.getElementById('banos-submenu').style.display = 'block';

    if (window.playSound) window.playSound('click');
}

function backToRecorridos() {
    document.getElementById('banos-submenu').style.display = 'none';
    const opcionesContainer = document.getElementById('banos-opciones');
    const opcionesList = document.getElementById('banos-opciones-list');
    const salasBuscador = document.getElementById('salas-buscador');
    if (opcionesContainer) opcionesContainer.style.display = 'none';
    if (opcionesList) opcionesList.innerHTML = '';
    if (salasBuscador) salasBuscador.style.display = 'none';
    banosCurrentRecorrido = null;
    banosCurrentFloor = null;
    banosLastView = null;
    document.getElementById('recorridos-container').style.display = 'block';

    // Reproducir sonido
    if (window.playSound) window.playSound('click');
}

// ========================================
// BUSCADOR DE SALAS
// ========================================

function showSalasBuscador(recorrido) {
    // Ocultar otros contenedores
    document.getElementById('recorridos-container').style.display = 'none';
    document.getElementById('banos-submenu').style.display = 'none';
    document.getElementById('banos-opciones').style.display = 'none';
    
    // Mostrar buscador
    document.getElementById('salas-buscador').style.display = 'block';
    
    // Limpiar input y mensaje
    const input = document.getElementById('sala-search-input');
    const mensaje = document.getElementById('sala-mensaje');
    if (input) input.value = '';
    if (mensaje) {
        mensaje.style.display = 'none';
        mensaje.className = 'alert';
    }
    
    // Enfocar input
    if (input) {
        setTimeout(() => input.focus(), 100);
    }
    
    // Reproducir sonido
    if (window.playSound) window.playSound('click');
}

function buscarSala() {
    const input = document.getElementById('sala-search-input');
    const mensaje = document.getElementById('sala-mensaje');
    
    if (!input || !mensaje) return;
    
    const numeroSala = input.value.trim();
    
    // Validar que no esté vacío
    if (!numeroSala) {
        mostrarMensajeSala('Por favor ingresa un número de sala', 'warning');
        return;
    }
    
    // Obtener datos de la sala
    const datosSala = obtenerDatosSala(numeroSala);
    
    if (!datosSala) {
        mostrarMensajeSala('Esta sala aún no está disponible', 'info');
        return;
    }
    
    if (!datosSala.disponible) {
        mostrarMensajeSala('Esta sala aún no está disponible', 'info');
        return;
    }
    
    if (!datosSala.imagenes || datosSala.imagenes.length === 0) {
        mostrarMensajeSala('Esta sala aún no está disponible', 'info');
        return;
    }
    
    // Crear objeto recorrido para el slideshow
    const recorridoSala = {
        id: `sala-${datosSala.numero}`,
        titulo: `Sala ${datosSala.numero}`,
        descripcion: `Recorrido virtual de la Sala ${datosSala.numero} - Piso ${datosSala.piso}`,
        icono: 'fa-chalkboard-teacher',
        disponible: true,
        imagenes: datosSala.imagenes
    };
    
    // Ocultar buscador
    document.getElementById('salas-buscador').style.display = 'none';
    
    // Iniciar slideshow
    startSlideshow(recorridoSala);
}

function mostrarMensajeSala(texto, tipo) {
    const mensaje = document.getElementById('sala-mensaje');
    if (!mensaje) return;
    
    mensaje.textContent = texto;
    mensaje.className = `alert alert-${tipo}`;
    mensaje.style.display = 'block';
    
    // Auto-ocultar después de 4 segundos
    setTimeout(() => {
        mensaje.style.display = 'none';
    }, 4000);
}

// ========================================
// VISOR DE DIAPOSITIVAS
// ========================================

function startSlideshow(recorrido) {
    if (recorrido.disponible === false || !recorrido.imagenes || recorrido.imagenes.length === 0) {
        showNotification('Este recorrido aún no está disponible', 'info');
        return;
    }

    currentRecorrido = recorrido;
    totalSlides = recorrido.imagenes.length;
    currentSlide = 0;

    // Actualizar información del header
    document.getElementById('slideshow-titulo').textContent = recorrido.titulo;
    document.getElementById('slideshow-subtitulo').textContent = 'DuocUC Sede Maipú';

    // Renderizar slides
    renderSlides();

    // Renderizar dots
    renderDots();

    // Mostrar visor
    document.getElementById('recorridos-container').style.display = 'none';
    const banosSubmenu = document.getElementById('banos-submenu');
    const banosOpciones = document.getElementById('banos-opciones');
    const salasBuscador = document.getElementById('salas-buscador');
    if (banosSubmenu) banosSubmenu.style.display = 'none';
    if (banosOpciones) banosOpciones.style.display = 'none';
    if (salasBuscador) salasBuscador.style.display = 'none';
    document.getElementById('slideshow-container').style.display = 'flex';

    // Actualizar navegación
    updateSlideNavigation();

    // Reproducir sonido
    if (window.playSound) window.playSound('click');

    // Precargar siguiente imagen
    preloadNextImage();
}

function renderSlides() {
    const container = document.getElementById('slide-container');
    container.innerHTML = '';

    currentRecorrido.imagenes.forEach((imagen, index) => {
        const slide = document.createElement('div');
        slide.className = `slide ${index === 0 ? 'active' : ''}`;

        const img = document.createElement('img');
        img.src = imagen.url;
        img.alt = imagen.titulo;
        img.loading = index === 0 ? 'eager' : 'lazy';

        // Agregar título y descripción overlay (opcional para mobile)
        const overlay = document.createElement('div');
        overlay.className = 'slide-overlay';
        overlay.innerHTML = `
            <div class="slide-info">
                <h3>${imagen.titulo}</h3>
                <p>${imagen.descripcion}</p>
            </div>
        `;

        slide.appendChild(img);
        // Descomentar si quieres overlay en las imágenes
        // slide.appendChild(overlay);
        
        container.appendChild(slide);
    });
}

function renderDots() {
    const container = document.getElementById('slideshow-dots');
    container.innerHTML = '';

    for (let i = 0; i < totalSlides; i++) {
        const dot = document.createElement('div');
        dot.className = `dot ${i === 0 ? 'active' : ''}`;
        dot.onclick = () => goToSlide(i);
        container.appendChild(dot);
    }
}

function updateSlideNavigation() {
    // Actualizar contador
    document.getElementById('slide-counter').textContent = `${currentSlide + 1} / ${totalSlides}`;

    // Actualizar barra de progreso
    const progress = ((currentSlide + 1) / totalSlides) * 100;
    document.getElementById('progress-bar').style.width = `${progress}%`;
        
        // Actualizar botones
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');

    if (prevBtn) prevBtn.disabled = currentSlide === 0;
    if (nextBtn) nextBtn.disabled = currentSlide === totalSlides - 1;

    // Actualizar dots
    const dots = document.querySelectorAll('.dot');
    dots.forEach((dot, index) => {
        dot.classList.toggle('active', index === currentSlide);
    });

    // Actualizar slides
    const slides = document.querySelectorAll('.slide');
    slides.forEach((slide, index) => {
        slide.classList.toggle('active', index === currentSlide);
    });
}

function nextSlide() {
    if (currentSlide < totalSlides - 1) {
        currentSlide++;
        updateSlideNavigation();
        preloadNextImage();
        if (window.playSound) window.playSound('navigate');
    }
}

function previousSlide() {
    if (currentSlide > 0) {
        currentSlide--;
        updateSlideNavigation();
        if (window.playSound) window.playSound('navigate');
    }
}

function goToSlide(index) {
    if (index >= 0 && index < totalSlides && index !== currentSlide) {
        currentSlide = index;
        updateSlideNavigation();
        preloadNextImage();
        if (window.playSound) window.playSound('click');
    }
}

function exitSlideshow() {
    document.getElementById('slideshow-container').style.display = 'none';

    const banosSubmenu = document.getElementById('banos-submenu');
    const banosOpciones = document.getElementById('banos-opciones');
    const salasBuscador = document.getElementById('salas-buscador');

    // Verificar si venimos de una sala
    if (currentRecorrido && currentRecorrido.id && currentRecorrido.id.startsWith('sala-')) {
        if (salasBuscador) {
            salasBuscador.style.display = 'block';
        } else {
            document.getElementById('recorridos-container').style.display = 'block';
        }
    } else if (banosCurrentRecorrido) {
        if (banosLastView === 'options' && banosOpciones) {
            banosOpciones.style.display = 'block';
        } else if (banosSubmenu) {
            banosSubmenu.style.display = 'block';
        }
    } else {
        document.getElementById('recorridos-container').style.display = 'block';
    }

    // Limpiar
    currentRecorrido = null;
    currentSlide = 0;
    totalSlides = 0;

    // Reproducir sonido
    if (window.playSound) window.playSound('click');
}

function preloadNextImage() {
    if (currentSlide < totalSlides - 1) {
        const nextImage = new Image();
        nextImage.src = currentRecorrido.imagenes[currentSlide + 1].url;
    }
}

// ========================================
// CONTROLES DE TECLADO
// ========================================

function handleKeyPress(e) {
    // Solo funciona si el visor está activo
    const slideshowContainer = document.getElementById('slideshow-container');
    if (!slideshowContainer || slideshowContainer.style.display === 'none') return;

    switch(e.key) {
        case 'ArrowRight':
        case ' ':
            e.preventDefault();
            nextSlide();
            break;
        case 'ArrowLeft':
            e.preventDefault();
            previousSlide();
            break;
        case 'Escape':
            e.preventDefault();
            exitSlideshow();
            break;
        case 'Home':
            e.preventDefault();
            goToSlide(0);
            break;
        case 'End':
            e.preventDefault();
            goToSlide(totalSlides - 1);
            break;
    }
}

// ========================================
// GESTOS TOUCH (SWIPE)
// ========================================

function handleTouchStart(e) {
    touchStartX = e.changedTouches[0].screenX;
}

function handleTouchEnd(e) {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
}

function handleSwipe() {
    const swipeThreshold = 50; // mínimo de píxeles para considerar swipe
    const difference = touchStartX - touchEndX;

    if (Math.abs(difference) < swipeThreshold) return;

    if (difference > 0) {
        // Swipe left - siguiente
        nextSlide();
    } else {
        // Swipe right - anterior
        previousSlide();
    }
}

// ========================================
// UTILIDADES
// ========================================

function showNotification(message, type = 'info') {
    // Crear notificación temporal
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
    alertDiv.style.zIndex = '10000';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);

    // Auto-eliminar después de 3 segundos
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

function logout() {
    // Implementar lógica de logout según tu sistema
    if (confirm('¿Deseas cerrar sesión?')) {
        localStorage.clear();
        sessionStorage.clear();
        window.location.href = '/login.html';
    }
}

// ========================================
// EXPORTAR FUNCIONES GLOBALES
// ========================================

// Hacer funciones accesibles globalmente para onclick en HTML
window.loadRecorridos = loadRecorridos;
window.backToSelector = backToSelector;
window.backToRecorridos = backToRecorridos;
window.backToBanosFloors = backToBanosFloors;
window.buscarSala = buscarSala;
window.nextSlide = nextSlide;
window.previousSlide = previousSlide;
window.goToSlide = goToSlide;
window.exitSlideshow = exitSlideshow;
window.logout = logout;

console.log('✅ Recorridos Virtuales - Sistema cargado correctamente');

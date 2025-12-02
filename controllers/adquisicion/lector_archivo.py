import csv
import json
import os
from models.libro import Libro

class LectorArchivo:
    """
    Class responsible for loading book data from a .csv or .json file
    """

    @staticmethod
    def cargar_csv(ruta_archivo: str):
        """
        Method for loading books from a CSV file.

        The CSV file must have the same attributes as the book.py class.

        Args:
            ruta_archivo (str): Path to the CSV file to load.

        Returns:
            list: List of Book objects loaded from the CSV file.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file format does not match.
        """
        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError(f"El archivo {ruta_archivo} no existe")
        
        libros = []

        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)

            for linea_num, fila in enumerate(lector, start=2):
                try:
                    libro = Libro(
                        isbn=fila['isbn'].strip(),
                        titulo=fila['titulo'].strip(),
                        autor=fila['autor'].strip(),
                        peso=float(fila['peso']),
                        valor=float(fila['valor']),
                        genero=fila['genero'].strip(),
                        cantidad_disponible=int(fila.get('cantidad_disponible', 1)),
                        cantidad_total=int(fila.get('cantidad_total', 1))
                    )
                    libros.append(libro)

                except KeyError as e:
                    raise ValueError(f"Columna faltante en línea {linea_num}: {e}"
                    )
                except ValueError as e:
                    raise ValueError(f"Error en línea {linea_num}: {e}"
                    )
        print(f"Se cargaron {len(libros)} libros desde {ruta_archivo}")
        return libros
    
    @staticmethod
    def cargar_json(ruta_archivo: str):
        """
        Method for loading books from a JSON file.

        The JSON file must have the same attributes as the libro.py class.

        Args:
            ruta_archivo (str): Path to the JSON file to load.

        Returns:
            list: List of Book objects loaded from the JSON file.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file format does not match.
        """
        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError(f"El archivo {ruta_archivo} no existe")
        
        libros = []

        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)

            if not isinstance(datos, list):
                raise ValueError("El archivo JSON debe contener un arreglo de libros")
            
            for idx, item in enumerate(datos):
                try:
                    libro = Libro(
                        isbn=item['isbn'],
                        titulo=item['titulo'],
                        autor=item['autor'],
                        peso=float(item['peso']),
                        valor=float(item['valor']),
                        genero=item['genero'],
                        cantidad_disponible=int(item.get('cantidad_disponible', 1)),
                        cantidad_total=int(item.get('cantidad_total', 1))
                    )
                    libros.append(libro)

                except KeyError as e:
                    raise ValueError(f"Falta una propiedad en {idx}: {e}")
                except ValueError as e:
                    raise ValueError(f"Error en el elemento {idx}: {e}")
        print(f"Se cargaron {len(libros)} libros desde {ruta_archivo}")
        return libros
    
    @staticmethod
    def cargar_libros(ruta_archivo: str):
        """
        Method for automatically detecting the file format.

        Detects the file type by its extension and calls the corresponding method.

        Args:
            ruta_archivo (str): Path to the file to load.

        Returns:
            list: List of Book objects loaded from the file.

        Raises:
            ValueError: If the file format is not supported.
        """
        extension = os.path.splitext(ruta_archivo)[1].lower()
        if extension == '.csv':
            return LectorArchivo.cargar_csv(ruta_archivo)
        elif extension == '.json':
            return LectorArchivo.cargar_json(ruta_archivo)
        else:
            raise ValueError(
                f"Formato de archivo no soportado: {extension}. "
                "Solo se soportan .csv y .json"
            )
        
    @staticmethod
    def guardar_csv(libros: list, ruta_archivo: str):
        """
        Save a list of books in CSV format

        Args:
            libros (list): List of Book objects to save.
            ruta_archivo (str): Path where to save the CSV file.
        """
        with open(ruta_archivo, 'w', encoding='utf-8', newline='') as archivo:
            campos = [
                'isbn', 'titulo', 'autor', 'peso', 
                'valor', 'genero', 'cantidad_disponible', 'cantidad_total', 'estante_id'
            ]
            escritor = csv.DictWriter(archivo, fieldnames=campos)

            escritor.writeheader()
            for libro in libros:
                escritor.writerow({
                    'isbn': libro.isbn,
                    'titulo': libro.titulo,
                    'autor': libro.autor,
                    'peso': libro.peso,
                    'valor': libro.valor,
                    'genero': libro.genero,
                    'cantidad_disponible': libro.cantidad_disponible,
                    'cantidad_total': libro.cantidad_total,
                    'estante_id': libro.estante_id
                })
        print(f"Se guardaron {len(libros)} libros en {ruta_archivo}")

    @staticmethod
    def guardar_json(libros: list, ruta_archivo: str):
        """
        Save a list of books in JSON format.

        Args:
            libros (list): List of Book objects to save.
            ruta_archivo (str): Path where to save the JSON file.
        """
        datos = []
        for libro in libros:
            datos.append({
                'isbn': libro.isbn,
                'titulo': libro.titulo,
                'autor': libro.autor,
                'peso': libro.peso,
                'valor': libro.valor,
                'genero': libro.genero,
                'cantidad_disponible': libro.cantidad_disponible,
                'cantidad_total': libro.cantidad_total,
                'estante_id': libro.estante_id
            })
        
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=2)
        print(f"Se guardaron {len(libros)} libros en {ruta_archivo}")
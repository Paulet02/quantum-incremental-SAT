# quantum-incremental-SAT

El este proyecto consta de 2 partes, el generador de problemas SAT y el solver cuántico.
Para hacer uso de ambos primero necesitamos tener instalado Python 3.7 o superior y las librerias que necesita. Estas librerías las podemos obtener ejecutando el siguiente comando en la raíz del proyecto:
```console
$ pip install -r requirements.txt
```
Una vez tengamos instalado todo lo necesario ya ponemos hace uso de ambas utilidades.

## Generador
El generador (generator.py) permite generar problemas k-SAT con diferentes densidades, número de variables, número de problemas a genearar, además de poder ponerle una semilla. Estos ejemplos los genera por defecto en la raíz dentro del directorio \benchmark. Los argumentos que acepta son:

-v,--variables: A list with the number of variables in the SAT problems, required=True \
-k,--ksat: A list with the number of variables per clause in the SAT problems, required=True \
-d,--densities: A list with the densities in the SAT problems, required=True \
-e,--examples: The number of SAT problems per case, required=True \
-s,--seed: Seed for the random generator, required=False \
-p,--path: Path for the benchmark folder, required=False 

El conjunto de problemas que viene generado en el repositorio se ha generado con en siguiente comando ejecutado en la raíz:

```console
$ python generator.py -v 5 6 7 8 9 10 11 12 13 14 15 16 --densities 2 3 4 5 -k 3 -e 10 --seed 1
```

Para generar un nuevo conjunto de problemas es necesario eliminar previamente el directorio \benchmark.

## Solver
El solver sirve para resolver todos los problemas que hay dentro del directorio \benchmark con el algoritmo propuesto en el artículo. Consta de un sistema de progreso que permite pararlo y ejecutarlo volviendo al punto en el que se encontraba. El fichero donde va guardando los resultados se llama "results.pickle" y lo crea en la raíz. Si se ve que está consumiendo mucha memoria RAM puede pararse con "Ctrl+C" y volver a lanzarlo partiendo del estado en el que se quedó pero con la memoria RAM liberada. Cuando el algoritmo termina de resolver todos los problemas, genera un fichero csv (export_dataframe.csv) con los datos de los resultados. Este solver ejecuta cada problema 5 veces con diferentes semillas.

Para ejecutar el solver hay que ejecutar el siguiente comando en la raíz del proyecto:

```console
$ python main.py
```

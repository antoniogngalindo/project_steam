# project_steam

Este proyecto hay como objetivo principal de desarrollar un MVP (Minimum Viable Product - Producto Mínimo Viable) con un sistema de recomendación de juegos basado en género y análisis de sentimiento de reseñas de usuarios, usando librerias scikit-learn y texblob, respectivamente. 

## Procesos hechos en este proyecto:

 - Atención: cada notebook ``(.ipynb)`` en este proyecto tiene paso a paso explicado de que se fue hecho en cada momento.

### Transformaciones:

En el contexto de este MVP, se requiere aplicar algunas transformaciones en los datos para prepararlos de forma adecuada y optimizar tanto el rendimiento de la API como el entrenamiento de modelos de aprendizaje automático. A continuación, se mencionan las transformaciones sugeridas:

1. Fue necesario transformar los datasets del formato JSON para CSV.

2. Formato de datos: Es importante asegurarse de que los datos se encuentren en el formato correcto para su procesamiento. Esto implica verificar los tipos de datos de cada columna y realizar las conversiones necesarias.

3. Eliminación de columnas no utilizadas: Para optimizar el rendimiento y reducir la cantidad de datos que se envían a través de la API, se pueden eliminar las columnas que no son necesarias para responder las consultas o preparar los modelos de aprendizaje automático. Esto reducirá el tamaño de los datos y acelerará el procesamiento.

4. Calculo de outliers por `Rango intercuartil (IQR)` para identificar y tratar los valores atípicos en los datos. Los outliers pueden afectar negativamente el rendimiento de los modelos de aprendizaje automático y distorsionar los resultados de las consultas.

### Feature Engineering:

El feature engineering consiste en crear nuevas variables o transformar las existentes para mejorar el rendimiento y la calidad de los modelos de aprendizaje automático. En el contexto de este proyecto, se propone realizar la siguiente tarea de feature engineering:

1. Análisis de sentimiento: En el dataset 'user_reviews', se incluyen reseñas de juegos realizadas por diferentes usuarios. Se puede aplicar análisis de sentimiento utilizando técnicas de procesamiento de lenguaje natural (NLP) para asignar un valor numérico que represente el sentimiento de cada reseña. Se asignó el valor '0' si la reseña es considerada negativa, '1' si es neutral y '2' si es positiva. Uso de la libreria ``textblob``

### Desarrollo API 

Este MVP se quedará disponible en el FrameWork FastApi, donde  se puede ser consumida segun los criterios de API REST o RESTful, en el seguinte link:

###  https://project-steam-nk7v.onrender.com/docs

También incluirá las siguientes funciones:

1. PlayTimeGenre: Permitirá a los usuarios encontrar el año de lanzamiento con más horas jugadas para un género específico. Esto les ayudará a descubrir los juegos más populares en un género en particular.

2. UserForGenre: Permitirá a los usuarios identificar el usuario que acumula la mayor cantidad de horas jugadas para un género determinado. Además, se proporcionará una lista que muestra la acumulación de horas jugadas por año para ese género, lo que les permitirá conocer la evolución de su tiempo de juego en relación con ese género.

3. UsersRecommend: Ofrecerá a los usuarios una lista del top 3 de juegos más recomendados por otros usuarios para un año específico. Estos juegos serán seleccionados en función de las recomendaciones positivas o neutrales y los comentarios favorables de los usuarios, lo que ayudará a los usuarios a descubrir nuevos juegos populares y bien valorados.

4. UsersNotRecommend: Proporcionará a los usuarios una lista del top 3 de juegos menos recomendados por otros usuarios para un año determinado. Estos juegos serán seleccionados en función de las recomendaciones negativas y los comentarios desfavorables de los usuarios, lo que permitirá a los usuarios evitar juegos que han recibido críticas negativas.

5. Sentiment_analysis: Mostrará a los usuarios una lista que representa el análisis de sentimiento de las reseñas de usuarios para un año específico. La lista incluirá la clasificación como "Negativo", "Neutral" y "Positivo", lo que permitirá a los usuarios tener una visión general de la recepción de los juegos en ese año.


### Modelo de aprendizaje automático

Fue utilizado el modelo Similitud de Cosenos por la libreria ``Scikit-Learn`` (DOCUMENTACIÓN: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html) para crear la matriz de similitudes y guardarlo en formato ``.pkl`` con la libreria ``Joblib``.

La similitud de cosenos es una medida utilizada para calcular la similitud entre dos vectores en un espacio vectorial. Es una métrica comúnmente utilizada en tareas como recuperación de información, minería de texto y recomendación de elementos. 

En el contexto de la recomendación de juegos por géneros, podemos utilizar la similitud de cosenos para determinar qué tan similares son los juegos en función de sus géneros. La idea es representar cada juego como un vector donde cada componente del vector representa un género, y luego calcular la similitud de cosenos entre los vectores de los juegos.

Para hacer esto, podemos utilizar la función cosine_similarity de scikit-learn. Esta función toma como entrada matrices de vectores y devuelve una matriz de similitudes de cosenos. Cada elemento de la matriz de salida representa la similitud de cosenos entre un par de vectores. Los valores de similitud oscilan entre -1 y 1, donde 1 indica una similitud máxima y -1 indica una similitud mínima.

### VIDEO:

https://drive.google.com/file/d/1CS8GckJox6m1xIaiPgeNaVHLUPRK4yFo/view?usp=sharing
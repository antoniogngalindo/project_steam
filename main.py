from fastapi import FastAPI
import uvicorn
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()


df_PlayTimeGenre = pd.read_csv('PlayTimeGenre.csv', low_memory= True)
df_UserForGenre = pd.read_csv('UserForGenre.csv', low_memory= True)
df_recommend = pd.read_csv('Recommend_functions.csv', low_memory= True)
df_sentiment_analysis = pd.read_csv('sentiment_analysis_function.csv', low_memory= True)
df_recomendacion_juego = pd.read_csv('recomendacion_juego_function.csv', low_memory= True)


@app.get("/Play_Time_Genre/{genero}", name='Año con mas horas jugadas para el género ingresado')

def PlayTimeGenre( genero : str ):
    filtro = df_PlayTimeGenre[df_PlayTimeGenre['most_played_genre']== genero]
    if len(filtro)>=1:
        max_playtime = filtro['playtime_forever'].max()
        max_year = filtro.loc[filtro['playtime_forever'] == max_playtime, 'year'].values[0]
        return {'Año de lanzamiento con más horas jugadas para ' + genero: int(max_year) }

    else:
        return {'No sé encontró el Género'}
    


@app.get("/User_For_Genre/{genero}", name='Usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.')

def UserForGenre(genero: str):
    filtro = df_UserForGenre[df_UserForGenre['most_played_genre'] == genero]
    if len(filtro) >= 1:
        user_playtime = filtro.groupby('user_id')['playtime_forever'].sum().reset_index()
        most_played_user = user_playtime.loc[user_playtime['playtime_forever'].idxmax(), 'user_id']
        
        horas_jugadas = []
        for year in filtro['year'].unique():
            playtime = filtro[(filtro['user_id'] == most_played_user) & (filtro['year'] == year)]['playtime_forever'].sum()
            if playtime > 0:
                hora_por_ano = {'Año': int(year), 'Horas': int(playtime)}
                horas_jugadas.append(hora_por_ano)

        return {f'Usuário com mais horas jogadas para {genero}: {most_played_user} , Horas jogadas: {horas_jugadas}'}
    else:
        return {'No sé encontró el Género'}
    
@app.get("/UsersRecommend/{year}", name='Top 3 de juegos MÁS recomendados por usuarios para el año dado.')

def UsersRecommend(year: int):
    filtro = df_recommend[df_recommend['year'] == year]
    if len(filtro) > 1:
        recomend = filtro[filtro['recommend'] == True]
        polaridad = recomend.nlargest(3, 'polaridad').reset_index(drop= True)
        resultado = {}
        for i, row in polaridad.iterrows():
            game = "Puesto " + str(i + 1 - polaridad.index[0])
            resultado[game] = row['title']
        
        return resultado
    else:
        return {f'Año no encuentrado!'}
    
@app.get("/UsersNotRecommend/{year}", name='Top 3 de juegos MENOS recomendados por usuarios para el año dado.')

def UsersNotRecommend( year : int ):
    filtro = df_recommend[df_recommend['year'] == year]
    if len(filtro) > 1:
        recomend = filtro[filtro['recommend'] == False]
        polaridad = recomend.nsmallest(3, 'polaridad').reset_index(drop= True)
        resultado = {}
        for i, row in polaridad.iterrows():
            game = "Puesto " + str(i + 1 - polaridad.index[0])
            resultado[game] = row['title']
        
        return resultado
    else:
        return {f'Año no encuentrado!'}
        

@app.get("/Sentiment_Analysis/{year}", name='Lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.')

def sentiment_analysis( year : int ):
    filtro = df_sentiment_analysis[df_sentiment_analysis['year']== year]
    
    if len(filtro) > 0:
        sentimientos = filtro[['Negativo', 'Neutro', 'Positivo']]

        return sentimientos.to_dict(orient = 'records')

    
    else: 
        return {f'Año no encuentrado!'}


@app.get("/Recomendacion_Juego/{id_producto}", name='5 juegos recomendados similares al ID ingresado')

def recomendacion_juego(id_producto: int):
    
    if id_producto in df_recomendacion_juego['item_id'].values:
        index = df_recomendacion_juego[df_recomendacion_juego['item_id'] == id_producto].index[0]
        similarities = cosine_similarity(df_recomendacion_juego.iloc[:, 1:-1])
        similar_indices = similarities[index].argsort()[::-1][1:6]
        similar_products = df_recomendacion_juego.iloc[similar_indices][['item_id', 'title']]
        return similar_products.to_dict(orient='records')
    else:
        return 'ID no encontrado'
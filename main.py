from fastapi import FastAPI
import uvicorn
import pandas as pd

app = FastAPI()


df_PlayTimeGenre = pd.read_csv('PlayTimeGenre.csv', low_memory= False)
df_UserForGenre = pd.read_csv('UserForGenre.csv', low_memory= False)
df_recommend = pd.read_csv('Recommend_functions.csv', low_memory= False)
df_sentiment_analysis = pd.read_csv('sentiment_analysis_function.csv')


@app.get("/PlayTimeGenre/{genero}", name='Año con mas horas jugadas para el género ingresado')

def PlayTimeGenre( genero : str ):
    filtro = df_PlayTimeGenre[df_PlayTimeGenre['most_played_genre']== genero]
    if len(filtro)>=1:
        max_playtime = filtro['playtime_forever'].max()
        max_year = filtro.loc[filtro['playtime_forever'] == max_playtime, 'year'].values[0]
        return {'Año de lanzamiento con más horas jugadas para Género' + int(max_year) : {genero}}
    else:
        return {'No sé encontró el Género'}
    


@app.get("/UserForGenre/{genero}", name='Usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.')

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

        return {'Usuário com mais horas jogadas para' + {genero}: {most_played_user}, 'Horas jogadas': {horas_jugadas}}
    else:
        return {'No sé encontró el Género'}
    
@app.get("/UsersRecommend/{año}", name='Top 3 de juegos MÁS recomendados por usuarios para el año dado.')

def UsersRecommend(año: int):
    filtro = df_recommend[df_recommend['year'] == año]
    if len(filtro) > 1:
        recomend = filtro[filtro['recommend'] == True]
        polaridad = recomend.nlargest(3, 'polaridad')
        resultado = []
        for puesto, (i, row) in enumerate(polaridad.iterrows(), start=1):
            game = row['title']
            resultado.append({f'Puesto {puesto}: {game}'})
        
        return resultado
    else:
        return {f'Año no encuentrado!'}
    
@app.get("/UsersNotRecommend/{año}", name='Top 3 de juegos MENOS recomendados por usuarios para el año dado.')

def UsersNotRecommend( año : int ):
    filtro = df_recommend[df_recommend['year'] == año]
    if len(filtro) > 1:
        recomend = filtro[filtro['recommend'] == False]
        polaridad = recomend.nsmallest(3, 'polaridad')
        resultado = []
        for puesto, (i, row) in enumerate(polaridad.iterrows(), start=1):
            game = row['title']
            resultado.append({f'Puesto {puesto}: {game}'})
        
        return resultado
    else:
        return {f'Año no encuentrado!'}
        

@app.get("/Sentiment_Analysis/{año}", name='Lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.')

def sentiment_analysis( año : int ):
    filtro = df_sentiment_analysis[df_sentiment_analysis['year']== año]
    negativo = 0
    neutro = 0
    positivo = 0
    if len(filtro) > 0:
        negativo = filtro[filtro['significado']== 'Negativo']['significado'].count()
        neutro = filtro[filtro['significado']== 'Neutro']['significado'].count()
        positivo = filtro[filtro['significado']== 'Positivo']['significado'].count()
        return {'Negativo': negativo, 'Neutral': neutro, 'Positivo': positivo}
    
    else: 
        return {f'Año no encuentrado!'}



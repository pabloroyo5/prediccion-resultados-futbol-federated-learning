from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import tensorflow as tf

app = Flask(__name__)

app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})



@app.route('/api/countries', methods=['GET'])
def get_countries():
    # Lee el archivo CSV
    df = pd.read_csv('data/countries.csv')
    # Convierte el dataframe a diccionario
    countries = df.to_dict(orient='records')
    return jsonify(countries)

@app.route('/api/leagues/<int:country>', methods=['GET'])
def get_league_by_country(country):
    # Lee el archivo CSV
    df = pd.read_csv('data/leagues.csv')
    # Filtra las ligas por país
    df = df[df['country_id'] == country]
    # Convierte el dataframe a diccionario
    leagues = df.to_dict(orient='records')
    return jsonify(leagues)

# get the posibles unique stages for a given country and a given year from matches.csv
@app.route('/api/stages/<int:country>/<int:year>', methods=['GET'])
def get_stages_by_league(country, year):
    # Lee el archivo CSV
    df = pd.read_csv('data/matches.csv')
    # Filtra los partidos por liga y año
    df = df[(df['country_id'] == country) & (df['year'] == year)]
    # Obtiene las etapas únicas
    stages = df['stage'].unique()
    if stages.size > 0:
        last_stage = stages[-1].tolist()
        return jsonify(last_stage)
    else:
        return jsonify(None)  # O algún valor por defecto

# get the matches for a given country, year and stage from matches.csv
@app.route('/api/matches/<int:country>/<int:year>/<int:stage>', methods=['GET'])
def get_matches_by_stage(country, year, stage):
    # Lee los archivos CSV
    matches_df = pd.read_csv('data/matches.csv')
    teams_df = pd.read_csv('data/teams.csv')
    
    # Agrega una columna 'id' basada en el índice del DataFrame
    matches_df['id'] = matches_df.index
    
    # Filtra los partidos por país, año y etapa
    filtered_matches = matches_df[
        (matches_df['country_id'] == country) & 
        (matches_df['year'] == year) & 
        (matches_df['stage'] == stage)
    ]
    
    # Selecciona solo las columnas de interés de matches.csv
    filtered_matches = filtered_matches[
        ['id', 'home_team_api_id', 'away_team_api_id', 'L_VAL_MEDIA_POR', 
         'L_VAL_MEDIA_DEF', 'L_VAL_MEDIA_MC', 'L_VAL_MEDIA_DEL', 
         'A_VAL_MEDIA_POR', 'A_VAL_MEDIA_DEF', 'A_VAL_MEDIA_MC', 'A_VAL_MEDIA_DEL', 'match_api_id']
    ]
    
    # Renombra la columna 'id' para evitar conflictos
    filtered_matches = filtered_matches.rename(columns={'id': 'match_id'})
    
    # Une la información del equipo local (home_team)
    merged_df = pd.merge(
        filtered_matches, 
        teams_df[['team_api_id', 'team_long_name', 'logourl', 'logourl1', 'logourl2']],
        left_on='home_team_api_id', 
        right_on='team_api_id', 
        suffixes=('', '_home')
    ).drop(columns='team_api_id')
    
    # Renombra las columnas del equipo local
    merged_df = merged_df.rename(columns={'team_long_name': 'home_team_name', 'logourl': 'home_team_logourl', 'logourl1': 'home_team_logourl1', 'logourl2': 'home_team_logourl2'})
    
    # Une la información del equipo visitante (away_team)
    merged_df = pd.merge(
        merged_df, 
        teams_df[['team_api_id', 'team_long_name', 'logourl', 'logourl1', 'logourl2']],
        left_on='away_team_api_id', 
        right_on='team_api_id', 
        suffixes=('', '_away')
    ).drop(columns='team_api_id')
    
    # Renombra las columnas del equipo visitante
    merged_df = merged_df.rename(columns={'team_long_name': 'away_team_name', 'logourl': 'away_team_logourl', 'logourl1': 'away_team_logourl1', 'logourl2': 'away_team_logourl2'})
    
    # Selecciona las columnas finales de interés
    final_columns = [
        'match_id', 'home_team_name', 'away_team_name', 'L_VAL_MEDIA_POR', 
        'L_VAL_MEDIA_DEF', 'L_VAL_MEDIA_MC', 'L_VAL_MEDIA_DEL', 
        'A_VAL_MEDIA_POR', 'A_VAL_MEDIA_DEF', 'A_VAL_MEDIA_MC', 'A_VAL_MEDIA_DEL',
        'home_team_logourl', 'home_team_logourl1', 'home_team_logourl2', 'away_team_logourl', 'away_team_logourl1', 'away_team_logourl2', 'match_api_id'
    ]
    
    result = merged_df[final_columns].replace([np.nan], [None]).to_dict(orient='records')
    
    return jsonify(result)


@app.route('/api/predict/<int:match_api_id>', methods=['GET'])
def predict_match(match_api_id):

    matches = pd.read_csv('data/matches_2015_normalized.csv')
    partido = matches[matches['match_api_id'] == match_api_id]
    partido = partido.drop(columns=['match_api_id'])
    X = partido.drop(columns=['RESULT'])
    y = partido['RESULT']
    new_model = tf.keras.models.load_model('model/modelo_ronda_75.keras')
    y_pred = new_model.predict(X)
    y_pred_rounded = [round(float(pred), 3) for pred in y_pred.flatten()]
    print(y)
    return jsonify(y_pred_rounded)

if __name__ == '__main__':
    app.run(debug=True)
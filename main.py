import requests 
import pandas as pd 
import sys 
from fpdf import FPDF
from bs4 import BeautifulSoup

#definimos todas las variables globales: 
team='GS'

urls = [ 'https://api.sportsdata.io/v3/nba/scores/json/Games/2023', 'https://api.sportsdata.io/v3/nba/scores/json/Stadiums',
'https://api.sportsdata.io/v3/nba/scores/json/TeamSeasonStats/2023',f'https://api.sportsdata.io/v3/nba/projections/json/PlayerSeasonProjectionStatsByTeam/2023/{team}',
f' https://api.sportsdata.io/v3/nba/scores/json/Players/{team}','https://api.sportsdata.io/v3/nba/scores/json/Standings/2023']

keys = ['schedules','stadiums','team season stats','player stats GS','players in GS','standings']

clave = 'c0e10232110a4a18b436f7219a4d51b3'

nombre_equipo = 'Golden State Warriors'

clave_equipo = 'GS'

head={'Ocp-Apim-Subscription-Key': clave}

#WEb scrapping prediccion: 

url ='https://www.sportytrader.es/pronosticos/baloncesto/usa/nba-306/'


def extract(urls,header,keys):
    
    dataframes=[]  # lista con todos los dataframes que cargaremos
    for i in range(0,len(urls)):
        response=requests.get(urls[i],headers=header)
        #print('\nCargando '+str(keys[i]))
        if i==0:
            df_schedules = pd.read_json(response.text)
            dataframes.append(df_schedules)
        elif i==1:
            df_stadiums= pd.read_json(response.text)
            dataframes.append(df_stadiums)
        elif i==2:
            df_teamstats=pd.read_json(response.text)       
            dataframes.append(df_teamstats)         
        elif i==3:
            df_playerstats= pd.read_json(response.text)
            dataframes.append(df_playerstats)
        elif i==4:
            df_players= pd.read_json(response.text)
            dataframes.append(df_players)
        elif i == 5: 
            df_standings= pd.read_json(response.text)
            dataframes.append(df_standings)
        # cargaremos los datos a un dataframe directamente 
        # teniendo en cuenta que lo que tenemos actualmente es un json
    
    return dataframes

def transform(dataframes):

    players=dataframes[4] # la informacion general
    stats=dataframes[3]  # para los datos de juego
    #lista con: player stats , players in GS, 
    'crear aqui la tabla '
    number_players=len(dataframes[4]['PlayerID'])
    ids = players['PlayerID']
    informacion_jugadores=[] 
    keys =['YahooName','Position','College','Games','Rebounds', 'Points','Steals','Assists']
    #son 3 de un df y 5 de otra 
    for i in range(15): 
        name= players['YahooName'][i]
        position= players['Position'][i]
        college= players['College'][i]
        games=str(stats['Games'][i])
        rebounds=str(stats['Rebounds'][i])
        points=str(stats['Points'][i])
        steals=str(stats['Steals'][i])
        assists=str(stats['Assists'][i])
        tupla_jugador=(name,position,college,games,rebounds,points,steals,assists)
        informacion_jugadores.append(tupla_jugador)

    return informacion_jugadores

def load(jugadores):

    'crear aqui un pdf'

    pdf = FPDF(orientation='P',unit='mm',format='A4')
    pdf.set_auto_page_break(auto = True, margin = 15) #pie de pagina 
    pdf.set_font('times','B', 18 )

    pdf.add_page()
    pdf.image('gswlogo.png',10,8,20)
    pdf.set_font('times','B',18)
    pdf.cell(0,10,'GSW season 2022/23', border=False , align='C')
    pdf.image('ciudad.jpg',50,70,50)
    pdf.image('nba.png',50,125,50)
    pdf.image('camiseta.png',100,70,50)
    pdf.image('stadium.jpg',100,125,50)

    pdf.add_page()
    pdf.set_font('Arial','',12)
    pdf.cell(w=0,h=15,txt='Golden State Warriors',border=1,ln=1,align='C',fill=0)
    pdf.cell(w=39,h=12,txt='Name',border=1,align='C',fill=0)
    pdf.cell(w=17,h=12,txt='Pos',border=1,align='C',fill=0)
    pdf.cell(w=32,h=12,txt='College',border=1,align='C',fill=0)
    pdf.cell(w=21,h=12,txt='N Games',border=1,align='C',fill=0)
    pdf.cell(w=23,h=12,txt='Rebounds',border=1,align='C',fill=0)
    pdf.cell(w=18,h=12,txt='Points',border=1,align='C',fill=0)
    pdf.cell(w=20,h=12,txt='Steals',border=1,align='C',fill=0)
    pdf.multi_cell(w=20,h=12,txt='Assists',border=1,align='C',fill=0)

    #Valores: 
    for valor in jugadores: 
        pdf.cell(w=39,h=12,txt=valor[0],border=1,align='C',fill=0)
        pdf.cell(w=17,h=12,txt=valor[1],border=1,align='C',fill=0)
        pdf.cell(w=32,h=12,txt=valor[2],border=1,align='C',fill=0)
        pdf.cell(w=21,h=12,txt=valor[3],border=1,align='C',fill=0)
        pdf.cell(w=23,h=12,txt=valor[4],border=1,align='C',fill=0)
        pdf.cell(w=18,h=12,txt=valor[5],border=1,align='C',fill=0)
        pdf.cell(w=20,h=12,txt=valor[6],border=1,align='C',fill=0)
        pdf.multi_cell(w=20,h=12,txt=valor[7],border=1,align='C',fill=0)

    pdf.output('gsw_22.pdf')

    return 


def extract_2():
    texto = requests.get(url).text
    return texto 

def transform_2(texto):
    soup = BeautifulSoup(texto, 'lxml')
    teams_games = soup.find_all("div" , {"class":"w-1/2 text-center break-word p-1 dark:text-white"} )
    #Equipos que tienen partidos hoy y del que vemos la poredicción: 
    teams_games_2=[]
    for element in teams_games: 
        element= element.text.strip() # limpiamos cada equipo para poder buscarlo mejor. 
        teams_games_2.append(element)
    ganador = soup.find_all("span" , {"class": "flex justify-center items-center h-7 w-6 rounded-md font-semibold bg-primary-green text-white mx-1"} ) 
    # Utilizamos el find_all ya que busca solo el primer elemento ganador, si es 1 gana el primer equipo y si no, el visitante 
    # Es decir, cada numero en ganador representa a un partido de 2 equipos. Por lo que len(teams_games) sera el doble que len(ganador) 
    ganador_2=[] #para datos limpios 
    for g in ganador: 
        g= g.text.strip()
        ganador_2.append(g)

    return teams_games_2, ganador_2

def load_2(teams,ganador):
    
    print('\nLas perdicciones para los partidos en el día de hoy son las siguientes:')
    cont=0
    for i in ganador:
        if i == '1': 
            equipo_g=teams[cont]
            equipo_p=teams[cont+1]
        else:
            equipo_g=teams[cont+1]
            equipo_p=teams[cont]
        cont+=2
        print(f'\n{equipo_g} ganará frente al equipo {equipo_p}')
    return 

def main(): 

    dataframes= extract(urls,head,keys)
    informacion_jugadores= transform(dataframes)
    load(informacion_jugadores)
    #print('\nFinalizando creacion de pdf')

    #Webscrapping con bs4: 
    html_texto= extract_2()
    h1,h2= transform_2(html_texto)
    load_2(h1,h2)
    print('\n Finalizando programa')
    sys.exit()

if __name__== '__main__': 
    main()
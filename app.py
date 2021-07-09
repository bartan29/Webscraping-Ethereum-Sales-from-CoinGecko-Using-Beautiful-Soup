from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.coingecko.com/en/coins/ethereum/historical_data/usd?start_date=2020-01-01&end_date=2021-06-30#panel')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('table', attrs={'class':"table table-striped text-sm text-lg-normal"})
row = table.find_all('th', attrs={'class':"font-semibold text-center"})

row_length = len(row)

temp = [] #initiating a list 

for i in range(1, row_length):

    #scrapping process
    
    #get date
    Periode = table.find_all('th', attrs={'class':"font-semibold text-center"})[i].text
    
    #get market cap
    Market_cap = table.find_all('td', attrs={'class':"text-center"})[i+(3*i)].text
    Market_cap = Market_cap.strip() #Menghilangkan kelebihan spasi
    
    #get volume
    Volume = table.find_all('td', attrs={'class':"text-center"})[i+1+(3*i)].text
    Volume = Volume.strip()
    
    #get open
    Open = table.find_all('td', attrs={'class':"text-center"})[i+2+(3*i)].text
    Open = Open.strip()
    
    #get close
    Close = table.find_all('td', attrs={'class':"text-center"})[i+3+(3*i)].text
    Close = Close.strip()
    
    temp.append((Periode, Market_cap, Volume, Open, Close))

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns = ('date','market_cap','volume','open','close'))

#insert data wrangling here
cols =['market_cap','volume','open','close']

#Melakukan pembersihan data dengan menghilangkan dollar sign pada kolom market_cap, volume, open dan close serta konversi menjadi float
df[cols] = df[cols].replace({'\$':''}, regex = True)
df[cols] = df[cols].replace({',':''}, regex = True)
df[cols] = df[cols].astype('float64')

#Melakukan konversi kolom date menjadi format tanggal
df['date'] = df['date'].astype('datetime64')

df = df.set_index('date')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df["volume"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = df['volume'].plot(figsize=(15,9))

	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)
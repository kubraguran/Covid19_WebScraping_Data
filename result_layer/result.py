import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt 
from transformation.connection import engine

def get_covid_data():
    return pd.read_sql('SELECT * FROM covid_data', con=engine)

df = get_covid_data()


#What are the top 10 highest total cases?
top10 = df.sort_values("TotalCases", ascending=False).head(10)[["Country","TotalCases"]].reset_index(drop=True)
print(top10)
sns.barplot(data = top10, x = 'TotalCases', y = 'Country', palette='Reds_r')
plt.title("Top 10 countries by Total Covid Cases")
plt.xlabel("Total Cases")
plt.ylabel("Country")
plt.tight_layout()
plt.show()
 

 #countries have the highest mortality rates (deaths / total cases)
df["check_number"] = df["TotalDeaths"] / df["TotalCases"]
highest_death = df.groupby("check_number")["Country"].sum().sort_values(ascending=False)





#Which continent has the highest average number of active cases per country?
country_ave = df.groupby(["Country", "Continent"])['ActiveCases'].mean().reset_index()
result = country_ave.groupby("Continent")["ActiveCases"].mean().sort_values(ascending=False)
print(result.index[0:3])


#How many countries have reported more than 1 million total cases?
more_than_mill = df.groupby("Country")["TotalCases"].sum() > 1000000
print(more_than_mill.sum())

#Which countries have more than 90% recovery rate?
df["RecoveryRate"] = df["TotalRecovered"] / df["TotalCases"]
step_1 = df[df["RecoveryRate"] > 0.9]
print(step_1.head(5))

sns.barplot(data=step_1.head(5), x="RecoveryRate", y="Country", palette="Greens_r")
plt.title("Countries with > 90% COVID-19 Recovery Rate")
plt.xlabel("Recovery Rate")
plt.ylabel("Country")
plt.tight_layout()
plt.show()

#Filter countries with more than 10 million total cases and return their count
more_than_10mil  = df.groupby("Country")["TotalCases"].sum() > 1000000
print(more_than_10mil.sum())






## Some SQL queries

#Which countries have the highest total deaths?
query = '''
    SELECT Country, TotalCases
    FROM covid_data
    ORDER BY TotalCases DESC
    LIMIT 10;
'''
df_top10 = pd.read_sql(query, con=engine)
print(df_top10)



#What are the top 5 countries by total tests conducted?

top_5 = ''' 
   SELECT Country, TotalTests
   FROM covid_data
   ORDER BY TotalTests DESC
   LIMIT 5
''' 
df_top5 = pd.read_sql(top_5, con = engine)
print(df_top5)

sns.barplot(data=df_top5, x="TotalTests", y="Country", palette="Blues")
plt.title("Top 5 Countries by Total COVID-19 Tests")
plt.xlabel("Total Tests")
plt.ylabel("Country")
plt.tight_layout()
plt.show()


#Which continent has the highest total number of active cases? 

highest_cases = ''' 
   select country from covid_data
   order by ActiveCases
   Limit 1
'''

df_highest = pd.read_sql(highest_cases, con = engine)
print(df_highest)





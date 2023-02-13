import mariadb
import pandas as pd
import plotly.io as pi
import plotly.graph_objects as go

# Open the Excel formatted file
import mariadb
df = pd.read_excel("C:\\Users\\rajes\\OneDrive\\Desktop\\Temperature_data.xlsx")

# Cleaning and translating the data
df1 = df.iloc[:, :10]

df1['ID'] = range(1, len(df) + 1)

df2 = df1.dropna().fillna(0)

df2['Datetime'] = df2['Date'].astype(str) + ' ' + df2['Time'].astype(str)

df3 = df2.drop_duplicates(subset='Datetime', keep='first', inplace=False)

columns_order = ['ID', 'Date', 'Time', 'Datetime', '1035', '1045', '1055', '1065', '1075', '1085', '1095', '1105']
df4 = df3.reindex(columns=columns_order)

print(df4)


# Establish a Mariadb connection
database = mariadb.connect(
            user="root",
            password="12345",
            host="127.0.0.1",
            port=3307,
            database="database")

# Get the cursor, which is used to traverse the database, line by line
cursor = database.cursor()

# Dropping the table if exists
cursor.execute('DROP TABLE IF EXISTS table_name')

# creating a new table
cursor.execute("create table table_name(ID INT PRIMARY KEY NOT NULL, Date VARCHAR(255) NULL, Time VARCHAR(255) NULL,"
               "Datetime VARCHAR(255) NULL, `1035` DECIMAL(5,1) NULL,`1045` DECIMAL(5,1) NULL,"
               "`1055` DECIMAL(5,1) NULL,`1065` DECIMAL(5,1) NULL,`1075` DECIMAL(5,1) NULL,"
               "`1085` DECIMAL(5,1) NULL,`1095` DECIMAL(5,1) NULL,`1105` DECIMAL(5,1) NULL)")

# Create a For loop to iterate through each row in the file
for i, row in df4.iterrows():
    mariadb = "INSERT INTO table_name VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(mariadb, tuple(row))

# Execute Mariadb Query
cursor.execute("SELECT * FROM table_name")
rows = cursor.fetchall()
data = pd.DataFrame(rows, columns=['ID', 'Date', 'Time', 'Datetime', '1035', '1045', '1055', '1065', '1075',
                                   '1085', '1095', '1105'])
print(data)

# creating a graph

fig = go.Figure()
fig.add_trace(go.Scatter(x=data['ID'], y=data['1035'], name='Tiefe 3,5m', mode="lines"))
fig.add_trace(go.Scatter(x=data['ID'], y=data['1045'], name='Tiefe 4,5m', mode="lines"))
fig.add_trace(go.Scatter(x=data['ID'], y=data['1055'], name='Tiefe 5,5m', mode="lines"))
fig.add_trace(go.Scatter(x=data['ID'], y=data['1065'], name='Tiefe 6,5m', mode="lines"))
fig.add_trace(go.Scatter(x=data['ID'], y=data['1075'], name='Tiefe 7,5m', mode="lines"))
fig.add_trace(go.Scatter(x=data['ID'], y=data['1085'], name='Tiefe 8,5m', mode="lines"))
fig.add_trace(go.Scatter(x=data['ID'], y=data['1095'], name='Tiefe 9,5m', mode="lines"))
fig.add_trace(go.Scatter(x=data['ID'], y=data['1105'], name='Tiefe 10,5m', mode="lines"))

fig.update_layout(
    xaxis=dict(title='Betriebstage[d]', type='linear',
               showline=True, linecolor='black', linewidth=2,
               zerolinewidth=2, tickangle=0, tick0=1, gridwidth=2, tickfont=dict(size=10)),
    yaxis=dict(title='Temperature[°C]',
               showline=True, linecolor='black', linewidth=2,
               zerolinewidth=2),
    legend=dict(orientation="h", y=-0.3, yanchor="bottom"))

fig.show()

# Commit the transaction
database.commit()

# Close the cursor
cursor.close()

# Close the database connection
database.close()

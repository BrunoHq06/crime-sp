import streamlit as st
import pandas as pd
import plotly.express as px

#Ler as bases e realizar gerar bases para os plots

#Base principal
df = pd.read_excel('Data.xlsx')

#Gerar df para fazer o line plot de ocorrencias por mês
df_ocorrencia = df.groupby('Ocorrencia').sum().iloc[:,3:].reset_index()
lista_ocorrencia = df_ocorrencia['Ocorrencia'].unique() #lista para fazer menu de filtro

#melt = transformar as colunas em linhas
types_melt = pd.melt(df_ocorrencia,'Ocorrencia',var_name='Month',value_name='Value')
#filtrar para retirar o total  da view, visto que não precisamos plotar nesse grafico
types_melt = types_melt[types_melt['Month'] != 'Total']

#df para gerar o mapa
mapa_df = df.groupby(['City','Long','Lat']).sum()['Total'].reset_index()
mapa_df = mapa_df.sort_values('Total',ascending=True)



#Streamlit


st.markdown("<h1 style='text-align: center; color: black;'>WEB-APP | CRIMES EM 2021</h1>", unsafe_allow_html=True)

st.header("Ocorrencia")

#instanciar o selectbox
types = st.selectbox("Escolha a ocorrencia:",lista_ocorrencia)

#plots
line = px.line(types_melt[types_melt['Ocorrencia'] == types],x='Month',y='Value',text='Value', title="Evolução da Ocorrêcia por mês" ,labels={
                     "Month": "Mês",
                     "Value": "Qtd"
                 },)
line.update_xaxes(showgrid=False)
line.update_yaxes(showgrid=False)
line.update_traces(textposition="top center")
line.update_layout(title_x=0.5)

st.plotly_chart(line)


#Linha do mapa

map = px.scatter_mapbox(mapa_df, lat="Lat", lon="Long",size='Total',hover_name="City",zoom=5,color="Total", color_continuous_scale=px.colors.sequential.Hot[::-1])
map.update_layout(mapbox_style="open-street-map")

st.write("Mapa")

st.plotly_chart(map)

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='whitegrid')

# Load the dataset
df_day = pd.read_csv('day.csv')
df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_day['year'] = df_day['dteday'].dt.year

# Sidebar settings
st.header('Analisis Dataset Bike Sharing :sparkles:')
st.sidebar.image("https://storage.googleapis.com/kaggle-datasets-images/3556223/6194875/c51f57d9f027c00fc8d573060eef197b/dataset-cover.jpeg", width=300)
min_date = df_day['dteday'].min().date()
max_date = df_day['dteday'].max().date()

# Date range filter
start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Convert date objects to datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filtering data based on selected date range
filtered_data = df_day[(df_day['dteday'] >= start_date) & (df_day['dteday'] <= end_date)]

# Calculate today's count and yesterday's count
todays_cnt = int(filtered_data['cnt'].iloc[-1])
yesterdays_cnt = int(filtered_data['cnt'].iloc[-2])

# Display the metric in the sidebar with thousand separators
st.sidebar.metric(
    label="Pertumbuhan harian pengguna",
    value=todays_cnt,
    delta=yesterdays_cnt
)


# Daily User
daily_users_data = filtered_data.groupby('dteday').agg({
    'casual': 'sum',
    'registered': 'sum',
    'cnt': 'sum'
}).reset_index()

st.subheader('Total Users')

col1, col2, col3 = st.columns(3)

def format_number(number):
    return f"{number:,}"

with col1:
    total_casual = daily_users_data.casual.sum()
    st.metric("Total Casual Users", value=format_number(total_casual))

with col2:
    total_registered = daily_users_data.registered.sum()
    st.metric("Total Registered Users", value=format_number(total_registered))

with col3:
    total_cnt = daily_users_data.cnt.sum()
    st.metric("Total Users", value=format_number(total_cnt))


# PLOT 1
user_counts_data = df_day[['casual', 'registered']].sum()

# Plotting pie plot
fig_pie, ax_pie = plt.subplots()
ax_pie.pie(user_counts_data, labels=user_counts_data.index, autopct='%2.1f%%', startangle=90, colors=['#FFA07A', '#90CAF9'])
ax_pie.axis('equal')
ax_pie.set_title("Persentase Pengguna (Casual vs Registered)")

# Display the plot in Streamlit
st.pyplot(fig_pie)


#PLOT 2
st.subheader('Daily Users')
# set figure size
fig_fh3, ax_fh3 = plt.subplots(figsize=(16, 8))
# Plotting
sns.lineplot(x='dteday', y='casual', data=daily_users_data, ax=ax_fh3, label='Casual', marker='o', color="#FFA07A")
sns.lineplot(x='dteday', y='registered', data=daily_users_data, ax=ax_fh3, label='Registered', marker='o', color="#90CAF9")
ax_fh3.set_ylabel("User Counts")
ax_fh3.set_xlabel("Order Date")
ax_fh3.set_title("Casual and Registered Users Counts per Day")
ax_fh3.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better readability
ax_fh3.legend(["Casual", "Registered"])

# Display the plot in Streamlit
st.pyplot(fig_fh3)


#PLOT 3

st.subheader('Users vs Temperature')

# Map numeric season values to labels
season_mapping = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Autumn'}
filtered_data['season'] = filtered_data['season'].map(season_mapping)

# Aggregated data
season_data = filtered_data.groupby('season').agg({
    'registered': 'sum',
    'casual': 'sum'
}).reset_index()

# Aggregated data for plotting
plot_data = filtered_data.groupby(['temp', 'atemp']).agg({
    'cnt': 'sum'
}).reset_index()

# Plotting
#subplot 1
fig, ax = plt.subplots()
sns.regplot(x='cnt', y='temp', data=plot_data, ax=ax, label='temp', color="#FFA07A", line_kws={'color': 'red'})
ax.set_ylabel("User Counts")
ax.set_xlabel("Temperature")
ax.set_title("Total Pengguna vs Temperature")
ax.legend()

#subplot 2
fig2, ax = plt.subplots()
sns.regplot(x='cnt', y='atemp', data=plot_data, ax=ax, label='atemp', color="#90CAF9", line_kws={'color': 'red'})
ax.set_ylabel("User Counts")
ax.set_xlabel("Temperature")
ax.set_title("Total Pengguna vs ATemperature")
ax.legend()

# Display the plot in Streamlit
col1, col2 = st.columns(2)
with col1:
    st.pyplot(fig)

with col2:
    st.pyplot(fig2)

# Expander for additional information
with st.expander("Informasi Tambahan"):
    st.write("""
    Secara umum, semakin tinggi temperatur udara (temp dan atemp), maka semakin banyak pengguna Bike Sharing.\n
    Ket:\n
    - **casual**: jumlah pengguna casual
    - **registered**: jumlah pengguna terdaftar
    - **temp**: suhu normal dalam Celsius. Nilai-nilai ini diperoleh melalui (t-t_min)/(t_max-t_min), t_min=-8, t_max=+39 (hanya dalam skala per jam)
    - **atemp**: suhu rasa normal dalam Celsius. Nilai-nilai ini diperoleh melalui (t-t_min)/(t_max-t_min), t_min=-16, t_max=+50 (hanya dalam skala per jam)
    """)


#PLOTTING 4

st.subheader('Users vs Season')

fig_fh1, ax_fh1 = plt.subplots()
sns.barplot(x='season', y='registered', data=season_data, ax=ax_fh1, label='Registered', color="#90CAF9")
sns.barplot(x='season', y='casual', data=season_data, ax=ax_fh1, label='Casual', color="#FFA07A")
ax_fh1.set_ylabel("Count")
ax_fh1.set_title(f"Pengguna Casual dan Registered Berdasarkan Musim")
ax_fh1.legend()

# Display the plot in Streamlit
st.pyplot(fig_fh1)


#PLOTTING 5

st.subheader('Users vs Weather')

season_data= df_day.groupby('weathersit').agg({
    'casual':'sum',
    'registered':'sum'
}).reset_index()
fig_fh1, ax_fh1 = plt.subplots()
sns.barplot(x='weathersit', y='registered', data=season_data, ax=ax_fh1, label='Registered', color="#90CAF9")
sns.barplot(x='weathersit', y='casual', data=season_data, ax=ax_fh1, label='Casual', color="#FFA07A")
ax_fh1.set_ylabel("Count")
ax_fh1.set_title(f"Pengguna Casual dan Registered Berdasarkan Musim")
ax_fh1.legend()

# Display the plot in Streamlit
st.pyplot(fig_fh1)

with st.expander("Informasi Tambahan"):
    st.write("""
    Secara umum, semakin baik cuacanya, semakin banyak pula pengguna Bike Sharing dengan 1 cuaca paling baik dan 3 cuaca paling buruk.\n
    Ket:\n
    - **1**: Clear, Few clouds, Partly cloudy, Partly cloudy
    - **2**:  Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
    - **3**: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
    """)


# PLOTTING 6

st.subheader('Users vs Hour')

# PLOTTING 6
# Hourly user counts
hourly_users_data = filtered_data.groupby(filtered_data['dteday'].dt.hour).agg({
    'casual': 'sum',
    'registered': 'sum',
    'cnt': 'sum'
}).reset_index()

# Plotting
fig_fh2, ax_fh2 = plt.subplots(figsize=(12, 6))
sns.barplot(x='dteday', y='cnt', data=hourly_users_data, ax=ax_fh2, color="#90CAF9")
ax_fh2.set_ylabel("Total Pengguna")
ax_fh2.set_xlabel("Jam")
ax_fh2.set_title("Total Pengguna Per Jam dalam Sehari")
ax_fh2.set_xticklabels(hourly_users_data['dteday'])
ax_fh2.tick_params(axis='x', rotation=45)

# Display the plot in Streamlit
st.pyplot(fig_fh2)


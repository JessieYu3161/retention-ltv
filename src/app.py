#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from datetime import date
import dash
from dash import dcc
from dash import html
from dash import dash_table
from jupyter_dash import JupyterDash
import dash.dependencies


# In[2]:


shopify_data = pd.read_csv('https://raw.githubusercontent.com/JessieYu3161/retention-ltv/main/src/shopify_df.csv')
# exclude emails contain 'ever-eden.com'
shopify_data = shopify_data[shopify_data['customer_email'].str.contains('ever-eden.com') == False]
############# note: Shopify Gross sales = net sales + discount + returns
# define sales = gross sales - returns
shopify_data['sales'] = shopify_data['gross_sales'] + shopify_data['returns']
shopify_data = shopify_data[(shopify_data['orders'] > 0) & (shopify_data['sales'] > 0)]
shopify_data['product_title'] = shopify_data['product_title'].astype(str)
shopify_data = shopify_data[['day', 'customer_id', 'customer_type', 'sales', 'product_title']]

# remove un-necessary product titles
remove_product = ['Copy of Soothing Baby Massage Oil', 'Exclusive Beauty Bag', 'Exclusive Spring Tote Bag',
                 'Full-Size Golden Body Serum','Full-Size Multi-Purpose Healing Balm','Full-Size Sheer Botanical Facial Sunscreen SPF30',
                 'Full-Size Soothing Diaper Rash Cream','Golden Belly Serum Sample','Golden Body Serum Sample (2.5ml)','Kids Body Lotion Cool Peach Sample',
                 'Kids Face Cream Melon Juice Sample','Luxe Silk Sleep Mask','Nourishing Baby Face Cream Sample','Nourishing Baby Massage Oil Sample',
                 'Nourishing Stretch Mark Cream Sample','Rush Shipping','Vegan Leather Beauty Bag','WELCOME10 Discount Removed',
                 'WIP Test - Baby Moisturizing Lotion','WIP Test - Jet Set Baby Core Collection','WIP Test - Lifting and Firming Lotion',
                 'WIP Test - NEW LOOK Soothing Baby Massage Oil','WIP Test - Nourishing Stretch Mark Cream','WIP Test - Premium Mineral Sunscreen SPF 30',
                 'Old - Baby Shampoo and Body Wash','Old - Lifting and Firming Lotion','Old - Multi-Purpose Healing Balm',
                 'Old - Nourishing Stretch Mark Cream','Old - Outdoors Essentials','Old - Premium Mineral Sunscreen SPF 30',
                 'Old - Soothing Baby Massage Oil','Old - Soothing Belly Mask']
shopify_data = shopify_data[~shopify_data['product_title'].isin(remove_product)]

# edit to universal product title
shopify_data.loc[shopify_data['product_title'] == 'Baby  Lip Balm', 'product_title'] = 'Baby Lip Balm'
shopify_data.loc[shopify_data['product_title'] == 'Lip Balm', 'product_title'] = 'Baby Lip Balm'
shopify_data.loc[shopify_data['product_title'] == 'Nourishing Lip Balm', 'product_title'] = 'Baby Lip Balm'

shopify_data.loc[shopify_data['product_title'] == 'Baby Moisturizing Lotion Fragrance Free', 'product_title'] = 'Baby Moisturizing Lotion'
shopify_data.loc[shopify_data['product_title'] == 'Baby Moisturizing Lotion Light Cucumber', 'product_title'] = 'Baby Moisturizing Lotion'
shopify_data.loc[shopify_data['product_title'] == 'Baby Moisturizing Lotion Light Jasmine', 'product_title'] = 'Baby Moisturizing Lotion'

shopify_data.loc[shopify_data['product_title'] == 'Baby Moisturizing Lotion Deluxe Mini', 'product_title'] = 'Baby Moisturizing Lotion Mini'
shopify_data.loc[shopify_data['product_title'] == 'Baby Moisturizing Lotion Fragrance Free - Mini', 'product_title'] = 'Baby Moisturizing Lotion Mini'
shopify_data.loc[shopify_data['product_title'] == 'Mini Fragrance-Free Baby Lotion', 'product_title'] = 'Baby Moisturizing Lotion Mini'

shopify_data.loc[shopify_data['product_title'] == 'Baby Shampoo and Body Wash Deluxe Mini', 'product_title'] = 'Baby Shampoo and Body Wash - Mini'
shopify_data.loc[shopify_data['product_title'] == 'GBOS + GBS', 'product_title'] = 'Belly Serum Experience Set'

shopify_data.loc[shopify_data['product_title'] == 'Cleanse and Nourish Routine Bundle', 'product_title'] = 'Cleanse and Nourish Bundle'

shopify_data.loc[shopify_data['product_title'] == 'Complete Baby Care Gift Set', 'product_title'] = 'Complete Baby Gift Bundle'

shopify_data.loc[shopify_data['product_title'] == 'Golden Belly Serum - Mini', 'product_title'] = 'Golden Belly Serum Mini'

shopify_data.loc[shopify_data['product_title'] == 'Kids Daily 1-2-3 Routine Set', 'product_title'] = 'Kids Daily 1-2-3 Routine'

shopify_data.loc[shopify_data['product_title'] == 'Kids Happy Face Duo Set', 'product_title'] = 'Kids Happy Face Duo'

shopify_data.loc[shopify_data['product_title'] == 'Kids Multi-Vitamin Body Lotion Cool Peach', 'product_title'] = 'Kids Multi-Vitamin Body Lotion'
shopify_data.loc[shopify_data['product_title'] == 'Kids Multi-Vitamin Body Lotion Fresh Pomelo', 'product_title'] = 'Kids Multi-Vitamin Body Lotion'
shopify_data.loc[shopify_data['product_title'] == 'Kids Multi-Vitamin Body Lotion Melon', 'product_title'] = 'Kids Multi-Vitamin Body Lotion'
shopify_data.loc[shopify_data['product_title'] == 'Kids Multi-Vitamin Body Lotion Melon Juice', 'product_title'] = 'Kids Multi-Vitamin Body Lotion'

shopify_data.loc[shopify_data['product_title'] == 'Kids Multi-Vitamin Body Wash Cool Peach', 'product_title'] = 'Kids Multi-Vitamin Body Wash'
shopify_data.loc[shopify_data['product_title'] == 'Kids Multi-Vitamin Body Wash Fresh Pomelo', 'product_title'] = 'Kids Multi-Vitamin Body Wash'
shopify_data.loc[shopify_data['product_title'] == 'Kids Multi-Vitamin Body Wash Melon Juice', 'product_title'] = 'Kids Multi-Vitamin Body Wash'

shopify_data.loc[shopify_data['product_title'] == 'Kids Multi-Vitamin Face Cream Cool Peach', 'product_title'] = 'Kids Multi-Vitamin Face Cream'
shopify_data.loc[shopify_data['product_title'] == 'Kids Multi-Vitamin Face Cream Fresh Pomelo', 'product_title'] = 'Kids Multi-Vitamin Face Cream'
shopify_data.loc[shopify_data['product_title'] == 'Kids Multi-Vitamin Face Cream Melon Juice', 'product_title'] = 'Kids Multi-Vitamin Face Cream'

shopify_data.loc[shopify_data['product_title'] == 'Kids Multi-Vitamin Face Cream Cool Peach Mini', 'product_title'] = 'Kids Multi-Vitamin Face Cream Mini'
shopify_data.loc[shopify_data['product_title'] == 'Mini Kids Multi-Vitamin Face Cream Melon Juice', 'product_title'] = 'Kids Multi-Vitamin Face Cream Mini'
shopify_data.loc[shopify_data['product_title'] == 'Kids Multi-Vitamin Face Cream Melon Juice - Mini', 'product_title'] = 'Kids Multi-Vitamin Face Cream Mini'

shopify_data.loc[shopify_data['product_title'] == 'Kids Multi-Vitamin Face Wash Cool Peach', 'product_title'] = 'Kids Multi-Vitamin Face Wash'
shopify_data.loc[shopify_data['product_title'] == 'Kids Multi-Vitamin Face Wash Fresh Pomelo', 'product_title'] = 'Kids Multi-Vitamin Face Wash'
shopify_data.loc[shopify_data['product_title'] == 'Kids Multi-Vitamin Face Wash Melon Juice', 'product_title'] = 'Kids Multi-Vitamin Face Wash'

shopify_data.loc[shopify_data['product_title'] == 'Kids Multi-Vitamin Face Wash Peach - Mini', 'product_title'] = 'Kids Multi-Vitamin Face Wash Mini'
shopify_data.loc[shopify_data['product_title'] == 'Mini Kids Multi-Vitamin Face Wash', 'product_title'] = 'Kids Multi-Vitamin Face Wash Mini'
shopify_data.loc[shopify_data['product_title'] == 'Mini Kids Multi-Vitamin Face Wash Melon', 'product_title'] = 'Kids Multi-Vitamin Face Wash Mini'
shopify_data.loc[shopify_data['product_title'] == 'Mini Kids Multi-Vitamin Face Wash Peach', 'product_title'] = 'Kids Multi-Vitamin Face Wash Mini'

shopify_data.loc[shopify_data['product_title'] == 'Kids Multi-Vitamin Shampoo & Conditioner Cool Peach', 'product_title'] = 'Kids Multi-Vitamin Shampoo & Conditioner'
shopify_data.loc[shopify_data['product_title'] == 'Kids Multi-Vitamin Shampoo & Conditioner Fresh Pomelo', 'product_title'] = 'Kids Multi-Vitamin Shampoo & Conditioner'
shopify_data.loc[shopify_data['product_title'] == 'Kids Multi-Vitamin Shampoo & Conditioner Melon Juice', 'product_title'] = 'Kids Multi-Vitamin Shampoo & Conditioner'

shopify_data.loc[shopify_data['product_title'] == 'Luxury Vegan Leather Gift Bag', 'product_title'] = 'Luxe Vegan Leather Gift Bag'

shopify_data.loc[shopify_data['product_title'] == 'Nourishing Baby Face Cream Cotton Dew', 'product_title'] = 'Nourishing Baby Face Cream'
shopify_data.loc[shopify_data['product_title'] == 'Nourishing Baby Face Cream Tea Meadow', 'product_title'] = 'Nourishing Baby Face Cream'

shopify_data.loc[shopify_data['product_title'] == 'Mini Nourishing Baby Face Cream', 'product_title'] = 'Nourishing Baby Face Cream - Mini'
shopify_data.loc[shopify_data['product_title'] == 'Nourishing Baby Face Cream Mini', 'product_title'] = 'Nourishing Baby Face Cream - Mini'
shopify_data.loc[shopify_data['product_title'] == 'Nourishing Baby Face Cream Mini 10 ml', 'product_title'] = 'Nourishing Baby Face Cream - Mini'

shopify_data.loc[shopify_data['product_title'] == 'Nourishing Stretch Mark Cream - Mini', 'product_title'] = 'Nourishing Stretch Mark Cream Mini'

shopify_data.loc[shopify_data['product_title'] == 'Pencil case', 'product_title'] = 'Pencil case & Puffy stickers'
shopify_data.loc[shopify_data['product_title'] == 'Puffy Stickers', 'product_title'] = 'Pencil case & Puffy stickers'
shopify_data.loc[shopify_data['product_title'] == 'Pencil case & puffy stickers Set', 'product_title'] = 'Pencil case & Puffy stickers'

shopify_data.loc[shopify_data['product_title'] == 'Petit Bouquet Postpartum Belly Serum', 'product_title'] = 'Petit Bouquet Belly Serum'

shopify_data.loc[shopify_data['product_title'] == 'Premium Mineral Sunscreen SPF 30', 'product_title'] = 'Premium Mineral Sunscreen SPF30'
shopify_data.loc[shopify_data['product_title'] == 'Protecting Baby Face Cream - No 2. Silk Cream', 'product_title'] = 'Protecting Baby Face Cream'
shopify_data.loc[shopify_data['product_title'] == 'Scented Bubble Trio', 'product_title'] = 'Scented Bubble Bundle'

shopify_data.loc[shopify_data['product_title'] == 'Soothing Baby Massage Oil  Cotton Dew', 'product_title'] = 'Soothing Baby Massage Oil'
shopify_data.loc[shopify_data['product_title'] == 'Soothing Baby Massage Oil  Warm Blossom', 'product_title'] = 'Soothing Baby Massage Oil'
shopify_data.loc[shopify_data['product_title'] == 'Soothing Baby Massage Oil Cotton Dew', 'product_title'] = 'Soothing Baby Massage Oil'
shopify_data.loc[shopify_data['product_title'] == 'Soothing Baby Massage Oil Morning Breeze', 'product_title'] = 'Soothing Baby Massage Oil'
shopify_data.loc[shopify_data['product_title'] == 'Soothing Baby Massage Oil Warm Blossom', 'product_title'] = 'Soothing Baby Massage Oil'
shopify_data.loc[shopify_data['product_title'] == 'Baby Massage Oil', 'product_title'] = 'Soothing Baby Massage Oil'

shopify_data.loc[shopify_data['product_title'] == 'Soothing Baby Massage Oil Deluxe Mini', 'product_title'] = 'Soothing Baby Massage Oil - Mini'

shopify_data.loc[shopify_data['product_title'] == 'Soothing Belly Mask - 4 Sheets', 'product_title'] = 'Soothing Belly Mask'
shopify_data.loc[shopify_data['product_title'] == 'Soothing Belly Mask 1-sheet', 'product_title'] = 'Soothing Belly Mask'
shopify_data.loc[shopify_data['product_title'] == 'Soothing Belly Mask Collection', 'product_title'] = 'Soothing Belly Mask'

shopify_data.loc[shopify_data['product_title'] == 'Special Delivery Discovery Set', 'product_title'] = 'Special Delivery Discovery Kit'

shopify_data.loc[shopify_data['product_title'] == 'SPF 50 Super-Sheer Premium Mineral Sunscreen', 'product_title'] = 'SPF 50 Premium Mineral Sunscreen'

shopify_data.loc[shopify_data['product_title'] == 'Jumbo-Sized Soothing Baby Massage Oil', 'product_title'] = 'Jumbo Soothing Baby Massage Oil'


# In[3]:


def purchase_rate(customer_id, day):
    purchase_rate = [1]
    for i in range(1, len(customer_id)):
        if customer_id[i] == customer_id[i - 1]:
            if day[i] == day[i - 1]:
                purchase_rate.append(purchase_rate[-1])
            else:
                purchase_rate.append(purchase_rate[-1] + 1)
        else:
            purchase_rate.append(1)
    return purchase_rate
def join_date(date, purchase_rate):
    join_date = list(range(len(date)))
    for i in range(len(purchase_rate)): 
          if purchase_rate[i] == 1:
                 join_date[i] = date[i]
          else:
                 join_date[i] = join_date[i-1]
    return join_date
def age_by_month(purchase_rate, month, year, join_month, join_year):
    age_by_month = list(range(len(year)))
    for i in range(len(purchase_rate)):
          if purchase_rate[i] == 1:
              age_by_month[i] = 0
          else:
              if year[i] == join_year[i]:
                 age_by_month[i] = month[i] - join_month[i]
              else:
                 age_by_month[i] = month[i] - join_month[i] + 12*(year[i]-join_year[i])
    return age_by_month


# In[4]:


first_time = shopify_data.loc[shopify_data['customer_type'] == 'First-time',]
final = shopify_data.loc[shopify_data['customer_id'].isin(first_time['customer_id'].values)]
final = final.drop(columns=['customer_type'])
final['day'] = pd.to_datetime(final['day'], dayfirst=True)
final = final.sort_values(['customer_id', 'day'])
final.reset_index(inplace=True, drop=True)

final['month'] = pd.to_datetime(final['day']).dt.month
final['Purchase Rate'] = purchase_rate(final['customer_id'], final['day'])
final['Join Date'] = join_date(final['day'], final['Purchase Rate'])
final['Join Date'] = pd.to_datetime(final['Join Date'], dayfirst=True)
final['cohort'] = pd.to_datetime(final['Join Date']).dt.strftime('%Y-%m')
final['year'] = pd.to_datetime(final['day']).dt.year
final['Join Date Month'] = pd.to_datetime(final['Join Date']).dt.month
final['Join Date Year'] = pd.to_datetime(final['Join Date']).dt.year
final['Age by month'] = age_by_month(final['Purchase Rate'], final['month'], final['year'], final['Join Date Month'], final['Join Date Year'])


# # Retention - in Absolute number by cohort

# In[5]:


cohorts = final.groupby(['cohort', 'Age by month']).nunique()
cohorts = cohorts.customer_id.to_frame().reset_index()   # convert series to frame
cohorts = pd.pivot_table(cohorts, values='customer_id', index='cohort', columns='Age by month')
retention_absolute = cohorts.replace(np.nan, '', regex=True)


# # Retention - in Absolute percentage by cohort

# In[6]:


for i in range(len(cohorts.columns)-1):
    cohorts[i+1] = cohorts[i+1] / cohorts[0]
    cohorts[i+1] = cohorts[i+1].map('{:.2%}'.format)
cohorts[0] = cohorts[0]

retention_percentage = cohorts.replace('nan%', '', regex=True)


# # Retention - in Cumulative number by cohort

# In[7]:


# Create a new table with cumulative sum of each row data from the previous data
retention_cumulative = retention_absolute.apply(pd.to_numeric, errors='coerce').copy()
for i in range(2, retention_cumulative.shape[1]):
    retention_cumulative.iloc[:, i] = retention_cumulative.iloc[:, i].add(retention_cumulative.iloc[:, i-1], fill_value=0)   


# # Retention - in Cumulative percentage by cohort

# In[8]:


retention_cum_percentage = retention_cumulative.copy()
for i in range(len(retention_cum_percentage.columns)-1):
    retention_cum_percentage[i+1] = retention_cum_percentage[i+1] / retention_cum_percentage[0]
    retention_cum_percentage[i+1] = retention_cum_percentage[i+1].map('{:.2%}'.format)
retention_cum_percentage[0] = retention_cum_percentage[0]


# # Retention - in Cumulative number by cohort [Unique Customers]
final_unique = final[final['Purchase Rate'] == 2]
final_unique_cohorts = final_unique.groupby(['cohort', 'Age by month']).nunique()
final_unique_cohorts = final_unique_cohorts.customer_id.to_frame().reset_index()
final_unique_cohorts = pd.pivot_table(final_unique_cohorts, values='customer_id', index='cohort', columns='Age by month')

unique_retention_absolute = final_unique_cohorts.replace(np.nan, '', regex=True)
unique_retention_absolute['New Customer'] = final.groupby(['cohort']).nunique().customer_id.to_frame().reset_index()['customer_id'].values
first_column = unique_retention_absolute.pop('New Customer')
unique_retention_absolute.insert(0, 'New Customer', first_column)
unique_retention_absolute['New Customer'] = unique_retention_absolute['New Customer'].astype(float)
unique_retention_absolute[0] = unique_retention_absolute[0].astype(str)
unique_retention_absolute = unique_retention_absolute.apply(pd.to_numeric, errors='coerce')
unique_retention_absolute = unique_retention_absolute.replace(np.nan, 0, regex=True)


column_index = unique_retention_absolute.columns.get_loc(25)
unique_retention_absolute = unique_retention_absolute.iloc[:, :column_index]
unique_retention_absolute

retention_cumulative_unique = unique_retention_absolute.apply(pd.to_numeric, errors='coerce').copy()
for i in range(2, retention_cumulative_unique.shape[1]):
    retention_cumulative_unique.iloc[:, i] = retention_cumulative_unique.iloc[:, i].add(retention_cumulative_unique.iloc[:, i-1], fill_value=0)


# # Retention - in Cumulative percentage by cohort [Unique Customers]

retention_cum_percentage_unique = retention_cumulative_unique.copy()
for i in range(-1,len(retention_cum_percentage_unique.columns)-2):
    retention_cum_percentage_unique[i+1] = retention_cum_percentage_unique[i+1] / retention_cum_percentage_unique['New Customer']
    retention_cum_percentage_unique[i+1] = retention_cum_percentage_unique[i+1].map('{:.2%}'.format)
retention_cum_percentage_unique['New Customer'] = retention_cum_percentage_unique['New Customer']


# # LTV by cohort

# In[9]:


ltv_data = final.copy()
ltv_data = ltv_data.groupby(['cohort', 'Age by month'])['sales'].sum().to_frame().reset_index()
ltv_data['cum_sum'] = ltv_data.groupby('cohort')['sales'].cumsum()
ltv_data['num_customer'] = final.groupby(['cohort', 'Age by month']).nunique().reset_index()['customer_id']

def assign_value(ltv_data):
    if ltv_data['Age by month'] == 0:
        return ltv_data['num_customer']
    elif ltv_data['Age by month'] != 0:
        return np.nan

ltv_data['monthly_new_customers'] = ltv_data.apply(assign_value, axis=1)
ltv_data['monthly_new_customers'] = ltv_data['monthly_new_customers'].fillna(method='ffill')
ltv_data['avg_LTV'] = ltv_data['cum_sum'] / ltv_data['monthly_new_customers']
ltv_data['avg_LTV'] = ltv_data['avg_LTV'].round(2)

ltv_cohorts = pd.pivot_table(ltv_data, values='avg_LTV', index='cohort', columns='Age by month')
ltv_cohorts = ltv_cohorts.replace(np.nan, '', regex=True)
ltv_cohorts['New Customer Acquired'] = cohorts[cohorts.columns[0]].values
first_column = ltv_cohorts.pop('New Customer Acquired')
ltv_cohorts.insert(0, 'New Customer Acquired', first_column)


# # Dash LayOut

# In[10]:


# Get unique product names and scents from the dataframe
product_names = shopify_data['product_title'].unique()
max_date = date.today().strftime("%Y-%m-%d")

# Create the JupyterDash app
app = JupyterDash(__name__)
server = app.server

# Define the layout
login_layout = html.Div(
    id = "login-container",
    children=[
        html.H2("Login Page"),
        html.Div(
            children=[
                html.Label("Username"),
                dcc.Input(id="username-input", type="text", placeholder="Enter your username"),
                html.Label("Password"),
                dcc.Input(id="password-input", type="password", placeholder="Enter your password"),
                html.Button("Login", id="login-button", n_clicks=0),
                html.Div(id="output-message")
            ],
            style={"width": "300px", "margin": "auto", "margin-top": "50px"}
        )
    ]
)


dashboard_layout = html.Div(
    id = "dashboard-container",
    children=[
        html.H1("Shopify Customer Retention and LTV Dashboard"),
        dcc.Tabs(id='tabs', value='cohort-tab', children=[
            dcc.Tab(label='Retention Cohort Analysis', value='cohort-tab'),
            dcc.Tab(label='Customer Lifetime Value', value='ltv-tab'),
            dcc.Tab(label='LTV by Product', value='ltv-by-product-tab'),
            dcc.Tab(label='Retention by Product', value='retention-by-product-tab'),
            dcc.Tab(label='Basket Analysis', value='basket-analysis')
        ]),
        html.Div(id='tab-content')
    ],
    style = {'display':'none'}
)

app.layout = html.Div([login_layout, dashboard_layout])

@app.callback(
    dash.dependencies.Output("dashboard-container", "style"),
    dash.dependencies.Output("login-container", "style"),
    dash.dependencies.Output("output-message", "children"),
    dash.dependencies.Input("login-button", "n_clicks"),
    dash.dependencies.State("username-input", "value"),
    dash.dependencies.State("password-input", "value")
)
def login(n_clicks, username, password):
    if n_clicks > 0:
        # Check if the username and password are correct
        if username == "jessie@ever-eden.com" and password == "Evereden2023!":
            # Hide the login container and show the dashboard container
            return {"display": "block"}, {"display": "none"}, ""
        else:
            # Show the login container and display an error message
            return {"display": "none"}, {"display": "block"}, "Login failed. Please try again."

    return {"display": "none"}, {"display": "block"}, ""



@app.callback(
    dash.dependencies.Output('tab-content', 'children'),
    [dash.dependencies.Input('tabs', 'value')]
)
def render_content(tab):
    if tab == 'cohort-tab':
        return html.Div([
            html.H2("Retention Rate by Cohort"),
            html.Div([
                html.H3("Retention Rate in Absolute Value"),
                dash_table.DataTable(
                    id='retention-absolute-table',
                    columns=[{"name": "Cohort", "id": "cohort"}] + [{"name": str(col), "id": str(col)} for col in retention_absolute.columns],
                    data=retention_absolute.reset_index().to_dict('records'),
                    style_table={'overflowX': 'scroll'},
                    style_cell={'minWidth': '100px', 'width': '100px', 'maxWidth': '100px', 'textAlign': 'center'}
                )
            ]),
            html.Div([
                html.H3("Retention Rate in Percentage"),
                dash_table.DataTable(
                    id='retention-percentage-table',
                    columns=[{"name": "Cohort", "id": "cohort"}] + [{"name": str(col), "id": str(col)} for col in retention_percentage.columns],
                    data=retention_percentage.reset_index().to_dict('records'),
                    style_table={'overflowX': 'scroll'},
                    style_cell={'minWidth': '100px', 'width': '100px', 'maxWidth': '100px', 'textAlign': 'center'}
                )
            ]),
            html.Div([
                html.H3("Retention Rate in Cumulative Value"),
                dash_table.DataTable(
                    id='retention-cumulative-table',
                    columns=[{"name": "Cohort", "id": "cohort"}] + [{"name": str(col), "id": str(col)} for col in retention_cumulative.columns],
                    data=retention_cumulative.reset_index().to_dict('records'),
                    style_table={'overflowX': 'scroll'},
                    style_cell={'minWidth': '100px', 'width': '100px', 'maxWidth': '100px', 'textAlign': 'center'}
                )
            ]),
            html.Div([
                html.H3("Retention Rate in Cumulative Percentage"),
                dash_table.DataTable(
                    id='retention-cum-percentage-table',
                    columns=[{"name": "Cohort", "id": "cohort"}] + [{"name": str(col), "id": str(col)} for col in retention_cum_percentage.columns],
                    data=retention_cum_percentage.reset_index().to_dict('records'),
                    style_table={'overflowX': 'scroll'},
                    style_cell={'minWidth': '100px', 'width': '100px', 'maxWidth': '100px', 'textAlign': 'center'}
                )
            ]),
            html.Div([
                html.H3("Retention Rate in Cumulative Value [Unique Customer]"),
                dash_table.DataTable(
                    id='retention-cum-unique-table',
                    columns=[{"name": "Cohort", "id": "cohort"}] + [{"name": str(col), "id": str(col)} for col in retention_cumulative_unique.columns],
                    data=retention_cumulative_unique.reset_index().to_dict('records'),
                    style_table={'overflowX': 'scroll'},
                    style_cell={'minWidth': '100px', 'width': '100px', 'maxWidth': '100px', 'textAlign': 'center'}
                )
            ]),
            html.Div([
                html.H3("Retention Rate in Cumulative Percentage [Unique Customer]"),
                dash_table.DataTable(
                    id='retention-cum-percentage-unique-table',
                    columns=[{"name": "Cohort", "id": "cohort"}] + [{"name": str(col), "id": str(col)} for col in retention_cum_percentage_unique.columns],
                    data=retention_cum_percentage_unique.reset_index().to_dict('records'),
                    style_table={'overflowX': 'scroll'},
                    style_cell={'minWidth': '100px', 'width': '100px', 'maxWidth': '100px', 'textAlign': 'center'}
                )
            ])
        ])
    elif tab == 'ltv-tab':
        return html.Div([
            html.H2("Customer Lifetime Value (LTV)"),
            dash_table.DataTable(
                id='ltv-table',
                columns=[{"name": "Cohort", "id": "cohort"}] + [{"name": str(col), "id": str(col)} for col in ltv_cohorts.columns],
                data=ltv_cohorts.reset_index().to_dict('records'),
                style_table={'overflowX': 'scroll'},
                style_cell={'minWidth': '100px', 'width': '100px', 'maxWidth': '100px', 'textAlign': 'center'}
            )
        ])
    elif tab == 'ltv-by-product-tab':
        return html.Div([
            html.H2("LTV by Product"),
            html.Div([
                html.Label("Select Product Name"),
                dcc.Dropdown(
                    id='ltv-product-dropdown',
                    options=[{'label': name, 'value': name} for name in sorted(product_names)],
                    value=sorted(product_names)[0]
                )
            ]),
            html.Div(id = 'ltv-by-product-content')
        ])
    elif tab == 'retention-by-product-tab':
        return html.Div([
            html.H2("Retention Rate by Product"),
            html.Div([
                html.Label("Select Product Name"),
                dcc.Dropdown(
                    id='retention-product-dropdown',
                    options=[{'label': name, 'value': name} for name in sorted(product_names)],
                    value=sorted(product_names)[0]
                )
            ]),
            html.Div(id = 'retention-by-product-content')
        ])
    elif tab == 'basket-analysis':
        return html.Div([
            html.H2("Basket Analysis"),
            html.Div([
                html.Label("Select Date Range  "),
                dcc.DatePickerRange(
                    id = 'date-picker',
                    start_date_placeholder_text="Start Period",
                    end_date_placeholder_text="End Period",
                    max_date_allowed=max_date)
            ]),
            html.Div(id = 'basket-analysis-content')
        ])
    
    
@app.callback(
    dash.dependencies.Output('ltv-by-product-content', 'children'),
    dash.dependencies.Input('ltv-product-dropdown', 'value')
)
def update_new_ltv_table(ltv_selected_product):
    filtered_data = shopify_data.loc[(shopify_data['customer_type'] == 'First-time') & (shopify_data['product_title'] == ltv_selected_product)]
    ltv_by_product = shopify_data.loc[shopify_data['customer_id'].isin(filtered_data['customer_id'].values)]
    ltv_by_product = ltv_by_product.drop(columns = ['customer_type'])
    ltv_by_product['day']= pd.to_datetime(ltv_by_product['day'], dayfirst=True)
    ltv_by_product = ltv_by_product.sort_values(['customer_id','day'])
    ltv_by_product.reset_index(inplace = True, drop = True)
    ltv_by_product['month'] =pd.to_datetime(ltv_by_product['day']).dt.month
    ltv_by_product['Purchase Rate'] = purchase_rate(ltv_by_product['customer_id'], ltv_by_product['day'])
    ltv_by_product['Join Date'] = join_date(ltv_by_product['day'], ltv_by_product['Purchase Rate'])
    ltv_by_product['Join Date'] = pd.to_datetime(ltv_by_product['Join Date'], dayfirst=True)
    ltv_by_product['cohort'] = pd.to_datetime(ltv_by_product['Join Date']).dt.strftime('%Y-%m')
    ltv_by_product['year'] = pd.to_datetime(ltv_by_product['day']).dt.year
    ltv_by_product['Join Date Month'] = pd.to_datetime(ltv_by_product['Join Date']).dt.month
    ltv_by_product['Join Date Year'] = pd.to_datetime(ltv_by_product['Join Date']).dt.year
    ltv_by_product['Age by month'] = age_by_month(ltv_by_product['Purchase Rate'], ltv_by_product['month'],ltv_by_product['year'],ltv_by_product['Join Date Month'],ltv_by_product['Join Date Year'])
        
    f_ltv_product = ltv_by_product.copy()
    f_ltv_product = f_ltv_product.groupby(['cohort','Age by month'])['sales'].sum().to_frame().reset_index()
    f_ltv_product['cum_sum'] = f_ltv_product.groupby('cohort')['sales'].cumsum()
    f_ltv_product['num_customer'] = ltv_by_product.groupby(['cohort','Age by month']).nunique().reset_index()['customer_id']
    f_ltv_product['monthly_new_customers'] = f_ltv_product.apply(assign_value, axis = 1)
    f_ltv_product['monthly_new_customers'] = f_ltv_product['monthly_new_customers'].fillna(method = 'ffill')
    f_ltv_product['avg_LTV'] = f_ltv_product['cum_sum']/f_ltv_product['monthly_new_customers']
    f_ltv_product['avg_LTV'] = f_ltv_product['avg_LTV'].round(2)
    
    # change Age by month format, so that after change the type to string, it will sort by age by month correctly in the table
    f_ltv_product['Age by month'] = f_ltv_product['Age by month'].apply(lambda x: "{0:0=2d}".format(x))
    f_ltv_product['cohort'] = f_ltv_product['cohort'].astype(str)
    f_ltv_product['Age by month'] = f_ltv_product['Age by month'].astype(str)

    f_ltv_product_tb = f_ltv_product.pivot_table(values = 'avg_LTV',index = 'cohort', columns= 'Age by month', fill_value = '').reset_index()
    
    # add cohort number of customers to second column
    f_ltv_product_tb['New Customer Acquired'] = f_ltv_product[['cohort','monthly_new_customers']].drop_duplicates()['monthly_new_customers'].values
    first_column = f_ltv_product_tb.pop('New Customer Acquired')
    f_ltv_product_tb.insert(1, 'New Customer Acquired', first_column)
    f_ltv_product_tb

    
    ltv_initial_table = dash_table.DataTable(
            data=f_ltv_product_tb.to_dict('records'),
            columns=[{"name": str(col), "id": str(col)} for col in f_ltv_product_tb.columns],
            style_table={'overflowX': 'scroll'},
            style_cell={'minWidth': '100px', 'width': '100px', 'maxWidth': '100px', 'textAlign': 'center'}
        )
    return ltv_initial_table


@app.callback(
    dash.dependencies.Output('retention-by-product-content', 'children'),
    dash.dependencies.Input('retention-product-dropdown', 'value')
)
def update_new_retention_table(retention_selected_product):
    filtered_data = shopify_data.loc[(shopify_data['customer_type'] == 'First-time') & (shopify_data['product_title'] == retention_selected_product)]
    retention_by_product = shopify_data.loc[shopify_data['customer_id'].isin(filtered_data['customer_id'].values)]
    retention_by_product = retention_by_product.drop(columns = ['customer_type'])
    retention_by_product['day']= pd.to_datetime(retention_by_product['day'], dayfirst=True)
    retention_by_product = retention_by_product.sort_values(['customer_id','day'])
    retention_by_product.reset_index(inplace = True, drop = True)
    retention_by_product['month'] =pd.to_datetime(retention_by_product['day']).dt.month
    retention_by_product['Purchase Rate'] = purchase_rate(retention_by_product['customer_id'],retention_by_product['day'])
    retention_by_product['Join Date'] = join_date(retention_by_product['day'], retention_by_product['Purchase Rate'])
    retention_by_product['Join Date'] = pd.to_datetime(retention_by_product['Join Date'], dayfirst=True)
    retention_by_product['cohort'] = pd.to_datetime(retention_by_product['Join Date']).dt.strftime('%Y-%m')
    retention_by_product['year'] = pd.to_datetime(retention_by_product['day']).dt.year
    retention_by_product['Join Date Month'] = pd.to_datetime(retention_by_product['Join Date']).dt.month
    retention_by_product['Join Date Year'] = pd.to_datetime(retention_by_product['Join Date']).dt.year
    retention_by_product['Age by month'] = age_by_month(retention_by_product['Purchase Rate'], retention_by_product['month'],retention_by_product['year'],retention_by_product['Join Date Month'],retention_by_product['Join Date Year'])
    
    ######
    retention_by_product_cohorts = retention_by_product.groupby(['cohort', 'Age by month']).nunique()
    retention_by_product_cohorts = retention_by_product_cohorts.customer_id.to_frame().reset_index()   # convert series to frame
    retention_by_product_cohorts = pd.pivot_table(retention_by_product_cohorts, values='customer_id', index='cohort', columns='Age by month').reset_index()
    retention_absolute_by_product = retention_by_product_cohorts.replace(np.nan, '', regex=True)
    ######
   
    retention_abs_tb = dash_table.DataTable(
            data=retention_absolute_by_product.to_dict('records'),
            columns=[{"name": str(col), "id": str(col)} for col in retention_absolute_by_product.columns],
            style_table={'overflowX': 'scroll'},
            style_cell={'minWidth': '100px', 'width': '100px', 'maxWidth': '100px', 'textAlign': 'center'}
        )
    
    #retention_by_product_cohorts.reset_index(drop=True, inplace=True)
    
    ######
    for i in range(2, len(retention_by_product_cohorts.columns)):
        retention_by_product_cohorts.iloc[:, i] = retention_by_product_cohorts.iloc[:, i] / retention_by_product_cohorts.iloc[:, 1]

    retention_abs_per_by_product = retention_by_product_cohorts.copy()
    retention_abs_per_by_product.iloc[:, 2:] = retention_abs_per_by_product.iloc[:, 2:].applymap(lambda x: '{:.2%}'.format(x) if pd.notnull(x) else '')
    ######

    retention_abs_per_tb = dash_table.DataTable(
            data=retention_abs_per_by_product.to_dict('records'),
            columns=[{"name": str(col), "id": str(col)} for col in retention_abs_per_by_product.columns],
            style_table={'overflowX': 'scroll'},
            style_cell={'minWidth': '100px', 'width': '100px', 'maxWidth': '100px', 'textAlign': 'center'}
        ) 

    
    ######
    retention_cum_product = retention_absolute_by_product.apply(pd.to_numeric, errors='coerce').copy()
    for i in range(3, retention_cum_product.shape[1]):
        retention_cum_product.iloc[:, i] = retention_cum_product.iloc[:, i].add(retention_cum_product.iloc[:, i-1], fill_value=0)
        retention_cum_product['cohort'] = retention_absolute_by_product['cohort'].values
    
    ######
    
    retention_cum_tb = dash_table.DataTable(
            data=retention_cum_product.to_dict('records'),
            columns=[{"name": str(col), "id": str(col)} for col in retention_cum_product.columns],
            style_table={'overflowX': 'scroll'},
            style_cell={'minWidth': '100px', 'width': '100px', 'maxWidth': '100px', 'textAlign': 'center'}
        ) 
    

    ######
    retention_cum_per_product = retention_cum_product.copy()
    for i in range(2, len(retention_cum_per_product.columns)):
        retention_cum_per_product.iloc[:, i] = retention_cum_per_product.iloc[:, i]/ retention_cum_per_product.iloc[:, 1]
    retention_cum_per_product.iloc[:, 2:] = retention_cum_per_product.iloc[:, 2:].applymap(lambda x: '{:.2%}'.format(x) if pd.notnull(x) else '')
    retention_cum_per_product['cohort'] = retention_cum_product['cohort'].values
    ######
    
    retention_cum_per_tb = dash_table.DataTable(
            data=retention_cum_per_product.to_dict('records'),
            columns=[{"name": str(col), "id": str(col)} for col in retention_cum_per_product.columns],
            style_table={'overflowX': 'scroll'},
            style_cell={'minWidth': '100px', 'width': '100px', 'maxWidth': '100px', 'textAlign': 'center'}
        ) 
     #######
    
    retention_by_product_unique = retention_by_product[retention_by_product['Purchase Rate'] == 2]
    retention_by_product_cohorts = retention_by_product_unique.groupby(['cohort', 'Age by month']).nunique()
    retention_by_product_cohorts = retention_by_product_cohorts.customer_id.to_frame().reset_index()
    retention_by_product_cohorts = pd.pivot_table(retention_by_product_cohorts, values='customer_id', index='cohort', columns='Age by month')

    unique_retention_product_absolute = retention_by_product_cohorts.replace(np.nan, '', regex=True)
    new_c = retention_by_product.groupby(['cohort']).nunique().customer_id.to_frame().reset_index()
    unique_retention_product_absolute = pd.merge(new_c, unique_retention_product_absolute, how = 'left', on = 'cohort').fillna(0)
    unique_retention_product_absolute.rename(columns={'customer_id':'New Customer'}, inplace=True)
    unique_retention_product_absolute = unique_retention_product_absolute.set_index(unique_retention_product_absolute.columns[0])

    retention_cumulative_product_unique = unique_retention_product_absolute.apply(pd.to_numeric, errors='coerce').copy()
    for i in range(2, retention_cumulative_product_unique.shape[1]):
        retention_cumulative_product_unique.iloc[:, i] = retention_cumulative_product_unique.iloc[:, i].add(retention_cumulative_product_unique.iloc[:, i-1], fill_value=0)
    
    retention_cum_per_product_unique = retention_cumulative_product_unique.copy()
    for i in range(1, len(retention_cum_per_product_unique.columns)):
        retention_cum_per_product_unique.iloc[:, i] = retention_cum_per_product_unique.iloc[:, i]/ retention_cum_per_product_unique['New Customer']
    retention_cum_per_product_unique.iloc[:, 1:] = retention_cum_per_product_unique.iloc[:, 1:].applymap(lambda x: '{:.2%}'.format(x) if pd.notnull(x) else '')
    retention_cum_per_product_unique['New Customer'] = retention_cumulative_product_unique['New Customer'].values

    ########
    
    retention_cum_per_unique_tb = dash_table.DataTable(
            data=retention_cum_per_product_unique.reset_index().to_dict('records'),
            columns=[{"name": "Cohort", "id": "cohort"}] + [{"name": str(col), "id": str(col)} for col in retention_cum_per_product_unique.columns],
            style_table={'overflowX': 'scroll'},
            style_cell={'minWidth': '100px', 'width': '100px', 'maxWidth': '100px', 'textAlign': 'center'}
        )     

    return html.Div([html.H3("In Absolute Value"),
                     retention_abs_tb, 
                     html.Hr(),
                     html.H3("In Absolute Percentage"),
                     retention_abs_per_tb,
                     html.Hr(),
                     html.H3("In Cumulative Value"),
                     retention_cum_tb,
                     html.Hr(),
                     html.H3("In Cumulative Percentage"),
                     retention_cum_per_tb,
                     html.Hr(),
                     html.H3("In Cumulative Percentage [Unique Customer]"),
                     retention_cum_per_unique_tb
                    ])


@app.callback(
    dash.dependencies.Output('basket-analysis-content', 'children'),
    dash.dependencies.Input('date-picker', 'start_date'),
    dash.dependencies.Input('date-picker', 'end_date')
)

def update_new_basket_analysis_table(selected_start_date, selected_end_date):
    basket_data = pd.read_csv('https://raw.githubusercontent.com/JessieYu3161/retention-ltv/main/src/shopify_df.csv')
    # exclude emails contain 'ever-eden.com'
    basket_data = basket_data[basket_data['customer_email'].str.contains('ever-eden.com') == False]
    basket_data = basket_data[basket_data['product_title'].str.contains('Mini') == False]
    basket_data.loc[basket_data['product_title'] == 'Nourishing Lip Balm', 'product_title'] = 'Baby Lip Balm'
    basket_data.loc[basket_data['product_title'] == 'Jumbo-Sized Soothing Baby Massage Oil', 'product_title'] = 'Jumbo Soothing Baby Massage Oil'
    basket_data = basket_data[(basket_data['product_type'] != 'GWP')&(basket_data['product_type'] != 'sample')&(basket_data['product_type'] != 'free_sample')&(basket_data['product_type'] != 'crm_sample')]
    basket_data = basket_data[basket_data['product_title'] != 'Exclusive Beauty Bag']
    basket_data = basket_data[basket_data['gross_sales']>0]
    basket_data = basket_data[(basket_data['day'] > selected_start_date) & (basket_data['day'] < selected_end_date)]
    
    order_ids = basket_data.groupby(['order_id'])['product_title'].count().reset_index()
    order_ids = order_ids[order_ids['product_title'] > 1]
    order_ids = order_ids['order_id']

    basket_data = basket_data.loc[basket_data['order_id'].isin(order_ids)]
    basket_data = basket_data.sort_values(['order_id','product_title'], ascending=True).groupby('order_id')['product_title'].apply(', '.join).reset_index()
    basket_tb = basket_data['product_title'].value_counts().to_frame().reset_index()
    basket_tb = basket_tb.head(300)
    basket_tb.columns = ['Product Combinations', '# of Orders']
    
    insert_row = pd.DataFrame({'Product Combinations':'Total', '# of Orders': sum(basket_tb['# of Orders'])},index =[0])
    basket_tb = pd.concat([insert_row, basket_tb]).reset_index(drop = True)
    
    column_widths = [{'if': {'column_id': 'Product Combinations'}, 'width': '400px'},
                     {'if': {'column_id': '# of Orders'}, 'width': '10px'}]
    
    basket_analysis_tb = dash_table.DataTable(
            data=basket_tb.to_dict('records'),
            columns=[{"name": str(col), "id": str(col)} for col in basket_tb.columns],
            style_table={'overflowX': 'scroll'},
            style_cell={'textAlign': 'left'},
            page_size=20,
            style_cell_conditional=column_widths
        ) 
    return basket_analysis_tb


# Run the app
if __name__ == '__main__':
    app.run_server(mode='inline')


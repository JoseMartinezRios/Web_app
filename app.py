"""
Display simple plots on the web browser
"""
import pandas as pd
import streamlit as st
import plotly.express as px

path = 'notebooks/dataset_clean.csv'
df = pd.read_csv(path)

# Create the dataframes for each plot
#BEST SELLERS BY COMPANY
best_sellers = df.pivot_table(index='vehicle_make',
                              values='vehicle_model',
                              aggfunc='count').reset_index()
best_sellers = best_sellers.sort_values(by='vehicle_model', ascending = False).head(20)

#percentage of sales, from the previous dataframe
percentage_sellers = best_sellers.copy()
percentage_sellers['vehicle_model'] = percentage_sellers['vehicle_model'].apply(
        lambda x: round(
            ((x/percentage_sellers['vehicle_model'].sum())*100)
            ,3))

# BEST SELLERS BY MODEL
best_sellers_model = df.pivot_table(index='vehicle_model',
                                    values='vehicle_make',
                                    aggfunc='count').reset_index()
best_sellers_model = best_sellers_model.sort_values(by='vehicle_make', ascending=False).head(20)

# BEST SELLERS, TYPE OF EV
best_types = df.groupby('vehicle_type')['vehicle_model'].count().reset_index()
best_types['vehicle_model'] = round(
        ((best_types['vehicle_model']/best_types['vehicle_model'].sum())*100)
        ,3)

# COUNTY WITH MOST SALES
best_sellers_county = df.pivot_table(index='location',
                                     values='vehicle_model',
                                     aggfunc='count').reset_index()
best_sellers_county = best_sellers_county.sort_values(by='vehicle_model', ascending=False)

# YEAR WITH MORE SALES
yearly_sales = df.pivot_table(index='year',
                              values='vehicle_model',
                              aggfunc='count').reset_index()

# SALES YEAR, MONTH
sales_year = df.groupby(['year', 'month'])['vehicle_model'].count().reset_index()

# Prepare the plots
#plot 1, best sellers by manufacturer
fig1 = px.bar(best_sellers.head(10),
              x='vehicle_make',
              y='vehicle_model')
fig1.update_layout(
        title="Best Seller manufacturer",
        xaxis_title="",
        yaxis_title="Total Sales")

#plot 2, percentage of sales by maker
top_10 = percentage_sellers.head(10)
fig2 = px.bar(top_10,
              x='vehicle_make',
              y='vehicle_model',
              title='Percentage of sales by Each maker',
              labels={'vehicle_make': 'Manufacturer', 'vehicle_model': 'Percentage'},
              color_discrete_sequence=['magenta'])
fig2.update_layout(
        xaxis_tickangle=-90,
        yaxis_title='Percentage',
        xaxis_title='Manufacturer',
        showlegend=False,
        plot_bgcolor='white',
        yaxis=dict(gridcolor='lightgray'))

#plot 3, best sellers models
fig3 = px.bar(
        best_sellers_model,
        x='vehicle_model',
        y='vehicle_make'
        )
fig3.update_layout(
        title='Best sellers models',
        xaxis_title="",
        yaxis_title="Total sales"
        )

#plot 4, best sellers types of ev
fig4 = px.bar(
        best_types,
        x='vehicle_type',
        y='vehicle_model'
        )
fig4.update_layout(
        title='Preferred type of vehicles',
        xaxis_title='',
        yaxis_title='Percent of sales',
        )

#plot 5, county with more sales
fig5 = px.bar(
        best_sellers_county,
        x='location',
        y='vehicle_model'
        )
fig5.update_layout(
        title='County sales comparison',
        xaxis_tickangle=-90,
        xaxis_title='',
        yaxis_title='Sales'
        )

#plot 6, year sales
fig6 = px.bar(
        yearly_sales,
        x='year',
        y='vehicle_model')
fig6.update_layout(
        xaxis_title='Year',
        yaxis_title='Sales per year',
        title='Difference from the past year',
        )

#plot 7, sales year, month
fig7 = px.bar(sales_year,
              x='month',
              y='vehicle_model',
              color='year'
              )
fig7.update_layout(
        title='How sales changed since the past year',
        showlegend=False,
        xaxis_title='Month',
        yaxis_title='Sales',
        )

#----------CREATE THE STREAMLIT PAGE.
st.header('Electric Vehicles data analysis')
st.write(
        'The following exploratory analysis was according to a Discord group of Data Buddies thatwhere we try to do our best polishing our -Data skills- in order to improve ourselves\nGreetings to you all'
        )

st.plotly_chart(fig1, use_container_width=True)
st.subheader('Best-seller on the market')
st.write("It's true that Tesla often dominates the headlines -whether it's news about its automotive innovations or ventures like SpaceX. However their core industry remains vehicle manufacturing. As the graphic shows, Tesla accounts for nearly half of all sales in the Nova Scotia market making the clear leader in this region.")

st.subheader('Hyundai motors')
st.write("Hyundai's electric vehicle division has been growing rapidly in recent years -almost like bubbles rising the surface. While many other manufacturers continue to focus on traditional gasoline models, Hyundai has steadly increased its commitment to green technologies, positioning itself as a forward thinking player in the EV space.")

st.plotly_chart(fig2, use_container_width=True)
st.subheader("Numbers don't lie")
st.write("This plot clearly reinforces the point discussed earlier, *35% of total sales come from Tesla's electric vehicles")
st.write("It's no surprise -those constant headlines do their job well, keeping Tesla at the center of public conversation and market attention.")

st.plotly_chart(fig3, use_container_width=True)

st.plotly_chart(fig4, use_container_width=True)
st.subheader("Family-Friendly = Comfort for Everyone")
st.write("As shown in the plot, SUVs represent the leading vehicle type, accounting for 51% of total sales. Families have consistently chose these models for several reasons -comfort being the top priority. If a vehicle can handle long cross-country trips without disturbing the children inside, it becomes the ideal choice for those seeking a quiet, smooth ride. Electric SUVs also offer fewer mechanicla issues. Everyone knows that when a traditional car breaks down, the repair process can be unpredictable -depending on the mechanic, it might take days or even weeks. Worse still, if the issue isn't properly fixed, you could end up paying twice (or more) for something that should've been minor.In contrast, electric vehicles have fewer moving parts, can be serviced at well equipped locations, and often cost less to maintain than their gasoline counterparts.")
st.subheader("Beach, Parties, and Sun (At least in Summertime)")
st.write("Another segment of the market revolves around family vacations, summer getaways, and events across Nova Scotia. The region offers a packed summer calendar filled with parades, concerts, international food courts, beach walks, and stunning locations to explore. This tourism-driven market is largely supported by rental car agencies, which have increasingly adopoted electric vehicles for the same reasons mentioned above. Families visiting for a peaceful vacation prefer quiet, eco-friendly transportation -avoiding the noise and emissions of traditional gasoline cars.")

st.plotly_chart(fig5, use_container_width=True)
st.subheader("The best place to start")
st.write('While most electric sales come from Halifax County, the largest and most central county in Nova Scotia, the highest percentage of EV ownership is found in Lunenburg County. Known for its deep connection to sailing -where people live for sail, from sail, and by sail- the region attracts many visitors drawn to its maritime charm and vibrant coastal lifestyle.')
st.write("Halifax, being the province's main urban center, drives nearly 40% of total sales. That's not small feat - it's a dominant force in the market. Just one glance at the plot makes it clear: Halifax isn't just participating, it's leading.")

st.plotly_chart(fig6, use_container_width=True)
st.subheader("Such a surprise")
st.write("*Most of the sales occur in January, June, and July.* This pattern may be linked to seasonal factors such as weather, local festivals, school vacation periods, and the influx of tourists seeking rental cars to explore the province.")
st.write("*January is naturally tied to New Year celebrations and the tail end of the Christmas season.* While household budgets may be tighter after the holidays, some buyers are drawn to post-holiday 'hot-sales' on electric vehicles. In recent years EVs have steadly gained market share -led prominently by Tesla, whose CEO and models frequently make headlines. Beyond the hype, deeper research suggests that EVs appeal to buyers who prefer to avoid the complex maintenance demands of conventional gasoline vehicles.")
st.write("*June and July bring a different dynamic.* Mid-year in Nova Scotia is rich with cultural events, parades, scenic excursions, and family-friendly activities such as hiking, sailing, and exploring the coastline. Many tourists have flexible schedules during this period, making it an ideal time to travel. For families, renting a car for a week or month often proves more economical than relying on taxis or hiring a driver for full-day trips -especially when they want the freedom to explore at their own pace.")

st.plotly_chart(fig7, use_container_width=True)
st.subheader("Prepare the stock")
st.write("The plot reveals a clear upward trend in electric vehicle (EV) sales over the past year. This growth provides a solid foundation for estimating the average number of vehicles to keep in stock for the upcoming year. By analyzing seasonal peaks, we can prepare for high-demand periods -adjusting staffing schedules, planning vacation rotations, launching hiring compaigns, and ensuring that physical spaces and spare parts inventory are ready to meet demand. With close coordination between operations and the marketing team, future sales can be strategically boosted around these key dates, maximizing impact and efficinecy.")
st.subheader("Sales per year")
st.write("One standout insight form the bar plot is the contrast between 2024 and 2025. last year's sales were relatively low -likely due to the store's initial launch phase- but this year, 2025, show a dramatic rise: 43.1% growth. That's not just impressive -it's a signal. The market is clearly responding to new models, fresh promotions, and growing consumer interest. The demand is here, and it's loud. Now's the time to act boldly, stock smartly, and ride the wave of momentum.")


# Step 1: Reading CSV File & Step 2: Total Sale
import csv

# Calculate yearly totals
year_totals = {}
header = []
with open('Data.csv', mode = 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        if not header:
            header = row
        else:
            year = int(row[0])
            year_total = sum([int(x.replace(',', '')) for x in row[1:]])
            year_totals[year] = year_total

# Write yearly totals to file
with open('stats.txt', 'w') as file:
    for year in range(2012, 2022):
        if year in year_totals:
            line = f"{year}: {year_totals[year]:,}\n"
        else:
            line = f"{year}: 0\n"
        file.write(line)

# Step 3: Bar Plot
import matplotlib.pyplot as plt

with open('stats.txt', 'r') as file:
    data = file.readlines()

years = []
sales = []

# Extract the years and sales from the data
for line in data:
    year, sales_str = line.strip().split(': ')
    years.append(int(year))
    sales.append(int(sales_str.replace(',', '')))

plt.bar(years, sales)
plt.title('Total Sales Per Year')
plt.xlabel('Year')
plt.ylabel('Total Sales')

plt.xticks(range(2012, 2022))
plt.gca().set_xticklabels(range(2012, 2022))

plt.show()

# Step 4: Sale Estimation
# Calculate sales growth rate and estimated sales
sales_2021 = 0
sales_2022 = 0
with open('Data.csv', mode = 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        if int(row[0]) == 2021:
            sales_2021 += sum([int(x.replace(',', '')) for x in row[1:7]])
        elif int(row[0]) == 2022:
           sales_2022 += sum([int(x.replace(',', '')) for x in row[1:7]])
sgr = (sales_2022 - sales_2021) / sales_2022
rounded_sgr = round(sgr, 2)
with open ('stats.txt', 'a') as f:
    f.write(f'Sales Growth Rate: {rounded_sgr}\n')
estimated_sales = []
for month in range(8, 14):
    with open('Data.csv', mode = 'r') as file:
        csv_reader = csv.reader(file)
        sales_2021_monthly = int(next(row[month-1].replace(',', '') for row in csv_reader if row[0] == '2021'))
        estimated_sales.append(sales_2021_monthly + sales_2021_monthly * sgr)
with open('stats.txt', 'a') as file:
    file.write('Estimated Sales for Last Six Months of 2022:\n')
    for month, sales in zip(range(8, 14), estimated_sales):
        file.write(f'{month}-2022: {sales:,.0f}\n')


# Step 5: Horizontal Bar Plot
# Read the estimated sales data from the stats.txt file
estimated_sales = []
with open('stats.txt', 'r') as file:
    for line in file:
        if line.startswith('Estimated Sales for Last Six Months of 2022:'):
            break
    for line in file:
        month, sales_str = line.strip().split(': ')
        estimated_sales.append(float(sales_str.replace(',', '')))

month_names = ['July', 'August', 'September', 'October', 'November', 'December']
plt.barh(month_names, estimated_sales)
plt.title('Estimated Sales for Last Six Months of 2022')
plt.xlabel('Estimated Sales')
plt.ylabel('Month')
plt.show()


from faker import Faker
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

fake = Faker()
Faker.seed(123)
np.random.seed(123)
random.seed(123)

# List of African countries with their population factors
african_countries = [
    ('Nigeria', 0.25), ('Ethiopia', 0.15), ('Egypt', 0.14), 
    ('DR Congo', 0.12), ('South Africa', 0.10), ('Kenya', 0.08),
    ('Ghana', 0.06), ('Morocco', 0.05), ('Angola', 0.03), ('Uganda', 0.02)
]

# Mobile service providers by country
providers_by_country = {
    'Nigeria': ['MTN', 'Airtel', 'Glo', '9mobile'],
    'South Africa': ['Vodacom', 'MTN', 'Cell C', 'Telkom'],
    'Kenya': ['Safaricom', 'Airtel', 'Telkom Kenya'],
    'Egypt': ['Orange', 'Vodafone', 'Etisalat'],
    'Ghana': ['MTN', 'AirtelTigo', 'Glo'],
    'Morocco': ['Maroc Telecom', 'Orange', 'Inwi'],
    'Ethiopia': ['Ethio Telecom', 'Safaricom'],
    'DR Congo': ['Vodacom', 'Orange', 'Airtel'],
    'Angola': ['Unitel', 'Movicel'],
    'Uganda': ['MTN', 'Airtel', 'Africell']
}

NUM_USERS = 2000
NUM_DAYS = 60

print(f"Generating mobile usage data for {NUM_USERS} users over {NUM_DAYS} days...")

def generate_user_profile():
    """Generate a user profile with demographic info"""
    country_names = [c[0] for c in african_countries]
    country_weights = [c[1] for c in african_countries]
    selected_country = random.choices(country_names, weights=country_weights)[0]
    
    return {
        'user_id': fake.unique.random_number(digits=6),
        'age': random.randint(18, 65),
        'gender': random.choice(['Male', 'Female']),
        'country': selected_country,
        'city': fake.city(),
        'provider': random.choice(providers_by_country.get(selected_country, ['MTN'])),
        'subscription_type': random.choices(
            ['Prepaid', 'Postpaid'], 
            weights=[0.7, 0.3]
        )[0],
        'device_brand': random.choice(['Samsung', 'Apple', 'Huawei', 'Tecno', 'Infinix', 'Nokia']),
        'joined_date': fake.date_between(start_date='-730d', end_date='-30d')
    }

# Generate user profiles
users = [generate_user_profile() for _ in range(NUM_USERS)]

# Create daily usage records
records = []
start_date = datetime.now() - timedelta(days=NUM_DAYS)

for user in users:
    for day in range(NUM_DAYS):
        date = start_date + timedelta(days=day)
        day_of_week = date.strftime('%A')
        
        # ============ FIXED: Use np.random.lognormal ============
        # Base usage with variation - using NumPy's lognormal
        base_data = np.random.lognormal(mean=3.5, sigma=0.8)
        age_factor = 1.5 if user['age'] < 25 else (0.7 if user['age'] > 50 else 1.0)
        country_factor = 1.3 if user['country'] in ['South Africa', 'Nigeria', 'Egypt'] else 1.0
        
        data_mb = max(0, base_data * age_factor * country_factor + np.random.uniform(-50, 50))
        data_mb = round(data_mb, 1)
        
        call_minutes = max(0, np.random.lognormal(mean=3.2, sigma=0.7) * (0.8 if user['age'] < 30 else 1.2))
        call_minutes = round(call_minutes, 1)
        
        sms_count = max(0, np.random.poisson(lam=3 + (0.02 * (user['age'] - 30))))
        sms_count = int(min(sms_count, 50))
        
        revenue = round(data_mb * 0.02 + call_minutes * 0.05 + sms_count * 0.01, 2)
        
        if day_of_week in ['Saturday', 'Sunday']:
            data_mb = data_mb * 1.4
            call_minutes = call_minutes * 0.7
            sms_count = int(sms_count * 0.6)
            revenue = revenue * 1.1
        
        if random.random() < 0.005:
            data_mb = np.nan
        
        records.append({
            'user_id': user['user_id'],
            'date': date,
            'day_of_week': day_of_week,
            'age': user['age'],
            'gender': user['gender'],
            'country': user['country'],
            'city': user['city'],
            'provider': user['provider'],
            'subscription_type': user['subscription_type'],
            'device_brand': user['device_brand'],
            'data_mb': data_mb,
            'call_minutes': call_minutes,
            'sms_count': sms_count,
            'revenue_usd': revenue
        })

# Create DataFrame
df = pd.DataFrame(records)

# Add calculated fields
df['month'] = pd.to_datetime(df['date']).dt.month
df['quarter'] = pd.to_datetime(df['date']).dt.quarter
df['year'] = pd.to_datetime(df['date']).dt.year

# Create the data folder if it doesn't exist
os.makedirs('../data', exist_ok=True)

# Save the data
df.to_csv('../data/africa_mobile_usage.csv', index=False)

print(f"✅ Mobile data saved to ../data/africa_mobile_usage.csv")
print(f"📊 Total records: {len(df):,}")
print(f"👥 Total users: {df['user_id'].nunique():,}")
print(f"🌍 Countries: {df['country'].nunique()}")

# Display sample
print("\n📋 Sample data:")
print(df.head(10))
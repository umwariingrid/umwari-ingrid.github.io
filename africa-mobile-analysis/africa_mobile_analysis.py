import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("viridis")

# Load data
df = pd.read_csv('../data/africa_mobile_usage.csv')

print("=" * 60)
print("AFRICAN MOBILE USAGE ANALYSIS REPORT")
print("=" * 60)

# Basic stats
print(f"\n📊 Dataset Overview:")
print(f"   - Total Records: {len(df):,}")
print(f"   - Unique Users: {df['user_id'].nunique():,}")
print(f"   - Countries: {df['country'].nunique()}")
print(f"   - Date Range: {df['date'].min()} to {df['date'].max()}")

# 1. Summary by country
print("\n🌍 Country Summary:")
country_summary = df.groupby('country').agg({
    'data_mb': 'mean',
    'call_minutes': 'mean',
    'sms_count': 'mean',
    'revenue_usd': 'mean'
}).round(2)

print(country_summary)

# 2. Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('African Mobile Usage Dashboard', fontsize=16, fontweight='bold')

# Plot 1: Average data usage by country
ax1 = axes[0, 0]
country_data = df.groupby('country')['data_mb'].mean().sort_values(ascending=True)
bars = ax1.barh(country_data.index, country_data.values, color='coral')
ax1.set_xlabel('Average Data Usage (MB)')
ax1.set_title('Average Data Usage by Country')
for bar, val in zip(bars, country_data.values):
    ax1.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2, 
             f'{val:.1f}MB', ha='left', va='center')

# Plot 2: Usage by age group
ax2 = axes[0, 1]
df['age_group'] = pd.cut(df['age'], bins=[18, 30, 45, 65], labels=['18-30', '30-45', '45-65'])
age_metrics = df.groupby('age_group')[['data_mb', 'call_minutes']].mean()

x = np.arange(len(age_metrics.index))
width = 0.35
ax2.bar(x - width/2, age_metrics['data_mb'], width, label='Data (MB)', color='teal')
ax2.bar(x + width/2, age_metrics['call_minutes'] / 5, width, label='Call Minutes/5', color='orange')
ax2.set_xlabel('Age Group')
ax2.set_ylabel('Data Usage (MB)')
ax2.set_title('Mobile Usage by Age Group')
ax2.set_xticks(x)
ax2.set_xticklabels(age_metrics.index)
ax2.legend()

# Plot 3: Revenue by provider
ax3 = axes[1, 0]
provider_revenue = df.groupby('provider')['revenue_usd'].mean().sort_values(ascending=False)
ax3.bar(provider_revenue.index[:10], provider_revenue.values[:10], color='purple')
ax3.set_xlabel('Provider')
ax3.set_ylabel('Average Revenue (USD)')
ax3.set_title('Top 10 Providers by Revenue')
ax3.tick_params(axis='x', rotation=45)

# Plot 4: Subscription type comparison
ax4 = axes[1, 1]
subscription_usage = df.groupby('subscription_type')[['data_mb', 'call_minutes', 'revenue_usd']].mean()
subscription_usage.plot(kind='bar', ax=ax4, rot=0)
ax4.set_title('Usage by Subscription Type')
ax4.set_ylabel('Average Value')
ax4.legend(['Data (MB)', 'Call Minutes', 'Revenue (USD)'])

plt.tight_layout()
plt.savefig('../data/africa_mobile_dashboard.png', dpi=300, bbox_inches='tight')
print("✅ Dashboard saved as 'africa_mobile_dashboard.png'")

# 3. Key insights
print("\n💡 KEY INSIGHTS:")
print("-" * 40)

# Top country by data usage
top_data_country = country_data.idxmax()
print(f"🔹 Highest data usage: {top_data_country} ({country_data.max():.1f}MB avg)")

# Most profitable country
top_revenue_country = df.groupby('country')['revenue_usd'].mean().idxmax()
print(f"🔹 Highest revenue per user: {top_revenue_country}")

# Age group insights
most_data_age = age_metrics['data_mb'].idxmax()
print(f"🔹 Most data usage age group: {most_data_age}")

# Gender split
gender_usage = df.groupby('gender')['data_mb'].mean()
print(f"🔹 Data usage: Male {gender_usage.get('Male', 0):.1f}MB vs Female {gender_usage.get('Female', 0):.1f}MB")

print("\n" + "=" * 60)
print("✅ Analysis complete!")
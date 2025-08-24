# Solar Oven Efficiency Analysis
# Sustainable Tech Approach - Giulia Torrentia
# Analyzing different solar oven designs and their cooking efficiency
# Date: August 2025

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

print("🌞 Solar Oven Efficiency Analysis - Sustainable Tech 🌞")
print("=" * 50)

# Simulate solar oven data (in real scenario, this would be measured data)
# Three types: Box, Parabolic, Funnel designs

# Generate time series data for a cooking session
time_points = np.arange(0, 120, 5)  # 2 hours, every 5 minutes
solar_radiation = 800 + 200 * np.sin(np.pi * time_points / 60) * np.random.normal(1, 0.1, len(time_points))

# Different oven types with different efficiency curves
def generate_temperature_data(oven_type, time_points, solar_radiation):
    """Generate realistic temperature data for different oven types"""
    base_temp = 25  # Ambient temperature
    
    if oven_type == "Box":
        # Box ovens: steady heat retention, slower warmup
        efficiency = 0.65
        thermal_mass = 0.8
    elif oven_type == "Parabolic":
        # Parabolic: high peak temperature, faster response
        efficiency = 0.85
        thermal_mass = 0.4
    else:  # Funnel
        # Funnel: moderate efficiency, good heat retention
        efficiency = 0.75
        thermal_mass = 0.6
    
    temperatures = []
    current_temp = base_temp
    
    for i, radiation in enumerate(solar_radiation):
        # Temperature increase based on solar radiation and oven efficiency
        temp_increase = (radiation * efficiency / 1000) * (1 - thermal_mass + thermal_mass * i/len(time_points))
        current_temp = base_temp + temp_increase + np.random.normal(0, 3)
        temperatures.append(max(current_temp, base_temp))
    
    return temperatures

# Generate data for three oven types
oven_types = ["Box", "Parabolic", "Funnel"]
data = []

for oven_type in oven_types:
    temperatures = generate_temperature_data(oven_type, time_points, solar_radiation)
    for i, (time, temp, radiation) in enumerate(zip(time_points, temperatures, solar_radiation)):
        data.append({
            'Time_Minutes': time,
            'Temperature_C': temp,
            'Solar_Radiation': radiation,
            'Oven_Type': oven_type,
            'Cooking_Phase': 'Warmup' if time < 30 else 'Cooking' if time < 90 else 'Maintenance'
        })

df = pd.DataFrame(data)

print(f"📊 Dataset created: {len(df)} measurements")
print(f"🔥 Oven types: {', '.join(oven_types)}")
print(f"⏱️ Duration: {max(time_points)} minutes")
print()

# Basic statistics
print("📈 TEMPERATURE STATISTICS BY OVEN TYPE")
print("=" * 40)
temp_stats = df.groupby('Oven_Type')['Temperature_C'].agg(['mean', 'max', 'std']).round(2)
print(temp_stats)
print()

# Efficiency analysis
print("⚡ EFFICIENCY ANALYSIS")
print("=" * 25)
efficiency_analysis = df.groupby('Oven_Type').agg({
    'Temperature_C': ['mean', 'max'],
    'Solar_Radiation': 'mean'
}).round(2)

efficiency_analysis.columns = ['Avg_Temp', 'Max_Temp', 'Avg_Solar_Input']
efficiency_analysis['Efficiency_Ratio'] = (efficiency_analysis['Avg_Temp'] / efficiency_analysis['Avg_Solar_Input'] * 100).round(2)
print(efficiency_analysis)
print()

# Cooking time analysis
cooking_threshold = 80  # Temperature needed for effective cooking
print(f"🍳 TIME TO COOKING TEMPERATURE ({cooking_threshold}°C)")
print("=" * 35)

for oven_type in oven_types:
    oven_data = df[df['Oven_Type'] == oven_type]
    cooking_time = oven_data[oven_data['Temperature_C'] >= cooking_threshold]['Time_Minutes'].min()
    if pd.isna(cooking_time):
        print(f"{oven_type}: Never reached cooking temperature")
    else:
        print(f"{oven_type}: {cooking_time} minutes")
print()

# Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('🌞 Solar Oven Performance Analysis\nSustainable Cooking Technology 🌞', fontsize=16, fontweight='bold')

# 1. Temperature curves over time
axes[0,0].set_title('Temperature Evolution by Oven Type')
for oven_type in oven_types:
    oven_data = df[df['Oven_Type'] == oven_type]
    axes[0,0].plot(oven_data['Time_Minutes'], oven_data['Temperature_C'], 
                   label=f'{oven_type} Oven', linewidth=2, marker='o', markersize=3)
axes[0,0].axhline(y=cooking_threshold, color='red', linestyle='--', alpha=0.7, label='Cooking Threshold')
axes[0,0].set_xlabel('Time (minutes)')
axes[0,0].set_ylabel('Temperature (°C)')
axes[0,0].legend()
axes[0,0].grid(True, alpha=0.3)

# 2. Box plot comparison
axes[0,1].set_title('Temperature Distribution by Oven Type')
df.boxplot(column='Temperature_C', by='Oven_Type', ax=axes[0,1])
axes[0,1].set_xlabel('Oven Type')
axes[0,1].set_ylabel('Temperature (°C)')

# 3. Efficiency scatter plot
axes[1,0].set_title('Solar Radiation vs Temperature Response')
for oven_type in oven_types:
    oven_data = df[df['Oven_Type'] == oven_type]
    axes[1,0].scatter(oven_data['Solar_Radiation'], oven_data['Temperature_C'], 
                      label=f'{oven_type}', alpha=0.6, s=30)
axes[1,0].set_xlabel('Solar Radiation (W/m²)')
axes[1,0].set_ylabel('Temperature (°C)')
axes[1,0].legend()
axes[1,0].grid(True, alpha=0.3)

# 4. Cooking phases comparison
axes[1,1].set_title('Average Temperature by Cooking Phase')
phase_temp = df.groupby(['Oven_Type', 'Cooking_Phase'])['Temperature_C'].mean().unstack()
phase_temp.plot(kind='bar', ax=axes[1,1], width=0.8)
axes[1,1].set_xlabel('Oven Type')
axes[1,1].set_ylabel('Average Temperature (°C)')
axes[1,1].legend(title='Cooking Phase')
axes[1,1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

# Sustainability insights
print("🌱 SUSTAINABILITY INSIGHTS")
print("=" * 30)
print("• Box ovens: Best for slow cooking, excellent heat retention")
print("• Parabolic ovens: Highest temperatures, best for quick cooking")
print("• Funnel ovens: Good balance, easiest to build with recycled materials")
print()
print("💡 COOKING RECOMMENDATIONS")
print("=" * 25)
print("• Bread/Rice: Box oven (steady temperature)")
print("• Meat/Vegetables: Parabolic oven (high heat)")
print("• Stews/Soups: Funnel oven (moderate, consistent)")
print()
print("🌍 ENVIRONMENTAL IMPACT")
print("=" * 25)
print("• Zero CO2 emissions during cooking")
print("• Reduces dependence on fossil fuels")
print("• Can be built with recycled materials")
print("• Ideal for off-grid communities")
print()

# Save analysis results
results_summary = {
    'Analysis_Date': datetime.now().strftime('%Y-%m-%d'),
    'Analyst': 'Giulia Torrentia',
    'Methodology': 'Comparative analysis of solar oven designs',
    'Best_Overall': 'Parabolic (highest efficiency)',
    'Most_Practical': 'Funnel (easy build + good performance)',
    'Best_Retention': 'Box (steady cooking temperature)'
}

print("🌞 Topic: Sustainable technology meets data science 🌞")
print("Solar Oven Selection Guide: It Depends on Your Needs!")



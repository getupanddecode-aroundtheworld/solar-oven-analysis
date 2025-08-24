# 🌞 Solar Oven Selection Guide: It Depends on Your Needs!
# Author: Giulia Torrentia
# Date: August 2025
# Description: Analyzing different solar oven designs for cooking efficiency

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Set style for better visualizations
plt.style.use('default')
sns.set_palette("husl")

print("🌞 Solar Oven Efficiency Analysis - Sustainable Tech")
print("=" * 50)

# Generate time series data for a cooking session
time_points = np.arange(0, 120, 5)  # 2 hours, every 5 minutes

# Solar radiation pattern (realistic midday curve)
peak_radiation = 1000  # W/m² at solar noon
solar_radiation = []
for t in time_points:
    # Bell curve for sun position
    radiation = peak_radiation * np.exp(-((t-60)**2)/(2*30**2)) + np.random.normal(0, 50)
    radiation = max(radiation, 200)  # Minimum radiation
    solar_radiation.append(radiation)

def generate_temperature_data(oven_type, time_points, solar_radiation):
    """Generate realistic temperature data for different oven types"""
    ambient_temp = 25  # Starting temperature
    
    # Realistic oven parameters
    if oven_type == "Box":
        max_efficiency = 0.4  # Box ovens reach 100-120°C
        heat_retention = 0.95
        warmup_speed = 0.02
    elif oven_type == "Parabolic":
        max_efficiency = 0.6  # Parabolic can reach 150-200°C  
        heat_retention = 0.85
        warmup_speed = 0.05
    else:  # Funnel
        max_efficiency = 0.45  # Funnel ovens reach 90-130°C
        heat_retention = 0.90
        warmup_speed = 0.03
    
    temperatures = [ambient_temp]
    current_temp = ambient_temp
    
    for i, radiation in enumerate(solar_radiation[1:], 1):
        # Heat gain from solar radiation
        heat_gain = (radiation / 1000) * max_efficiency * 80 * warmup_speed * (1 + i/50)
        
        # Heat loss to environment
        heat_loss = (current_temp - ambient_temp) * (1 - heat_retention) * 0.1
        
        # New temperature
        current_temp = current_temp + heat_gain - heat_loss + np.random.normal(0, 2)
        current_temp = max(current_temp, ambient_temp)  # Never below ambient
        
        temperatures.append(current_temp)
    
    return temperatures

def main():
    """Main analysis function"""
    # Create dataset
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
    
    # Statistics
    print("\n📈 TEMPERATURE STATISTICS BY OVEN TYPE")
    print("=" * 40)
    
    for oven_type in oven_types:
        oven_data = df[df['Oven_Type'] == oven_type]['Temperature_C']
        print(f"\n{oven_type} Oven:")
        print(f"  Average: {oven_data.mean():.1f}°C")
        print(f"  Maximum: {oven_data.max():.1f}°C")
        print(f"  Std Dev: {oven_data.std():.1f}°C")
    
    # Visualizations
    create_visualizations(df, oven_types)
    
    return df

def create_visualizations(df, oven_types):
    """Create all visualizations"""
    
    # 1. Temperature Evolution
    plt.figure(figsize=(12, 6))
    plt.title('Temperature Evolution by Solar Oven Type', fontsize=14)
    
    for oven_type in oven_types:
        oven_data = df[df['Oven_Type'] == oven_type]
        plt.plot(oven_data['Time_Minutes'], oven_data['Temperature_C'], 
                 label=f'{oven_type} Oven', linewidth=2, marker='o', markersize=3)
    
    plt.axhline(y=60, color='red', linestyle='--', alpha=0.7, 
                label='Cooking Threshold (60°C)')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    
    # 2. Box Plot Distribution
    plt.figure(figsize=(10, 6))
    box_data = []
    labels = []
    for oven_type in oven_types:
        temps = df[df['Oven_Type'] == oven_type]['Temperature_C'].tolist()
        box_data.append(temps)
        labels.append(oven_type)
    
    plt.boxplot(box_data, labels=labels)
    plt.title('Temperature Distribution by Oven Type')
    plt.xlabel('Oven Type')
    plt.ylabel('Temperature (°C)')
    plt.grid(True, alpha=0.3)
    plt.show()
    
    # 3. Solar Radiation Scatter
    plt.figure(figsize=(10, 6))
    colors = ['red', 'blue', 'green']
    
    for i, oven_type in enumerate(oven_types):
        oven_data = df[df['Oven_Type'] == oven_type]
        plt.scatter(oven_data['Solar_Radiation'], oven_data['Temperature_C'], 
                    label=oven_type, alpha=0.6, s=40, color=colors[i])
    
    plt.title('Solar Radiation vs Temperature Response')
    plt.xlabel('Solar Radiation (W/m²)')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    
    # 4. Cooking Phases Bar Chart
    plt.figure(figsize=(12, 6))
    phases = ['Warmup', 'Cooking', 'Maintenance']
    
    data_for_plot = []
    for oven_type in oven_types:
        oven_temps = []
        for phase in phases:
            avg_temp = df[(df['Oven_Type'] == oven_type) & 
                         (df['Cooking_Phase'] == phase)]['Temperature_C'].mean()
            oven_temps.append(avg_temp)
        data_for_plot.append(oven_temps)
    
    x = np.arange(len(oven_types))
    width = 0.25
    
    for i, phase in enumerate(phases):
        temps = [data_for_plot[j][i] for j in range(len(oven_types))]
        plt.bar(x + i*width, temps, width, label=phase, alpha=0.8)
    
    plt.title('Average Temperature by Cooking Phase')
    plt.xlabel('Oven Type')
    plt.ylabel('Temperature (°C)')
    plt.xticks(x + width, oven_types)
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')
    plt.show()

if __name__ == "__main__":
    df = main()
    print("\n🌱 Analysis completed!")
    print("💡 Conclusion: The best solar oven depends on your cooking needs!")
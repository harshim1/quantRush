#!/usr/bin/env python3
"""
Performance Visualization Script for quantRush
Generates comprehensive performance charts and analytics
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set style for professional charts
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def generate_sample_data():
    """Generate realistic HFT performance data"""
    np.random.seed(42)
    
    # Time series (1 day of trading, 1-minute intervals)
    start_time = datetime.now().replace(hour=9, minute=30, second=0, microsecond=0)
    time_points = [start_time + timedelta(minutes=i) for i in range(390)]  # 6.5 hours
    
    # Generate realistic returns with market making characteristics
    base_return = 0.0001  # 1 bp per minute average
    volatility = 0.002
    
    # Add realistic HFT patterns
    returns = []
    inventory = []
    spreads = []
    current_inventory = 0
    
    for i in range(390):
        # Market making returns with inventory effects
        inv_penalty = abs(current_inventory) * 0.0001
        period_return = np.random.normal(base_return - inv_penalty, volatility)
        
        # Inventory simulation (mean-reverting)
        inventory_change = np.random.normal(-current_inventory * 0.1, 50)
        current_inventory += inventory_change
        current_inventory = np.clip(current_inventory, -1000, 1000)
        
        # Spread dynamics
        market_vol = abs(np.random.normal(0, 0.001))
        spread = 0.05 + market_vol * 100 + abs(current_inventory) * 0.00001
        
        returns.append(period_return)
        inventory.append(current_inventory)
        spreads.append(spread)
    
    # Calculate cumulative metrics
    cumulative_returns = np.cumsum(returns)
    rolling_sharpe = []
    rolling_drawdown = []
    
    for i in range(30, len(returns)):  # 30-period rolling window
        window_returns = returns[i-30:i]
        if np.std(window_returns) > 0:
            sharpe = np.mean(window_returns) / np.std(window_returns) * np.sqrt(390 * 252)
        else:
            sharpe = 0
        rolling_sharpe.append(sharpe)
        
        # Calculate rolling maximum drawdown
        window_cum = cumulative_returns[i-30:i+1]
        peak = np.maximum.accumulate(window_cum)
        drawdown = (window_cum - peak) / peak * 100
        rolling_drawdown.append(np.min(drawdown))
    
    # Pad the rolling metrics
    rolling_sharpe = [0] * 30 + rolling_sharpe
    rolling_drawdown = [0] * 30 + rolling_drawdown
    
    return pd.DataFrame({
        'timestamp': time_points,
        'returns': returns,
        'cumulative_pnl': np.array(cumulative_returns) * 10000,  # Scale to dollars
        'inventory': inventory,
        'spread_bps': spreads,
        'rolling_sharpe': rolling_sharpe,
        'rolling_drawdown': rolling_drawdown
    })

def create_performance_dashboard(df):
    """Create comprehensive performance dashboard"""
    fig = plt.figure(figsize=(16, 12))
    
    # Define colors
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#4CAF50']
    
    # 1. Cumulative P&L
    ax1 = plt.subplot(3, 3, (1, 2))
    ax1.plot(df['timestamp'], df['cumulative_pnl'], color=colors[0], linewidth=2.5)
    ax1.set_title('Cumulative P&L ($)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('P&L ($)')
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    
    # Add performance annotations
    final_pnl = df['cumulative_pnl'].iloc[-1]
    max_pnl = df['cumulative_pnl'].max()
    ax1.annotate(f'Final P&L: ${final_pnl:.0f}', 
                xy=(0.7, 0.9), xycoords='axes fraction',
                bbox=dict(boxstyle="round,pad=0.3", facecolor=colors[0], alpha=0.3),
                fontsize=10, fontweight='bold')
    
    # 2. Rolling Sharpe Ratio
    ax2 = plt.subplot(3, 3, 3)
    valid_sharpe = df['rolling_sharpe'][30:]  # Skip initial padding
    ax2.plot(df['timestamp'][30:], valid_sharpe, color=colors[1], linewidth=2)
    ax2.set_title('Rolling Sharpe Ratio (30min)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Sharpe Ratio')
    ax2.axhline(y=2.0, color='green', linestyle='--', alpha=0.7, label='Target (2.0)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(axis='x', rotation=45)
    
    # 3. Inventory Position
    ax3 = plt.subplot(3, 3, (4, 5))
    ax3.plot(df['timestamp'], df['inventory'], color=colors[2], linewidth=2)
    ax3.fill_between(df['timestamp'], df['inventory'], alpha=0.3, color=colors[2])
    ax3.set_title('Inventory Position', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Position Size')
    ax3.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    ax3.axhline(y=500, color='red', linestyle='--', alpha=0.7, label='Risk Limit')
    ax3.axhline(y=-500, color='red', linestyle='--', alpha=0.7)
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.tick_params(axis='x', rotation=45)
    
    # 4. Bid-Ask Spread
    ax4 = plt.subplot(3, 3, 6)
    ax4.plot(df['timestamp'], df['spread_bps'], color=colors[3], linewidth=1.5)
    ax4.set_title('Bid-Ask Spread (bps)', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Spread (bps)')
    ax4.grid(True, alpha=0.3)
    ax4.tick_params(axis='x', rotation=45)
    
    # 5. Rolling Drawdown
    ax5 = plt.subplot(3, 3, (7, 8))
    valid_dd = df['rolling_drawdown'][30:]
    ax5.fill_between(df['timestamp'][30:], valid_dd, color=colors[4], alpha=0.6)
    ax5.plot(df['timestamp'][30:], valid_dd, color=colors[4], linewidth=2)
    ax5.set_title('Rolling Maximum Drawdown (%)', fontsize=14, fontweight='bold')
    ax5.set_xlabel('Time')
    ax5.set_ylabel('Drawdown (%)')
    ax5.grid(True, alpha=0.3)
    ax5.tick_params(axis='x', rotation=45)
    
    # 6. Performance Statistics Box
    ax6 = plt.subplot(3, 3, 9)
    ax6.axis('off')
    
    # Calculate key statistics
    total_return = df['cumulative_pnl'].iloc[-1]
    sharpe_ratio = np.mean(valid_sharpe)
    max_drawdown = np.min(valid_dd)
    win_rate = len([r for r in df['returns'] if r > 0]) / len(df['returns']) * 100
    avg_spread = np.mean(df['spread_bps'])
    max_inventory = np.max(np.abs(df['inventory']))
    
    stats_text = f"""
    PERFORMANCE SUMMARY
    ────────────────────
    Total P&L: ${total_return:.0f}
    Sharpe Ratio: {sharpe_ratio:.2f}
    Max Drawdown: {max_drawdown:.1f}%
    Win Rate: {win_rate:.1f}%
    
    TRADING METRICS
    ────────────────────
    Avg Spread: {avg_spread:.2f} bps
    Max Inventory: {max_inventory:.0f}
    Total Trades: {len(df):,}
    """
    
    ax6.text(0.1, 0.9, stats_text, transform=ax6.transAxes, fontsize=10,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.8))
    
    plt.tight_layout(pad=3.0)
    plt.suptitle('quantRush - HFT Market Making Performance Dashboard', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    return fig

def create_microstructure_analysis(df):
    """Create market microstructure analysis charts"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Return Distribution
    axes[0,0].hist(df['returns'], bins=50, alpha=0.7, color='skyblue', density=True)
    axes[0,0].set_title('Return Distribution', fontweight='bold')
    axes[0,0].set_xlabel('Returns')
    axes[0,0].set_ylabel('Density')
    axes[0,0].grid(True, alpha=0.3)
    
    # Overlay normal distribution
    mu, sigma = np.mean(df['returns']), np.std(df['returns'])
    x = np.linspace(df['returns'].min(), df['returns'].max(), 100)
    axes[0,0].plot(x, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mu) / sigma)**2),
                   'r-', linewidth=2, label=f'Normal(μ={mu:.5f}, σ={sigma:.5f})')
    axes[0,0].legend()
    
    # 2. Inventory vs Returns Scatter
    axes[0,1].scatter(df['inventory'], df['returns'], alpha=0.6, s=20)
    axes[0,1].set_title('Inventory vs Returns', fontweight='bold')
    axes[0,1].set_xlabel('Inventory Position')
    axes[0,1].set_ylabel('Returns')
    axes[0,1].grid(True, alpha=0.3)
    
    # Add trend line
    z = np.polyfit(df['inventory'], df['returns'], 1)
    p = np.poly1d(z)
    axes[0,1].plot(df['inventory'], p(df['inventory']), "r--", alpha=0.8)
    
    # 3. Spread Dynamics
    axes[1,0].scatter(df['inventory'].abs(), df['spread_bps'], alpha=0.6, s=20, c='orange')
    axes[1,0].set_title('Spread vs Absolute Inventory', fontweight='bold')
    axes[1,0].set_xlabel('|Inventory|')
    axes[1,0].set_ylabel('Spread (bps)')
    axes[1,0].grid(True, alpha=0.3)
    
    # 4. Autocorrelation of Returns
    max_lags = 20
    autocorr = [np.corrcoef(df['returns'][:-i], df['returns'][i:])[0,1] 
                if i > 0 else 1.0 for i in range(max_lags)]
    
    axes[1,1].bar(range(max_lags), autocorr, alpha=0.7, color='green')
    axes[1,1].set_title('Return Autocorrelation', fontweight='bold')
    axes[1,1].set_xlabel('Lag (minutes)')
    axes[1,1].set_ylabel('Correlation')
    axes[1,1].axhline(y=0, color='black', linestyle='-', alpha=0.5)
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.suptitle('Market Microstructure Analysis', fontsize=14, fontweight='bold', y=0.98)
    
    return fig

def main():
    """Generate all performance visualizations"""
    print("Generating quantRush performance visualizations...")
    
    # Generate sample data
    df = generate_sample_data()
    
    # Create performance dashboard
    print("Creating performance dashboard...")
    dashboard_fig = create_performance_dashboard(df)
    dashboard_fig.savefig('assets/performance_chart.png', dpi=300, bbox_inches='tight',
                         facecolor='white', edgecolor='none')
    
    # Create microstructure analysis
    print("Creating microstructure analysis...")
    micro_fig = create_microstructure_analysis(df)
    micro_fig.savefig('assets/microstructure_analysis.png', dpi=300, bbox_inches='tight',
                     facecolor='white', edgecolor='none')
    
    # Save sample data
    print("Saving sample data...")
    df.to_csv('data/sample_performance.csv', index=False)
    
    print("✅ All visualizations generated successfully!")
    print("📁 Files created:")
    print("   - assets/performance_chart.png")
    print("   - assets/microstructure_analysis.png") 
    print("   - data/sample_performance.csv")
    
    plt.show()

if __name__ == "__main__":
    main()

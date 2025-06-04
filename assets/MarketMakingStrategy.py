#!/usr/bin/env python3
"""
Market Making Strategy Visualization
Creates professional diagrams explaining the market making process
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_order_book_visualization():
    """Create a visual representation of the limit order book"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 10))
    
    # Order Book Visualization
    ax1.set_xlim(0, 10)
    ax1.set_ylim(95, 105)
    
    # Sample order book data
    bid_prices = [99.95, 99.94, 99.93, 99.92, 99.91, 99.90]
    bid_quantities = [100, 250, 150, 300, 200, 180]
    ask_prices = [100.05, 100.06, 100.07, 100.08, 100.09, 100.10]
    ask_quantities = [120, 200, 180, 250, 150, 220]
    
    # Plot bid side (left side, green)
    for i, (price, qty) in enumerate(zip(bid_prices, bid_quantities)):
        width = qty / 50  # Scale for visualization
        rect = patches.Rectangle((5-width, price-0.005), width, 0.01, 
                               facecolor='lightgreen', edgecolor='darkgreen', alpha=0.8)
        ax1.add_patch(rect)
        ax1.text(4.8, price, f'${price:.2f}', ha='right', va='center', fontweight='bold')
        ax1.text(5-width/2, price, f'{qty}', ha='center', va='center', fontsize=8)
    
    # Plot ask side (right side, red)
    for i, (price, qty) in enumerate(zip(ask_prices, ask_quantities)):
        width = qty / 50  # Scale for visualization
        rect = patches.Rectangle((5, price-0.005), width, 0.01, 
                               facecolor='lightcoral', edgecolor='darkred', alpha=0.8)
        ax1.add_patch(rect)
        ax1.text(5.2, price, f'${price:.2f}', ha='left', va='center', fontweight='bold')
        ax1.text(5+width/2, price, f'{qty}', ha='center', va='center', fontsize=8)
    
    # Mid price line
    mid_price = (bid_prices[0] + ask_prices[0]) / 2
    ax1.axhline(y=mid_price, color='blue', linestyle='--', linewidth=2, alpha=0.7)
    ax1.text(5, mid_price+0.03, f'Mid: ${mid_price:.2f}', ha='center', va='bottom',
             bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.8),
             fontweight='bold')
    
    # Market maker quotes
    mm_bid = 99.96
    mm_ask = 100.04
    ax1.axhline(y=mm_bid, color='orange', linewidth=3, alpha=0.8)
    ax1.axhline(y=mm_ask, color='orange', linewidth=3, alpha=0.8)
    ax1.text(1, mm_bid, 'MM Bid: $99.96', ha='left', va='center',
             bbox=dict(boxstyle="round,pad=0.3", facecolor='orange', alpha=0.6),
             fontweight='bold')
    ax1.text(1, mm_ask, 'MM Ask: $100.04', ha='left', va='center',
             bbox=dict(boxstyle="round,pad=0.3", facecolor='orange', alpha=0.6),
             fontweight='bold')
    
    ax1.set_title('Limit Order Book with Market Maker Quotes', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Order Quantity →')
    ax1.set_ylabel('Price ($)')
    ax1.text(2.5, 104, 'ASK SIDE', ha='center', va='center', fontsize=12, fontweight='bold', color='darkred')
    ax1.text(2.5, 96, 'BID SIDE', ha='center', va='center', fontsize=12, fontweight='bold', color='darkgreen')
    ax1.grid(True, alpha=0.3)
    
    # Strategy Flow Diagram
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    
    # Define boxes for strategy flow
    boxes = [
        {'xy': (5, 9), 'width': 3, 'height': 0.8, 'text': 'Market Data\nFeed', 'color': 'lightblue'},
        {'xy': (1.5, 7.5), 'width': 2.5, 'height': 0.8, 'text': 'Order Book\nAnalysis', 'color': 'lightgreen'},
        {'xy': (6, 7.5), 'width': 2.5, 'height': 0.8, 'text': 'Inventory\nManagement', 'color': 'lightyellow'},
        {'xy': (5, 6), 'width': 3, 'height': 0.8, 'text': 'Pricing Engine\n(Spread Calculation)', 'color': 'lightcoral'},
        {'xy': (1.5, 4.5), 'width': 2.5, 'height': 0.8, 'text': 'Generate\nBid Orders', 'color': 'lightgreen'},
        {'xy': (6, 4.5), 'width': 2.5, 'height': 0.8, 'text': 'Generate\nAsk Orders', 'color': 'lightcoral'},
        {'xy': (5, 3), 'width': 3, 'height': 0.8, 'text': 'Order Management\nSystem', 'color': 'orange'},
        {'xy': (5, 1.5), 'width': 3, 'height': 0.8, 'text': 'Exchange\nMatching Engine', 'color': 'lightgray'},
    ]
    
    # Draw boxes
    for box in boxes:
        fancy_box = FancyBboxPatch(
            (box['xy'][0] - box['width']/2, box['xy'][1] - box['height']/2),
            box['width'], box['height'],
            boxstyle="round,pad=0.1",
            facecolor=box['color'],
            edgecolor='black',
            linewidth=1.5
        )
        ax2.add_patch(fancy_box)
        ax2.text(box['xy'][0], box['xy'][1], box['text'], 
                ha='center', va='center', fontweight='bold', fontsize=10)
    
    # Draw arrows
    arrows = [
        ((5, 8.6), (2.75, 7.9)),  # Market Data to Order Book Analysis
        ((5, 8.6), (7.25, 7.9)),  # Market Data to Inventory Management
        ((2.75, 7.1), (5, 6.4)),  # Order Book to Pricing
        ((7.25, 7.1), (5, 6.4)),  # Inventory to Pricing
        ((5, 5.6), (2.75, 4.9)),  # Pricing to Bid Orders
        ((5, 5.6), (7.25, 4.9)),  # Pricing to Ask Orders
        ((2.75, 4.1), (5, 3.4)),  # Bid Orders to OMS
        ((7.25, 4.1), (5, 3.4)),  # Ask Orders to OMS
        ((5, 2.6), (5, 1.9)),     # OMS to Exchange
    ]
    
    for start, end in arrows:
        arrow = ConnectionPatch(start, end, "data", "data",
                              arrowstyle="->", shrinkA=5, shrinkB=5,
                              mutation_scale=20, fc="black", lw=1.5)
        ax2.add_patch(arrow)
    
    ax2.set_title('Market Making Strategy Flow', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    return fig

def create_pnl_attribution_chart():
    """Create P&L attribution analysis"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. P&L Components
    components = ['Spread Capture', 'Inventory Risk', 'Market Impact', 'Fees', 'Slippage']
    values = [1250, -320, -180, -150, -75]
    colors = ['green', 'red', 'orange', 'purple', 'brown']
    
    bars = ax1.bar(components, values, color=colors, alpha=0.7)
    ax1.set_title('P&L Attribution by Component ($)', fontweight='bold')
    ax1.set_ylabel('P&L ($)')
    ax1.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    ax1.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + (10 if height > 0 else -30),
                f'${value}', ha='center', va='bottom' if height > 0 else 'top', fontweight='bold')
    
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # 2. Risk Metrics Over Time
    time_hours = np.arange(0, 6.5, 0.1)
    var_95 = 100 + 50 * np.sin(time_hours * 0.5) + np.random.normal(0, 10, len(time_hours))
    expected_shortfall = var_95 * 1.3
    
    ax2.plot(time_hours, var_95, label='VaR (95%)', linewidth=2, color='red')
    ax2.plot(time_hours, expected_shortfall, label='Expected Shortfall', linewidth=2, color='darkred')
    ax2.fill_between(time_hours, 0, var_95, alpha=0.3, color='red')
    ax2.set_title('Intraday Risk Metrics', fontweight='bold')
    ax2.set_xlabel('Trading Hours')
    ax2.set_ylabel('Risk ($)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Inventory Turnover
    inventory_levels = np.random.normal(0, 200, 100)
    inventory_time = np.linspace(0, 6.5, 100)
    
    ax3.plot(inventory_time, inventory_levels, color='blue', linewidth=1.5)
    ax3.fill_between(inventory_time, inventory_levels, alpha=0.3, color='blue')
    ax3.axhline(y=0, color='black', linestyle='--', alpha=0.7)
    ax3.axhline(y=500, color='red', linestyle='--', alpha=0.7, label='Risk Limit')
    ax3.axhline(y=-500, color='red', linestyle='--', alpha=0.7)
    ax3.set_title('Inventory Management', fontweight='bold')
    ax3.set_xlabel('Trading Hours')
    ax3.set_ylabel('Position Size')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Spread Analysis
    market_vol = np.random.exponential(0.05, 1000)
    spreads = 0.05 + market_vol * 2 + np.random.normal(0, 0.01, 1000)
    
    ax4.hist2d(market_vol, spreads, bins=30, cmap='Blues', alpha=0.8)
    ax4.set_title('Spread vs Market Volatility', fontweight='bold')
    ax4.set_xlabel('Market Volatility')
    ax4.set_ylabel('Bid-Ask Spread (bps)')
    
    # Add trend line
    z = np.polyfit(market_vol, spreads, 1)
    p = np.poly1d(z)
    vol_range = np.linspace(market_vol.min(), market_vol.max(), 100)
    ax4.plot(vol_range, p(vol_range), "r--", linewidth=2, alpha=0.8, label='Trend')
    ax4.legend()
    
    plt.tight_layout()
    plt.suptitle('Market Making Performance Analytics', fontsize=16, fontweight='bold', y=0.98)
    return fig

def create_architecture_diagram():
    """Create system architecture diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Define architecture components
    components = [
        # Market Data Layer
        {'xy': (2, 9), 'width': 2.5, 'height': 0.8, 'text': 'Market Data\nFeed Handler', 'color': 'lightblue'},
        {'xy': (6, 9), 'width': 2.5, 'height': 0.8, 'text': 'Order Book\nProcessor', 'color': 'lightblue'},
        {'xy': (10, 9), 'width': 2.5, 'height': 0.8, 'text': 'Risk Monitor', 'color': 'lightcoral'},
        
        # Strategy Layer
        {'xy': (2, 7), 'width': 2.5, 'height': 0.8, 'text': 'Market Making\nStrategy', 'color': 'lightgreen'},
        {'xy': (6, 7), 'width': 2.5, 'height': 0.8, 'text': 'Pricing Engine', 'color': 'lightgreen'},
        {'xy': (10, 7), 'width': 2.5, 'height': 0.8, 'text': 'Portfolio\nManager', 'color': 'lightgreen'},
        
        # Execution Layer
        {'xy': (2, 5), 'width': 2.5, 'height': 0.8, 'text': 'Order\nGenerator', 'color': 'lightyellow'},
        {'xy': (6, 5), 'width': 2.5, 'height': 0.8, 'text': 'Order Management\nSystem (OMS)', 'color': 'lightyellow'},
        {'xy': (10, 5), 'width': 2.5, 'height': 0.8, 'text': 'Execution\nAlgorithms', 'color': 'lightyellow'},
        
        # Infrastructure Layer
        {'xy': (4, 3), 'width': 2.5, 'height': 0.8, 'text': 'Message Queue\n(Low Latency)', 'color': 'lightgray'},
        {'xy': (8, 3), 'width': 2.5, 'height': 0.8, 'text': 'Database\n(Time Series)', 'color': 'lightgray'},
        
        # Exchange Interface
        {'xy': (6, 1), 'width': 3, 'height': 0.8, 'text': 'Exchange Gateway\n(FIX/Binary Protocol)', 'color': 'orange'},
    ]
    
    # Draw components
    for comp in components:
        fancy_box = FancyBboxPatch(
            (comp['xy'][0] - comp['width']/2, comp['xy'][1] - comp['height']/2),
            comp['width'], comp['height'],
            boxstyle="round,pad=0.1",
            facecolor=comp['color'],
            edgecolor='black',
            linewidth=1.5
        )
        ax.add_patch(fancy_box)
        ax.text(comp['xy'][0], comp['xy'][1], comp['text'], 
                ha='center', va='center', fontweight='bold', fontsize=9)
    
    # Draw connections
    connections = [
        # Market Data Flow
        ((2, 8.6), (2, 7.4)),   # Feed Handler to Strategy
        ((6, 8.6), (6, 7.4)),   # Order Book to Pricing
        ((10, 8.6), (10, 7.4)), # Risk Monitor to Portfolio
        
        # Strategy to Execution
        ((2, 6.6), (2, 5.4)),   # Strategy to Order Gen
        ((6, 6.6), (6, 5.4)),   # Pricing to OMS
        ((10, 6.6), (10, 5.4)), # Portfolio to Execution
        
        # Execution to Infrastructure
        ((4, 4.6), (4, 3.4)),   # To Message Queue
        ((8, 4.6), (8, 3.4)),   # To Database
        
        # To Exchange
        ((6, 4.6), (6, 1.4)),   # OMS to Exchange
        
        # Cross connections
        ((3.25, 7), (4.75, 7)), # Strategy to Pricing
        ((7.25, 7), (8.75, 7)), # Pricing to Portfolio
        ((3.25, 5), (4.75, 5)), # Order Gen to OMS
        ((7.25, 5), (8.75, 5)), # OMS to Execution
    ]
    
    for start, end in connections:
        arrow = ConnectionPatch(start, end, "data", "data",
                              arrowstyle="->", shrinkA=5, shrinkB=5,
                              mutation_scale=15, fc="darkblue", lw=1.2)
        ax.add_patch(arrow)
    
    # Add layer labels
    ax.text(0.5, 9, 'DATA LAYER', rotation=90, va='center', ha='center', 
            fontsize=12, fontweight='bold', color='darkblue')
    ax.text(0.5, 7, 'STRATEGY LAYER', rotation=90, va='center', ha='center', 
            fontsize=12, fontweight='bold', color='darkgreen')
    ax.text(0.5, 5, 'EXECUTION LAYER', rotation=90, va='center', ha='center', 
            fontsize=12, fontweight='bold', color='orange')
    ax.text(0.5, 3, 'INFRASTRUCTURE', rotation=90, va='center', ha='center', 
            fontsize=12, fontweight='bold', color='gray')
    ax.text(0.5, 1, 'EXCHANGE', rotation=90, va='center', ha='center', 
            fontsize=12, fontweight='bold', color='red')
    
    ax.set_title('quantRush - System Architecture', fontsize=16, fontweight='bold')
    
    # Add performance metrics box
    perf_text = """
    PERFORMANCE TARGETS
    ───────────────────
    • Latency: < 50μs order-to-wire
    • Throughput: 100K+ msg/sec
    • Uptime: 99.99%
    • Risk Limits: Real-time monitoring
    """
    
    ax.text(12.5, 2, perf_text, ha='left', va='center', fontsize=9,
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.8))
    
    return fig

def main():
    """Generate all strategy diagrams"""
    print("Generating quantRush strategy diagrams...")
    
    # Create order book visualization
    print("Creating order book visualization...")
    ob_fig = create_order_book_visualization()
    ob_fig.savefig('assets/market_making_diagram.png', dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
    
    # Create P&L attribution chart
    print("Creating P&L attribution analysis...")
    pnl_fig = create_pnl_attribution_chart()
    pnl_fig.savefig('assets/pnl_attribution.png', dpi=300, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
    
    # Create architecture diagram
    print("Creating system architecture diagram...")
    arch_fig = create_architecture_diagram()
    arch_fig.savefig('assets/architecture_diagram.png', dpi=300, bbox_inches='tight',
                     facecolor='white', edgecolor='none')
    
    print("✅ All strategy diagrams generated successfully!")
    print("📁 Files created:")
    print("   - assets/market_making_diagram.png")
    print("   - assets/pnl_attribution.png")
    print("   - assets/architecture_diagram.png")

if __name__ == "__main__":
    main()

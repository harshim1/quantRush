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
    
    ax1.set_title('Limit Order Book with Market Maker

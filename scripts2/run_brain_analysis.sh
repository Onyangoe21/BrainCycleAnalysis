#!/bin/bash
echo "🚀 Processing Brain Graphs..."
python scripts/process_brain_data.py

echo "🔍 Analyzing Cycles & Hubs..."
python scripts/analyze_brain_cycles.py

echo "📊 Visualizing Brain Network..."
python scripts/visualize_brain_network.py

echo "✅ Analysis Complete! Check results in 'results/' and figures in 'figures/'."

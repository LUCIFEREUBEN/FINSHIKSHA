import graphviz
import os

def generate_flowchart(income, expenses, emi, savings, emi_share, savings_rate, output_path="out/flowchart"):
    """Generate financial health flowchart"""
    try:
        os.makedirs("out", exist_ok=True)
        
        dot = graphviz.Digraph(comment='Financial Health', format='png')
        dot.attr(rankdir='TB')
        dot.attr('node', shape='box', style='rounded,filled', fontname='Arial')
        
        # Root
        dot.node('A', f'Monthly Income\n₹{income:,.0f}', fillcolor='lightblue')
        
        # Expenses
        dot.node('B', f'Expenses\n₹{expenses:,.0f}\n({expenses/income*100:.1f}%)', fillcolor='lightyellow')
        dot.edge('A', 'B')
        
        # EMI
        if emi > 0:
            color = 'lightcoral' if emi_share > 40 else 'lightyellow'
            dot.node('C', f'EMI\n₹{emi:,.0f}\n({emi_share:.1f}%)', fillcolor=color)
            dot.edge('A', 'C')
        
        # Savings
        if savings > 0:
            color = 'lightgreen' if savings_rate >= 20 else 'lightyellow'
            dot.node('D', f'Savings\n₹{savings:,.0f}\n({savings_rate:.1f}%)', fillcolor=color)
            dot.edge('A', 'D')
            
            # Recommendations
            if savings_rate >= 20:
                dot.node('E', 'Emergency Fund\n(6 months)', fillcolor='lightgreen')
                dot.node('F', 'Invest in\nMutual Funds', fillcolor='lightgreen')
                dot.edge('D', 'E')
                dot.edge('D', 'F')
        else:
            dot.node('D', f'⚠️ Overspending\n₹{abs(savings):,.0f}', fillcolor='lightcoral')
            dot.edge('A', 'D')
        
        # Health status
        if savings_rate >= 20 and emi_share < 40:
            status = '✅ Healthy Finances'
            color = 'lightgreen'
        elif savings_rate >= 10:
            status = '⚡ Needs Improvement'
            color = 'lightyellow'
        else:
            status = '🚨 Financial Stress'
            color = 'lightcoral'
        
        dot.node('Z', status, fillcolor=color, shape='ellipse')
        dot.edge('D', 'Z')
        
        dot.render(output_path, cleanup=True)
        return f"{output_path}.png"
    
    except Exception as e:
        print(f"Flowchart generation error: {e}")
        return None

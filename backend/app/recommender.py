def analyze_finances(income, expenses, emi=0):
    """Analyze financial health and provide recommendations"""
    
    savings = income - expenses - emi
    savings_rate = (savings / income * 100) if income > 0 else 0
    emi_share = (emi / income) if income > 0 else 0
    
    metrics = {
        "savings": savings,
        "savings_rate": round(savings_rate, 2),
        "emi_share": round(emi_share * 100, 2),
        "expense_ratio": round((expenses / income * 100) if income > 0 else 0, 2)
    }
    
    return metrics

def generate_recommendations(income, expenses, emi=0, lang="en"):
    """Generate personalized financial recommendations"""
    
    metrics = analyze_finances(income, expenses, emi)
    savings = metrics["savings"]
    savings_rate = metrics["savings_rate"]
    emi_share = metrics["emi_share"]
    
    recommendations = []
    
    if lang == "en":
        # English recommendations
        if savings <= 0:
            recommendations.append("⚠️ URGENT: Your expenses exceed income! You're overspending by ₹{:,.0f}. Cut unnecessary expenses immediately.".format(abs(savings)))
            recommendations.append("📊 Review your spending: Identify and reduce entertainment, dining out, and subscriptions.")
        
        if emi_share > 40:
            recommendations.append("🚨 DANGER: Your EMI (₹{:,.0f}) is {:.1f}% of income. Avoid taking new loans! Target EMI below 40%.".format(emi, emi_share))
            recommendations.append("💡 Consider: Prepay high-interest loans or consolidate debt to reduce EMI burden.")
        elif emi_share > 20:
            recommendations.append("⚡ WARNING: Your EMI is {:.1f}% of income. Be careful before taking new loans.".format(emi_share))
        
        if savings_rate < 10:
            recommendations.append("📉 Low Savings: You're saving only {:.1f}% of income. Target minimum 20% savings rate.".format(savings_rate))
            recommendations.append("🎯 Action Plan: Use 50-30-20 rule: 50% needs, 30% wants, 20% savings.")
        elif savings_rate >= 20:
            recommendations.append("✅ EXCELLENT: You're saving {:.1f}%! Consider investing ₹{:,.0f} monthly in mutual funds.".format(savings_rate, savings * 0.8))
        
        if savings > 0 and savings_rate >= 20:
            recommendations.append("💰 Emergency Fund: Build 6 months expenses (₹{:,.0f}) in savings account first.".format(expenses * 6))
            recommendations.append("📈 Investment Suggestion: Start SIP with ₹{:,.0f}/month in diversified mutual funds.".format(savings * 0.5))
        
        if not recommendations:
            recommendations.append("💪 Financial Health: You're doing okay! Keep saving {:.1f}% and avoid unnecessary debt.".format(savings_rate))
    
    return {
        "recommendations": recommendations,
        "metrics": metrics
    }

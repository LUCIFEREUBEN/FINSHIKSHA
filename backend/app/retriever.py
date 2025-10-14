from sentence_transformers import SentenceTransformer
import json
import os

class SimpleRetriever:
    def __init__(self):
        print("Initializing retriever...")
        self.knowledge_base = {
            "asset": "An asset is anything of value that you own. Examples include cash, bank deposits, property, gold, vehicles, and investments. Assets can generate income or appreciate in value over time.",
            
            "liability": "A liability is money you owe to others. Common liabilities include home loans, car loans, credit card debt, personal loans, and EMIs. High liabilities can affect your financial health.",
            
            "savings": "Savings is money set aside from your income for future use. Financial experts recommend the 50-30-20 rule: 50% for needs, 30% for wants, and 20% for savings. Emergency fund should cover 6 months of expenses.",
            
            "investment": "Investment is allocating money to generate returns. Options include fixed deposits (low risk, 6-7% returns), mutual funds (medium risk, 10-12% returns), stocks (high risk, variable returns), and gold (hedge against inflation).",
            
            "emi": "EMI (Equated Monthly Installment) is a fixed monthly payment for loans. EMI = [P x R x (1+R)^N]/[(1+R)^N-1], where P=Principal, R=Monthly interest rate, N=Tenure in months. Keep total EMI below 40% of monthly income.",
            
            "budget": "A budget tracks income and expenses. Create categories: Housing (30%), Food (15%), Transportation (10%), Utilities (5%), Insurance (10%), Savings (20%), Entertainment (10%). Use apps or spreadsheets to track spending.",
            
            "credit_score": "Credit score (300-900) reflects creditworthiness. Score above 750 is excellent. Factors: payment history (35%), credit utilization (30%), credit history length (15%), credit mix (10%), new credit (10%). Check free at CIBIL.",
            
            "insurance": "Insurance protects against financial loss. Types: Life insurance (cover 10-15x annual income), Health insurance (₹5-10 lakhs minimum), Term insurance (cheapest life cover), Vehicle insurance (mandatory). Buy young for lower premiums.",
            
            "mutual_funds": "Mutual funds pool money from investors to buy securities. Types: Equity (stocks, high risk), Debt (bonds, low risk), Hybrid (mixed). SIP (Systematic Investment Plan) allows monthly investments from ₹500. Regulated by SEBI.",
            
            "emergency_fund": "Emergency fund covers unexpected expenses. Target: 6-12 months of expenses. Keep in liquid assets like savings account or liquid mutual funds. Build gradually by saving 10-15% monthly. Don't invest in stocks."
        }
        print("Retriever ready with 10 financial topics!")
    
    def retrieve(self, query, top_k=2):
        """Simple keyword-based retrieval"""
        query_lower = query.lower()
        matches = []
        
        for key, text in self.knowledge_base.items():
            if key in query_lower or any(word in query_lower for word in key.split('_')):
                matches.append({
                    "text": text,
                    "topic": key.replace('_', ' ').title(),
                    "score": 1.0
                })
        
        # If no matches, return general financial literacy
        if not matches:
            matches.append({
                "text": "Financial literacy involves understanding assets, liabilities, savings, investments, and budgeting. Start by tracking your income and expenses, then create a budget and build an emergency fund.",
                "topic": "Financial Literacy Basics",
                "score": 0.5
            })
        
        return matches[:top_k]

retriever_instance = None

def get_retriever():
    global retriever_instance
    if retriever_instance is None:
        retriever_instance = SimpleRetriever()
    return retriever_instance

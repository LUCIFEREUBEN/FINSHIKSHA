"""
Safety and Content Moderation Module
Handles out-of-scope questions and crisis situations
"""
import re

class SafetyFilter:
    def __init__(self):
        # Crisis keywords (suicide, self-harm, severe depression)
        self.crisis_keywords = [
            'suicide', 'kill myself', 'end my life', 'want to die', 'suicidal',
            'self harm', 'cut myself', 'harm myself', 'no reason to live',
            'better off dead', 'everyone hates me', 'can\'t go on',
            # Hindi
            'आत्महत्या', 'मरना चाहता', 'जीना नहीं चाहता', 'खुद को मार',
            # Kannada  
            'ಆತ್ಮಹತ್ಯೆ', 'ಸಾಯಲು ಬಯಸುತ್ತೇನೆ'
        ]
        
        # Mild mental health keywords
        self.mental_health_keywords = [
            'depressed', 'depression', 'anxious', 'anxiety', 'stressed',
            'panic', 'worried', 'scared', 'fear', 'hopeless', 'sad',
            'tension', 'mental health', 'psychological',
            # Hindi
            'तनाव', 'डिप्रेशन', 'चिंता', 'परेशान',
            # Kannada
            'ಒತ್ತಡ', 'ಆತಂಕ', 'ಚಿಂತೆ'
        ]
        
        # Financial keywords (in-scope)
        self.financial_keywords = [
            'money', 'rupee', 'salary', 'income', 'expense', 'save', 'saving',
            'invest', 'investment', 'loan', 'emi', 'debt', 'credit', 'bank',
            'account', 'fund', 'stock', 'mutual fund', 'insurance', 'asset',
            'liability', 'budget', 'tax', 'return', 'interest', 'principal',
            'deposit', 'withdraw', 'payment', 'cash', 'financial', 'finance',
            'economy', 'pension', 'retirement', 'property', 'gold', 'bond',
            # Hindi
            'पैसा', 'रुपया', 'सैलरी', 'बचत', 'निवेश', 'लोन', 'बैंक', 'खाता',
            # Kannada
            'ಹಣ', 'ಸಂಬಳ', 'ಉಳಿತಾಯ', 'ಹೂಡಿಕೆ', 'ಸಾಲ', 'ಬ್ಯಾಂಕ್'
        ]
        
        # Non-financial out-of-scope topics
        self.out_of_scope_keywords = {
            'medical': ['medicine', 'doctor', 'disease', 'illness', 'hospital', 'treatment', 'surgery'],
            'legal': ['lawyer', 'court', 'case', 'legal', 'law', 'judge', 'police'],
            'relationship': ['girlfriend', 'boyfriend', 'marriage', 'divorce', 'dating', 'love'],
            'education': ['college', 'university', 'exam', 'study', 'degree', 'marks'],
            'career': ['job', 'interview', 'resume', 'career', 'promotion'],
            'technology': ['laptop', 'phone', 'computer', 'software', 'app', 'coding'],
            'shopping': ['buy car', 'buy bike', 'buy phone', 'shopping', 'purchase']
        }
    
    def check_crisis(self, text):
        """Check for mental health crisis"""
        text_lower = text.lower()
        
        # Crisis detection (highest priority)
        for keyword in self.crisis_keywords:
            if keyword in text_lower:
                return {
                    'is_crisis': True,
                    'severity': 'CRITICAL',
                    'message': self.get_crisis_response()
                }
        
        # Mental health concern (moderate priority)
        for keyword in self.mental_health_keywords:
            if keyword in text_lower and self.is_mental_health_context(text_lower):
                return {
                    'is_crisis': True,
                    'severity': 'MODERATE',
                    'message': self.get_mental_health_response()
                }
        
        return {'is_crisis': False}
    
    def is_mental_health_context(self, text):
        """Check if mental health keyword is in serious context"""
        # If combined with financial distress, it's a concern
        distress_indicators = ['can\'t', 'cannot', 'unable', 'hopeless', 'lost', 'don\'t know', 'no way']
        return any(indicator in text for indicator in distress_indicators)
    
    def check_scope(self, text):
        """Check if question is within financial scope"""
        text_lower = text.lower()
        
        # Check if it contains ANY financial keyword
        has_financial_keyword = any(keyword in text_lower for keyword in self.financial_keywords)
        
        if has_financial_keyword:
            return {'in_scope': True}
        
        # Check what category it falls into
        for category, keywords in self.out_of_scope_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return {
                    'in_scope': False,
                    'category': category,
                    'message': self.get_out_of_scope_response(category)
                }
        
        # If no keywords match, assume it's financial (give it benefit of doubt)
        return {'in_scope': True}
    
    def get_crisis_response(self):
        """Response for crisis situations"""
        return """
🚨 URGENT: I noticed you mentioned thoughts of self-harm or suicide. 

**Your life matters! Please reach out for immediate help:**

📞 **India National Suicide Prevention:**
   - Helpline: 1800-599-0019 (24/7 toll-free)
   - iCall: 9152987821 (Mon-Sat, 8 AM - 10 PM)
   - Vandrevala Foundation: 1860-2662-345 (24/7)
   - AASRA: 9820466726 (24/7)

💬 **International Crisis Support:**
   - WhatsApp Helpline: +91 9820466726

🏥 **For immediate danger:** Call 112 (Emergency) or visit nearest hospital

---

**About money and stress:**
I understand financial stress can feel overwhelming, but there are ALWAYS solutions:

1. **Debt is manageable** - Talk to credit counselors
2. **Jobs can be found** - Temporary setbacks are not permanent
3. **Family/friends want to help** - Don't isolate yourself
4. **Free financial counseling** available from NGOs

💪 **Remember:** 
- Financial problems are TEMPORARY
- Your life is PRECIOUS and IRREPLACEABLE
- Millions have overcome similar situations
- Professional help is available and effective

**Please talk to someone right now. You are not alone.** ❤️

---

*Note: I'm a financial literacy AI, not equipped for mental health support. Please contact the helplines above for proper care.*
"""
    
    def get_mental_health_response(self):
        """Response for mental health concerns"""
        return """
💙 I notice you're feeling stressed or anxious about finances. This is very common - you're not alone.

**Helpful resources:**

📞 **Mental Health Support:**
   - Vandrevala Foundation: 1860-2662-345 (24/7)
   - iCall: 9152987821 (8 AM - 10 PM)
   - NIMHANS: 080-46110007 (Mon-Sat, 9 AM - 5 PM)

💰 **Financial Stress Tips:**

1. **Break it down:** Tackle one small financial task at a time
2. **Talk to someone:** Family, friends, or financial counselor
3. **Make a plan:** Even small steps reduce anxiety
4. **Avoid isolation:** Connect with support groups
5. **Professional help:** Credit counseling NGOs offer free guidance

🧘 **Immediate Relief:**
- Take deep breaths (4 counts in, 6 counts out)
- Write down your worries (makes them less overwhelming)
- Physical activity (even 10-minute walk helps)
- Avoid financial decisions when highly stressed

---

**I can still help with your financial questions!** Let's work through your specific situation together. What financial aspect would you like to understand better?

*Remember: Financial problems have solutions. Your wellbeing comes first.* ❤️
"""
    
    def get_out_of_scope_response(self, category):
        """Response for out-of-scope questions"""
        
        responses = {
            'medical': "I'm a financial literacy assistant and can't provide medical advice. However, I can help with medical **expenses** and health **insurance** questions! For medical advice, please consult a doctor.",
            
            'legal': "I can't provide legal advice, but I can help with financial aspects like loan **contracts**, tax **regulations**, or financial **fraud** awareness! For legal matters, consult a lawyer.",
            
            'relationship': "While I can't give relationship advice, I can help with **financial planning for marriage**, **joint accounts**, or **household budgeting** for couples!",
            
            'education': "I can't help with academic advice, but I can assist with **education loan planning**, **saving for child education**, or **financial planning for students**!",
            
            'career': "I focus on financial literacy, but I can help with **salary negotiation tips**, **income management**, or **career-related financial planning**!",
            
            'technology': "I'm not a tech expert, but I can help with **budgeting for gadgets**, **financing technology purchases**, or **digital payment systems**!",
            
            'shopping': "I can't recommend specific products, but I can help you with **budgeting for purchases**, **evaluating loans vs cash payment**, or **avoiding impulse buying**!"
        }
        
        return f"""
🤔 **Slightly Out of My Expertise!**

{responses.get(category, "This question is outside financial literacy, but I'm here to help with money management!")}

**Try asking me:**
- "How do I budget for [your need]?"
- "What's the smart way to finance [purchase]?"
- "How can I save money for [goal]?"
- "Should I take a loan for this?"

💡 **Or, let's talk finances:** What's your financial goal or concern?
"""
    
    def process_question(self, question):
        """Main processing function"""
        
        # Step 1: Check for crisis (highest priority)
        crisis_check = self.check_crisis(question)
        if crisis_check['is_crisis']:
            return {
                'safe': False,
                'block': True,
                'severity': crisis_check['severity'],
                'response': crisis_check['message']
            }
        
        # Step 2: Check if in scope
        scope_check = self.check_scope(question)
        if not scope_check.get('in_scope', True):
            return {
                'safe': True,
                'block': False,
                'in_scope': False,
                'response': scope_check['message']
            }
        
        # Step 3: All clear - proceed with normal processing
        return {
            'safe': True,
            'block': False,
            'in_scope': True,
            'response': None
        }


# Initialize global instance
safety_filter = SafetyFilter()

def check_safety(question):
    """Main safety check function"""
    return safety_filter.process_question(question)

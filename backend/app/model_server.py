from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from pathlib import Path

class FinLitModel:
    def __init__(self):
        print("Loading model...")
        self.model_name = "google/flan-t5-small"
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        self.device = "cpu"
        self.model.to(self.device)
        print("Model loaded successfully!")
    
    def generate(self, text, lang="en", max_length=200):
        """Generate financial advice with strong fallback"""
        
        # Build prompt
        if lang == "hi":
            prompt = f"हिंदी में सरल भाषा में उत्तर दें: {text}"
        elif lang == "kn":
            prompt = f"ಸರಳ ಕನ್ನಡದಲ್ಲಿ ಉತ್ತರಿಸಿ: {text}"
        else:
            prompt = f"Explain in simple terms for beginners: {text}"
        
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
            inputs = inputs.to(self.device)
            
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                num_beams=4,
                temperature=0.7,
                do_sample=True,
                top_p=0.9,
                no_repeat_ngram_size=3,
                early_stopping=True
            )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Check if response is valid
            if response and len(response) > 20 and '<' not in response and 'extra_id' not in response.lower():
                return response
            else:
                # Use fallback if model fails
                return self.get_fallback_response(text, lang)
        
        except Exception as e:
            print(f"Model generation error: {e}")
            return self.get_fallback_response(text, lang)
    
    def get_fallback_response(self, text, lang):
        """Comprehensive fallback responses for all common questions"""
        
        fallback_responses = {
            "en": {
                # Basic Concepts
                "asset": "An asset is anything valuable you own that can make money or increase in value over time. Common assets include:\n\n• Cash in bank (savings, FD)\n• Real estate (house, land, property)\n• Gold and jewelry\n• Vehicles (car, bike)\n• Investments (mutual funds, stocks, bonds)\n• Business ownership\n\nAssets help build wealth and financial security. They can generate income (like rent from property or dividends from stocks) or appreciate in value. Focus on building appreciating assets (grow in value) rather than depreciating assets (lose value like cars).",
                
                "liability": "A liability is money you owe to others - any debt or financial obligation. Types include:\n\n• Home loans/mortgages\n• Car loans\n• Personal loans\n• Education loans\n• Credit card debt\n• EMIs (monthly installments)\n\nLiabilities reduce your net worth and create financial stress. Important rules:\n• Keep total EMI below 40% of monthly income\n• Pay high-interest debt first (credit cards)\n• Avoid lifestyle loans (for vacations, gadgets)\n\nYour Net Worth = Total Assets - Total Liabilities. Focus on increasing assets and reducing liabilities for financial freedom.",
                
                "emi": "EMI = Equated Monthly Installment. It's a fixed amount you pay every month to repay a loan.\n\nEMI has two parts:\n• Principal (original loan amount)\n• Interest (cost of borrowing)\n\nExample: ₹10 lakh loan at 10% interest for 5 years = ₹21,247 monthly EMI\n\nImportant rules:\n• Keep total EMI below 40% of income\n• Higher EMI = faster loan closure but less savings\n• Prepay high-interest loans first\n\nIf you earn ₹50,000/month, maximum EMI should be ₹20,000. This leaves money for savings and emergencies.",
                
                "saving": "Savings are the portion of income you don't spend. Financial experts recommend:\n\n**50-30-20 Rule:**\n• 50% for Needs (rent, food, EMI)\n• 30% for Wants (entertainment, shopping)\n• 20% for Savings & Investments\n\n**By Age:**\n• 20s-30s: Save 20-30%\n• 30s-40s: Save 25-35%\n• 40s-50s: Save 30-40%\n\n**Priority Order:**\n1. Build 6-month emergency fund\n2. Clear high-interest debt\n3. Start SIP in mutual funds\n4. Increase savings with salary hikes\n\nMinimum: Save at least 15-20% of income. If earning ₹50,000/month, save ₹10,000 minimum.",
                
                "investment": "Investment means putting money into assets that can grow over time. Unlike savings (keep money safe), investments aim to beat inflation and build wealth.\n\n**Types:**\n• Equity (stocks, equity mutual funds): High risk, 12-15% returns\n• Debt (bonds, FDs, debt funds): Low risk, 6-8% returns\n• Gold: Hedge against inflation, 8-10% returns\n• Real Estate: Long-term, 7-9% returns\n\n**Investment Strategy by Time:**\n• Emergency fund: Savings account (need liquidity)\n• 1-2 years: Fixed deposits, debt funds\n• 3-5 years: Hybrid mutual funds\n• 5+ years: Equity mutual funds, stocks\n\n**Golden Rule:** Don't invest money you need in next 3 years in stocks. Start early - even ₹500/month SIP grows to ₹10+ lakhs in 20 years!",
                
                "mutual fund": "Mutual funds pool money from many investors to buy securities (stocks, bonds, gold). Managed by professional fund managers.\n\n**Types:**\n• Equity Funds: Invest in stocks (high risk, 12-15% returns)\n• Debt Funds: Invest in bonds (low risk, 6-8% returns)\n• Hybrid Funds: Mix of stocks+bonds (medium risk, 8-10% returns)\n• Index Funds: Copy Nifty/Sensex (low cost, market returns)\n\n**Benefits:**\n• Professional management\n• Diversification (spreads risk)\n• Start small (₹500/month SIP)\n• Easy to buy and sell (1-3 day)\n• SEBI regulated (safe)\n\n**How to invest:**\nUse apps like Groww, Zerodha, Paytm Money or directly from AMC websites. Best for long-term wealth creation!",
                
                "sip": "SIP = Systematic Investment Plan. Invest fixed amount monthly in mutual funds automatically.\n\n**How it works:**\n1. Choose mutual fund scheme\n2. Set monthly amount (₹500, ₹1000, ₹5000)\n3. Auto-debit from bank on fixed date\n4. Units credited at current NAV price\n\n**Benefits:**\n• Rupee Cost Averaging: Buy more when price low, less when high\n• Power of Compounding: Returns generate more returns\n• Disciplined investing: Automatic habit\n• Start small: Begin with ₹500\n\n**Example:** ₹5000/month SIP for 20 years at 12% = ₹1.49 crores!\n\nBest for salaried individuals and first-time investors. Never stop SIP during market falls - that's when you get cheapest units!",
                
                "emergency fund": "Emergency fund is money set aside for unexpected expenses:\n• Medical emergencies\n• Job loss (cover 6-12 months expenses)\n• Urgent home/vehicle repairs\n• Family emergencies\n\n**Target Amount:** 6-12 months of monthly expenses\nIf you spend ₹30,000/month, keep ₹1.8-3.6 lakhs\n\n**Where to keep:**\n• Savings account (instant access)\n• Liquid mutual funds (withdraw in 1 day)\n• Sweep-in FD (earns interest + liquid)\n\n**DON'T:**\n• Invest in stocks (too risky)\n• Put in long lock-in schemes\n• Use for lifestyle expenses\n\nBuild gradually by saving 10-15% monthly. This fund gives peace of mind and prevents debt during crises.",
                
                "insurance": "Insurance protects against financial loss from unexpected events.\n\n**Life Insurance (Term):**\n• If you die, family gets money (₹50L - ₹1 crore)\n• Coverage: 10-15 times annual income\n• Cost: ₹500-1000/month for ₹1 crore cover (age 30)\n• Buy when young (cheaper premiums)\n• DON'T mix with investment (avoid LIC endowment)\n\n**Health Insurance:**\n• Covers medical expenses (₹5-10 lakh minimum)\n• Family floater available\n• Cashless at network hospitals\n• Medical inflation is 10-15% yearly\n\n**Why needed:**\n• One serious illness can wipe out savings\n• Insurance is cheapest when young and healthy\n• Provides financial protection to family\n\nPriority: Term life insurance if you have dependents + health insurance for everyone.",
                
                "budget": "Budgeting is planning how to spend your money wisely.\n\n**50-30-20 Rule:**\n• 50% Needs: Rent, food, utilities, EMI, insurance, transport\n• 30% Wants: Entertainment, dining, shopping, hobbies, vacations\n• 20% Savings: Emergency fund, investments, retirement\n\n**Example: ₹50,000 salary**\n• ₹25,000 for needs\n• ₹15,000 for wants\n• ₹10,000 for savings\n\n**Budgeting Steps:**\n1. Track all expenses for 1 month\n2. Categorize into needs/wants/savings\n3. Set spending limits for each category\n4. Review monthly and adjust\n5. Use apps like Walnut, Money Manager\n\n**Tips:**\n• Pay yourself first (save before spending)\n• Avoid impulse purchases\n• Use cash for wants (limits spending)\n• Automate savings on salary day",
                
                "credit score": "Credit score is a 3-digit number (300-900) showing creditworthiness. Banks check it before giving loans.\n\n**Score Ranges:**\n• 750-900: Excellent (instant approval, lowest rates)\n• 650-749: Good (likely approval, moderate rates)\n• 550-649: Average (difficult approval, high rates)\n• Below 550: Poor (rejection likely)\n\n**Factors (CIBIL):**\n• Payment history (35%): Pay EMIs/cards on time\n• Credit utilization (30%): Use <30% of credit limit\n• Credit history (15%): Keep old accounts active\n• Credit mix (10%): Mix of secured/unsecured loans\n• New credit (10%): Don't apply multiple loans together\n\n**Check Free:** CIBIL.com, Experian, Paisa Bazaar (once yearly)\n\n**Improve Score:**\n• Pay all bills on time\n• Keep credit card usage low\n• Don't close old credit cards\n• Check for errors and dispute",
                
                "tax": "Taxes reduce your income. Smart planning can save ₹50,000+ yearly!\n\n**Section 80C (₹1.5L limit):**\n• ELSS mutual funds (best: 3 year lock-in, high returns)\n• PPF (7-8%, 15 year lock-in)\n• Life insurance premium\n• Home loan principal\n• NSC, FD (5 years)\n\n**Section 80D:**\n• Health insurance: ₹25,000 (self)\n• Parents insurance: ₹25,000 more (₹50K if senior citizens)\n\n**Section 80CCD(1B):**\n• NPS: Additional ₹50,000 deduction\n\n**Home Loan:**\n• Interest: ₹2 lakhs deduction (Section 24)\n• First-time buyer: ₹1.5L additional (80EEA)\n\n**Total Possible Savings:** ₹1.5L (80C) + ₹50K (NPS) + ₹2L (home loan) + ₹50K (health) = ₹3.5L deductions = ₹1L+ tax saved!",
                
                "retirement": "Retirement planning ensures financial independence in old age.\n\n**How Much Needed:**\nRule of thumb: 25-30X annual expenses\nIf ₹50,000/month expenses = ₹1.5-1.8 crores needed at retirement\n\n**Start Age Matters:**\n• At 25: ₹5000/month SIP = ₹1.5 crores by 60\n• At 35: ₹15,000/month SIP = ₹1.5 crores by 60\n• At 45: ₹50,000/month SIP = ₹1.5 crores by 60\n\n**Investment Options:**\n• EPF (mandatory for salaried): 8-9% returns\n• NPS (extra ₹50K tax benefit): 8-10% returns\n• PPF (₹1.5L yearly): 7-8%, tax-free\n• Equity mutual funds: 10-12% long-term\n\n**Strategy by Age:**\n• 20s-40s: 70-80% equity (growth)\n• 40s-50s: 60-70% equity (balanced)\n• 50s-60s: 40-50% equity (conservative)\n\nStart NOW! Time is your biggest asset in retirement planning.",
                
                "loan": "Loans let you borrow money to buy things now and pay later with interest.\n\n**Secured Loans (backed by asset):**\n• Home loan: 8-10% interest, 15-30 years\n• Car loan: 8-12% interest, 5-7 years\n• Gold loan: 7-9% interest, 1-3 years\n\n**Unsecured Loans (no asset):**\n• Personal loan: 12-24% interest, 1-5 years\n• Credit card debt: 36-42% interest (HIGHEST!)\n• Education loan: 8-12% interest, 5-15 years\n\n**Loan Rules:**\n• Keep total EMI < 40% of monthly income\n• Compare interest rates (even 1% difference = ₹lakhs saved)\n• Read fine print (processing fee, prepayment charges)\n• Avoid loans for lifestyle (vacation, wedding, gadgets)\n• Good debt: Home, education (builds assets)\n• Bad debt: Credit cards, personal loans (no asset)\n\n**Priority:** Pay off high-interest debt first (credit cards, personal loans) before investing.",
                
                "default": "I'm your AI financial literacy assistant! I can help you understand:\n\n**Basic Concepts:**\n• What is an asset?\n• What is a liability?\n• How to calculate EMI?\n• Emergency fund planning\n\n**Investing:**\n• Mutual funds explained\n• SIP benefits\n• Stock vs mutual funds\n• Tax-saving options (80C)\n\n**Planning:**\n• How much to save?\n• Budget planning (50-30-20 rule)\n• Retirement planning\n• Insurance needs\n\n**Banking:**\n• Credit score importance\n• Types of loans\n• UPI and digital payments\n\nTry asking: 'What is an asset?' or 'Explain EMI simply' or 'How much should I save?'\n\nI provide simple, clear answers for financial literacy - perfect for beginners!"
            },
            "hi": {
                "asset": "संपत्ति वह मूल्यवान चीज है जो आपके पास है और जो समय के साथ आय उत्पन्न कर सकती है या मूल्य बढ़ा सकती है। मुख्य संपत्तियां:\n\n• नकद और बैंक जमा (बचत खाता, FD)\n• रियल एस्टेट (घर, जमीन, प्रॉपर्टी)\n• सोना और आभूषण\n• वाहन (कार, बाइक)\n• निवेश (म्यूचुअल फंड, शेयर, बॉन्ड)\n• व्यापार\n\nसंपत्ति धन निर्माण और वित्तीय सुरक्षा में मदद करती है। यह आय उत्पन्न कर सकती है (प्रॉपर्टी से किराया, शेयरों से डिविडेंड) या समय के साथ मूल्य बढ़ सकती है।",
                
                "emi": "EMI का मतलब Equated Monthly Installment है। यह लोन चुकाने के लिए हर महीने pay की जाने वाली fixed राशि है।\n\nEMI में दो हिस्से हैं:\n• Principal (मूल लोन राशि)\n• Interest (उधार लेने की लागत)\n\nउदाहरण: ₹10 लाख लोन, 10% सालाना ब्याज, 5 साल = ₹21,247 मासिक EMI\n\nमहत्वपूर्ण नियम:\n• कुल EMI मासिक आय के 40% से कम रखें\n• ज्यादा EMI = जल्दी लोन खत्म पर कम बचत\n• High-interest loans पहले चुकाएं",
                
                "default": "मैं आपका AI वित्तीय साक्षरता सहायक हूं! मैं मदद कर सकता हूं:\n\n• संपत्ति क्या है?\n• देनदारी क्या है?\n• EMI कैसे calculate करें?\n• बचत कैसे करें?\n• Mutual funds क्या हैं?\n• निवेश कैसे शुरू करें?\n\nकुछ पूछें जैसे 'संपत्ति क्या है?' या 'EMI समझाएं' या 'कितनी बचत करूं?'"
            },
            "kn": {
                "asset": "ಆಸ್ತಿ ಎಂದರೆ ನೀವು ಹೊಂದಿರುವ ಮೌಲ್ಯವುಳ್ಳ ವಸ್ತು ಮತ್ತು ಇದು ಕಾಲಾನಂತರದಲ್ಲಿ ಆದಾಯ ಉತ್ಪಾದಿಸಬಹುದು ಅಥವಾ ಮೌಲ್ಯ ಹೆಚ್ಚಿಸಬಹುದು। ಮುಖ್ಯ ಆಸ್ತಿಗಳು:\n\n• ನಗದು ಮತ್ತು ಬ್ಯಾಂಕ್ ಠೇವಣಿ (ಉಳಿತಾಯ, FD)\n• ರಿಯಲ್ ಎಸ್ಟೇಟ್ (ಮನೆ, ಜಮೀನು)\n• ಚಿನ್ನ ಮತ್ತು ಆಭರಣಗಳು\n• ವಾಹನಗಳು (ಕಾರು, ಬೈಕ್)\n• ಹೂಡಿಕೆಗಳು (ಮ್ಯೂಚುಯಲ್ ಫಂಡ್, ಷೇರುಗಳು)\n\nಆಸ್ತಿಗಳು wealth ಹೆಚ್ಚಿಸುತ್ತವೆ ಮತ್ತು ಆದಾಯ ಉತ್ಪಾದಿಸುತ್ತವೆ।",
                
                "emi": "EMI ಎಂದರೆ ಸಾಲವನ್ನು ತಿರುಗಿ ಪಾವತಿಸಲು ಪ್ರತಿ ತಿಂಗಳು ನೀಡುವ ನಿಗದಿತ ಮೊತ್ತ।\n\nEMI ಯಲ್ಲಿ ಎರಡು ಭಾಗಗಳು:\n• Principal (ಮೂಲ ಸಾಲ)\n• Interest (ಬಡ್ಡಿ)\n\nಉದಾಹರಣೆ: ₹10 ಲಕ್ಷ ಸಾಲ, 10% ವಾರ್ಷಿಕ ಬಡ್ಡಿ, 5 ವರ್ಷ = ₹21,247 ಮಾಸಿಕ EMI\n\nಮುಖ್ಯ ನಿಯಮ: ಒಟ್ಟು EMI ನಿಮ್ಮ ಮಾಸಿಕ ಆದಾಯದ 40% ಕ್ಕಿಂತ ಕಡಿಮೆ ಇರಬೇಕು।",
                
                "default": "ನಾನು ನಿಮ್ಮ AI ಹಣಕಾಸು ಸಾಕ್ಷರತೆ ಸಹಾಯಕ! ನಾನು ಸಹಾಯ ಮಾಡಬಲ್ಲೆ:\n\n• ಆಸ್ತಿ ಎಂದರೇನು?\n• ಹೊಣೆಗಾರಿಕೆ ಎಂದರೇನು?\n• EMI ಹೇಗೆ ಲೆಕ್ಕ ಹಾಕುವುದು?\n• ಉಳಿತಾಯ ಹೇಗೆ ಮಾಡುವುದು?\n• Mutual funds ಎಂದರೇನು?\n\nಕೇಳಿ: 'ಆಸ್ತಿ ಎಂದರೇನು?' ಅಥವಾ 'EMI ವಿವರಿಸಿ'"
            }
        }
        
        text_lower = text.lower()
        
        # Match keywords to responses
        for key in fallback_responses[lang].keys():
            if key in text_lower or key.replace(' ', '') in text_lower.replace(' ', ''):
                return fallback_responses[lang][key]
        
        # Default response if no match
        return fallback_responses[lang].get("default", fallback_responses["en"]["default"])


model_instance = None

def get_model():
    global model_instance
    if model_instance is None:
        model_instance = FinLitModel()
    return model_instance

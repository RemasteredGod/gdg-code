import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import re
import json

class DisasterResponseChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("India Disaster Response Chatbot")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        self.state_helplines = {
            'andhra pradesh': '108, 112',
            'arunachal pradesh': '1070, 112',
            'assam': '1077, 1070, 0361-2237219, 9401044617',
            'bihar': '1078, 18002456145',
            'chhattisgarh': '1070, 112',
            'delhi': '1077, Central Control Room: 011-24611210',
            'goa': '108, 112',
            'gujarat': '1078, 079-23276944, 1077',
            'haryana': '112, NDRF: 9711077372',
            'himachal pradesh': '1100, 1070, 1077',
            'jharkhand': '1070, 112',
            'karnataka': '080-1070, 080-22340676',
            'kerala': '1070, 1077',
            'madhya pradesh': '108, 1070',
            'maharashtra': '1916, 108',
            'manipur': '1070, 112',
            'meghalaya': '108, 1070',
            'mizoram': '1070, 112',
            'nagaland': '1070, 112',
            'odisha': '1078, 1093, 112, 1800 200 4444',
            'punjab': '8968215758, NDRF: 011-26107953',
            'rajasthan': '1078',
            'sikkim': '1070, 112',
            'tamil nadu': '1070, 1078, 1077',
            'telangana': '108, 112, 211111111',
            'tripura': '1070, 112',
            'uttar pradesh': '1070, 112',
            'uttarakhand': '1070, 9557444486',
            'west bengal': '1800-11-3330, 1070, 2214-4052',
            'jammu and kashmir': '1077',
            'ladakh': '1077',
            'puducherry': '1077',
            'chandigarh': '1077',
            'daman and diu': '1077',
            'dadra and nagar haveli': '1077',
            'lakshadweep': '1077',
            'andaman and nicobar islands': '1077'
        }
        
        self.national_helplines = {
            'police': '100',
            'fire': '101',
            'ambulance': '102',
            'women helpline': '1091',
            'child helpline': '1098',
            'senior citizen helpline': '1090',
            'disaster management': '108',
            'ndrf': '011-24363260',
            'ndma': '011-26701728'
        }
        
        self.disaster_instructions = {
            'earthquake': [
                "🚨 EARTHQUAKE SAFETY INSTRUCTIONS:",
                "• Drop, Cover, and Hold On immediately",
                "• Stay away from windows, glass, and heavy objects",
                "• If indoors: Stay inside, get under a sturdy table/desk",
                "• If outdoors: Move to an open area away from buildings, trees, and power lines",
                "• If in a vehicle: Stop safely and stay inside",
                "• After shaking stops: Check for injuries and damage",
                "• Be prepared for aftershocks",
                "• Listen to emergency broadcasts for updates"
            ],
            'cyclone': [
                "🌀 CYCLONE SAFETY INSTRUCTIONS:",
                "PREPARATION BEFORE CYCLONE SEASON:",
                "• Secure roof tiles, repair doors/windows, trim trees",
                "• Store emergency food, water, medicine, and light sources",
                "• Prepare emergency kit and secure outdoor objects",
                "",
                "WHEN WARNING IS ISSUED:",
                "• Move away from low-lying coastal areas early",
                "• Board up glass windows; remove or secure loose items outside",
                "• Switch off electricity; shelter in strong, safe interior rooms",
                "• Do not go out during lull (eye of cyclone); wait for official 'all clear'"
            ],
            'tsunami': [
                "🌊 TSUNAMI SAFETY INSTRUCTIONS:",
                "IMMEDIATE ACTIONS:",
                "• Immediately move to higher ground/inland if warning issued",
                "• Do not wait for instructions if close to the coast—evacuate as quickly as possible",
                "• Avoid river valleys; follow evacuation signage to uphill footpaths",
                "• Stay away from beaches and waterfront until official all-clear is given",
                "",
                "SAFETY TIPS:",
                "• If you're in a boat, go to deep water (at least 100 fathoms)",
                "• Stay away from rivers and streams that lead to the ocean",
                "• Listen to emergency broadcasts for updates"
            ],
            'flood': [
                "🌊 FLOOD SAFETY INSTRUCTIONS:",
                "IMMEDIATE ACTIONS:",
                "• Listen to weather alerts, move to higher ground if flash flood likely",
                "• Avoid crossing moving water: Six inches can knock down a person",
                "• Do not drive into flooded roads; abandon car if trapped and safely climb to higher ground",
                "",
                "PREPARATION:",
                "• Elevate electrical and valuable items; turn off utilities before evacuation",
                "• Prepare an emergency kit and ensure outdoor objects are secured",
                "• Keep important documents in waterproof containers",
                "• Stay tuned to weather updates and emergency broadcasts"
            ],
            'landslide': [
                "🏔️ LANDSLIDE SAFETY INSTRUCTIONS:",
                "PREVENTION & MONITORING:",
                "• Monitor weather and listen to warnings; avoid slope areas during heavy rain",
                "• Avoid river valleys, unstable slopes, and recently burned areas",
                "",
                "IF LANDSLIDE OCCURS:",
                "• If indoors: Move to upper floors or higher ground; stay away from windows and doors",
                "• If outside: Move away from landslide path and uphill",
                "• Help others and report hazards after area is declared safe",
                "",
                "SAFETY TIPS:",
                "• Be aware of your surroundings and potential escape routes",
                "• Listen for unusual sounds (rumbling, cracking, falling rocks)"
            ],
            'fire': [
                "🔥 FIRE SAFETY INSTRUCTIONS:",
                "PREVENTION MEASURES:",
                "• Establish clear evacuation routes with proper signage and conduct regular drills",
                "• Install smoke detectors and fire alarms in high-risk areas",
                "• Use fire-resistant materials for furnishings and construction",
                "",
                "DURING FIRE:",
                "• Know how to raise alarm, call fire brigade (101), and evacuate safely",
                "• Get out of the building immediately",
                "• If trapped, close doors and seal gaps with wet cloths",
                "• Stay low to avoid smoke inhalation",
                "• Never use elevators during a fire; evacuate using stairs",
                "• Stop, Drop, and Roll if your clothes catch fire"
            ],
            'drought': [
                "☀️ DROUGHT SAFETY INSTRUCTIONS:",
                "WATER CONSERVATION:",
                "• Conserve water - use only what you need",
                "• Store water in clean, covered containers",
                "• Avoid activities that waste water",
                "• Follow local water restrictions",
                "• Report water leaks immediately",
                "",
                "PREPARATION:",
                "• Use drought-resistant plants in gardens",
                "• Stay informed about water availability",
                "• Help neighbors who may need assistance"
            ]
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title_label = tk.Label(main_frame, text="🇮🇳 India Disaster Response Chatbot", 
                              font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(main_frame, text="Get emergency help, safety instructions, and helpline numbers", 
                                 font=('Arial', 10), bg='#f0f0f0', fg='#7f8c8d')
        subtitle_label.pack(pady=(0, 20))
    
        chat_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, bd=1)
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.chat_display = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, 
                                                     font=('Arial', 10), bg='white', 
                                                     fg='#2c3e50', state=tk.DISABLED,
                                                     height=20)
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        input_frame = tk.Frame(main_frame, bg='#f0f0f0')
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.input_field = tk.Entry(input_frame, font=('Arial', 11), relief=tk.RAISED, bd=2)
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_field.bind('<Return>', self.send_message)
        
        send_button = tk.Button(input_frame, text="Send", command=self.send_message, 
                               bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                               relief=tk.RAISED, bd=2, padx=20)
        send_button.pack(side=tk.RIGHT)
        
        quick_frame = tk.Frame(main_frame, bg='#f0f0f0')
        quick_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(quick_frame, text="Quick Actions:", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0', fg='#2c3e50').pack(anchor=tk.W)
        
        button_frame = tk.Frame(quick_frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, pady=(5, 0))
        
        buttons = [
            ("Emergency", "help emergency"),
            ("Earthquake", "help earthquake"),
            ("Flood", "help flood"),
            ("Fire", "help fire"),
            ("Cyclone", "help cyclone"),
            ("Tsunami", "help tsunami"),
            ("Landslide", "help landslide"),
            ("State Help", "state inquiry")
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = tk.Button(button_frame, text=text, command=lambda c=command: self.quick_action(c),
                           bg='#e74c3c' if text == "Emergency" else '#95a5a6', 
                           fg='white', font=('Arial', 9, 'bold'),
                           relief=tk.RAISED, bd=1, padx=10, pady=5)
            btn.pack(side=tk.LEFT, padx=(0, 5))
        
        emergency_frame = tk.Frame(main_frame, bg='#ecf0f1', relief=tk.RAISED, bd=1)
        emergency_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(emergency_frame, text="🚨 Emergency Contacts:", font=('Arial', 10, 'bold'), 
                bg='#ecf0f1', fg='#e74c3c').pack(anchor=tk.W, padx=5, pady=5)
        
        contacts_text = "Police: 100 | Fire: 101 | Ambulance: 102 | Women: 1091 | Child: 1098 | Disaster: 108"
        tk.Label(emergency_frame, text=contacts_text, font=('Arial', 9), 
                bg='#ecf0f1', fg='#2c3e50').pack(anchor=tk.W, padx=5, pady=(0, 5))
        
        self.add_to_chat("🤖 Welcome to ResQIndia Disaster Response Chatbot!")
        self.add_to_chat("I can help you with:")
        self.add_to_chat("• State-wise disaster helpline numbers")
        self.add_to_chat("• Disaster safety instructions (Earthquake, Flood, Fire, Cyclone, Tsunami, Landslide)")
        self.add_to_chat("• Emergency contact numbers")
        self.add_to_chat("• General disaster preparedness advice")
        self.add_to_chat("\n💡 Try typing: 'help fire', 'earthquake help', 'flood safety', or use quick action buttons!")
        self.add_to_chat("\n📍 Do you need state-specific help? Please tell me which state you're in for personalized assistance!")
        
    def add_to_chat(self, message, sender="Bot"):
        self.chat_display.config(state=tk.NORMAL)
        if sender == "Bot":
            self.chat_display.insert(tk.END, f"🤖 {message}\n\n")
        else:
            self.chat_display.insert(tk.END, f"👤 You: {message}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def send_message(self, event=None):
        message = self.input_field.get().strip()
        if not message:
            return
            
        self.add_to_chat(message, "User")
        self.input_field.delete(0, tk.END)
        
        response = self.process_message(message)
        self.add_to_chat(response)
        
    def quick_action(self, action):
        self.input_field.delete(0, tk.END)
        self.input_field.insert(0, action)
        self.send_message()
        
    def process_message(self, message):
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['emergency','danger']):
            return self.get_emergency_response()
        
        state_response = self.detect_state_helpline(message)
        if state_response:
            return state_response
        
        disaster_response = self.detect_disaster_type(message_lower)
        if disaster_response:
            return disaster_response
        
        if any(word in message_lower for word in ['national', 'all india', 'country', 'india']):
            return self.get_national_helplines()
        
        if any(word in message_lower for word in ['helpline', 'number', 'contact', 'phone']):
            return self.get_general_helplines()
        
        if message_lower in ['state inquiry', 'state help']:
            return self.get_state_inquiry_response()
        
        if any(word in message_lower for word in ['help', 'assistance', 'support', 'what can you do']):
            return self.get_state_inquiry_response()
        
        return self.get_default_response()
    
    def get_state_inquiry_response(self):
        response = "I'm here to help with disaster-related emergencies in India!\n\n"
        response += "📍 **For the most relevant help, please tell me:**\n"
        response += "• Which state you're in (e.g., 'I'm in Maharashtra')\n"
        response += "• What type of disaster you need help with\n\n"
        response += "**Available assistance:**\n"
        response += "• State-specific disaster helpline numbers\n"
        response += "• Disaster safety instructions (Earthquake, Flood, Fire, Cyclone, Tsunami, Landslide)\n"
        response += "• Emergency contact numbers\n"
        response += "• Disaster preparedness advice\n\n"
        response += "**Quick examples:**\n"
        response += "• 'I'm in Kerala and there's a flood' → Kerala helpline + flood safety\n"
        response += "• 'help fire' → Fire safety instructions\n"
        response += "• 'emergency' → Immediate emergency response"
        return response
    
    def get_emergency_response(self):
        response = "🚨 EMERGENCY RESPONSE:\n\n"
        response += "IMMEDIATE ACTIONS:\n"
        response += "• Call 100 for Police\n"
        response += "• Call 101 for Fire\n"
        response += "• Call 102 for Ambulance\n"
        response += "• Call 108 for Disaster Management\n\n"
        response += "STAY CALM AND FOLLOW THESE STEPS:\n"
        response += "1. Ensure your safety first\n"
        response += "2. Call emergency services immediately\n"
        response += "3. Follow their instructions\n"
        response += "4. Help others if it's safe to do so\n"
        response += "5. Stay in a safe location\n\n"
        response += "For specific disaster instructions, mention the type of disaster."
        return response
    
    def detect_state_helpline(self, message):
        message_lower = message.lower()
        
        state_variations = {
            'andhra pradesh': ['andhra', 'andhra pradesh', 'ap','help andhra pradesh','andhra pradesh help'],
            'arunachal pradesh': ['arunachal', 'arunachal pradesh','help arunachal pradesh','arunachal pradesh help'],
            'assam': ['assam','help assam','assam help'],
            'bihar': ['bihar','help bihar','bihar help'],
            'chhattisgarh': ['chhattisgarh', 'chattisgarh', 'chhatisgarh','help chhattisgarh','chhattisgarh help'],
            'delhi': ['delhi', 'new delhi', 'nct','help delhi','delhi help'],
            'goa': ['goa','help goa','goa help'],
            'gujarat': ['gujarat', 'gujrat','help gujarat','gujarat help'],
            'haryana': ['haryana','help haryana','haryana help'],
            'himachal pradesh': ['himachal', 'himachal pradesh', 'hp','help himachal pradesh','himachal pradesh help'],
            'jharkhand': ['jharkhand','help jharkhand','jharkhand help'],
            'karnataka': ['karnataka', 'karnatka','help karnataka','karnataka help'],
            'kerala': ['kerala', 'kerela','help kerala','kerala help'],
            'madhya pradesh': ['madhya pradesh', 'madhya', 'mp','help madhya pradesh','madhya pradesh help'],
            'maharashtra': ['maharashtra', 'maharastra','help maharashtra','maharashtra help'],
            'manipur': ['manipur','help manipur','manipur help'],
            'meghalaya': ['meghalaya','help meghalaya','meghalaya help'],
            'mizoram': ['mizoram','help mizoram','mizoram help'],
            'nagaland': ['nagaland','help nagaland','nagaland help'],
            'odisha': ['odisha', 'orissa','help odisha','odisha help'],
            'punjab': ['punjab','help punjab','punjab help'],
            'rajasthan': ['rajasthan', 'rajasthan','help rajasthan','rajasthan help'],
            'sikkim': ['sikkim','help sikkim','sikkim help'],
            'tamil nadu': ['tamil nadu', 'tamilnadu', 'tamil nadu', 'tn','help tamil nadu','tamil nadu help'],
            'telangana': ['telangana', 'telengana','help telangana','telangana help'],
            'tripura': ['tripura','help tripura','tripura help'],
            'uttar pradesh': ['uttar pradesh', 'up', 'uttar pradesh','help uttar pradesh','uttar pradesh help'],
            'uttarakhand': ['uttarakhand', 'uttaranchal','help uttarakhand','uttarakhand help'],
            'west bengal': ['west bengal', 'wb', 'bengal','help west bengal','west bengal help']
        }
        
        for state, helpline in self.state_helplines.items():
            if state in message_lower:
                response = f"📍 {state.title()} Disaster Helpline Numbers:\n\n"
                response += f"🚨 State Emergency Numbers:\n"
                response += f"• {helpline}\n\n"
                response += f"📞 Additional Emergency Contacts:\n"
                response += f"• Police: 100\n"
                response += f"• Fire: 101\n"
                response += f"• Ambulance: 102\n"
                response += f"• National Disaster Management: 108\n"
                response += f"• NDRF: 011-24363260\n"
                response += f"• NDMA: 011-26701728\n\n"
                response += f"💡 Available 24/7 for disaster-related emergencies"
                return response
        return None
    
    def detect_disaster_type(self, message):
        message_lower = message.lower()
        
        disaster_help_patterns = {
            'earthquake': ['earthquake help', 'help earthquake', 'earthquake safety', 'earthquake instructions'],
            'flood': ['flood help', 'help flood', 'flood safety', 'flood instructions'],
            'cyclone': ['cyclone help', 'help cyclone', 'cyclone safety', 'cyclone instructions'],
            'tsunami': ['tsunami help', 'help tsunami', 'tsunami safety', 'tsunami instructions'],
            'landslide': ['landslide help', 'help landslide', 'landslide safety', 'landslide instructions'],
            'fire': ['fire help', 'help fire', 'fire safety', 'fire instructions', 'fire protocol'],
            'drought': ['drought help', 'help drought', 'drought safety', 'drought instructions']
        }
        
        for disaster, patterns in disaster_help_patterns.items():
            if any(pattern in message_lower for pattern in patterns):
                return self.get_disaster_instructions(disaster)
        
        disaster_keywords = {
            'earthquake': ['earthquake', 'quake', 'seismic', 'tremor', 'shaking','help earthquake','earthquake help'],
            'flood': ['flood', 'flooding', 'water', 'rain', 'monsoon','help flood','flood help'],
            'cyclone': ['cyclone', 'storm', 'hurricane', 'typhoon', 'wind','help cyclone','cyclone help'],
            'tsunami': ['tsunami', 'tidal wave', 'sea wave','help tsunami','tsunami help'],
            'landslide': ['landslide', 'mudslide', 'rock fall', 'slope','help landslide','landslide help'],
            'fire': ['fire', 'burning', 'blaze', 'flame','help fire','fire help'],
            'drought': ['drought', 'water shortage', 'scarcity','help drought','drought help']
        }
        
        for disaster, keywords in disaster_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                return self.get_disaster_instructions(disaster)
        
        return None
    
    def get_disaster_instructions(self, disaster_type):
        if disaster_type in self.disaster_instructions:
            instructions = self.disaster_instructions[disaster_type]
            response = "\n".join(instructions)
            response += f"\n\n📞 EMERGENCY CONTACTS:\n"
            response += f"• Police: 100\n"
            response += f"• Fire: 101\n"
            response += f"• Ambulance: 102\n"
            response += f"• Disaster Management: 108\n"
            response += f"• NDRF: 011-24363260\n"
            response += f"• NDMA: 011-26701728"
            return response
        return None
    
    def get_national_helplines(self):
        response = "🇮🇳 NATIONAL EMERGENCY HELPLINES:\n\n"
        for service, number in self.national_helplines.items():
            response += f"• {service.title()}: {number}\n"
        
        response += "\n📱 DISASTER MANAGEMENT CONTACTS:\n"
        response += "• NDRF (National Disaster Response Force): 011-24363260\n"
        response += "• NDMA (National Disaster Management Authority): 011-26701728\n"
        response += "• IMD (India Meteorological Department): 011-24629721\n"
        response += "• State-wise helplines: Varies by state (1070, 1077, 1078, 108, 112)\n\n"
        response += "These numbers are available 24/7 for emergency assistance."
        return response
    
    def get_general_helplines(self):
        response = "📞 EMERGENCY HELPLINE NUMBERS:\n\n"
        response += "🚨 IMMEDIATE EMERGENCY:\n"
        response += "• Police: 100\n"
        response += "• Fire: 101\n"
        response += "• Ambulance: 102\n"
        response += "• Disaster Management: 108\n\n"
        
        response += "👥 SPECIALIZED HELPLINES:\n"
        response += "• Women Helpline: 1091\n"
        response += "• Child Helpline: 1098\n"
        response += "• Senior Citizen Helpline: 1090\n\n"
        
        response += "🏛️ DISASTER MANAGEMENT:\n"
        response += "• NDRF: 011-24363260\n"
        response += "• NDMA: 011-26701728\n"
        response += "• State Disaster Helpline: 1077\n\n"
        
        response += "For state-specific help, mention your state name."
        return response
    
    def get_default_response(self):
        response = "I'm here to help with disaster-related emergencies in India.\n\n"
        response += "I can assist you with:\n"
        response += "• State-wise disaster helpline numbers\n"
        response += "• Safety instructions for different disasters\n"
        response += "• Emergency contact numbers\n"
        response += "• Disaster preparedness advice\n\n"
        response += "📍 **State-Specific Help Available!**\n"
        response += "Please tell me which state you're in for personalized assistance:\n"
        response += "• Just type your state name (e.g., 'Maharashtra', 'Kerala', 'Tamil Nadu')\n"
        response += "• Or mention it in a sentence (e.g., 'I'm in Gujarat and need help')\n\n"
        response += "Other options:\n"
        response += "• Type disaster name for safety instructions\n"
        response += "• 'help [disaster]' or '[disaster] help' (e.g., 'help fire', 'earthquake help')\n"
        response += "• 'emergency' for immediate help\n"
        response += "• 'helpline' for contact numbers"
        return response

def main():
    root = tk.Tk()
    app = DisasterResponseChatbot(root)
    root.mainloop()

if __name__ == "__main__":
    main()

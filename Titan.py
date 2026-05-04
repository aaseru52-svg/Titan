import json
import math
import re
import threading
import time
import random
import os

class TitanSystemV18:
    def __init__(self, memory_file="titan_memory.json"):
        self.version = "18.5 (Global Edition)"
        self.memory_file = memory_file
        self.is_running = True
        self.responses = [
            "Processing at Titan speed...",
            "Your command is being handled.",
            "Analysis complete. Here is the result:",
            "Smart question! Let me think..."
        ]
        self.memory = self._load_memory()
        
        # Start background monitoring thread
        self.monitor_thread = threading.Thread(target=self._background_monitor, daemon=True)
        self.monitor_thread.start()

    def _load_memory(self):
        """Load the brain/memory from a JSON file"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {"history": [], "patterns": {}}
        return {"history": [], "patterns": {}}

    def _save_memory(self):
        """Save interactions to memory"""
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, indent=4, ensure_ascii=False)

    def _background_monitor(self):
        """Background task for system monitoring"""
        while self.is_running:
            # You can add file checking or update logic here
            time.sleep(60)

    def solve_math(self, expression):
        """Mathematical and Logical Engine"""
        clean_expr = re.sub(r'[^0-9+\-*/().^%]', '', expression)
        try:
            # Convert ^ to ** for Python power syntax
            result = eval(clean_expr.replace('^', '**'))
            return f"Math Result: {result}"
        except:
            return "Error: Could not process math expression. Check your syntax."

    def process_input(self, user_input):
        """Main core to process all user inputs"""
        user_input_lower = user_input.lower()
        
        # 1. Exit Commands
        if user_input_lower in ["exit", "stop", "quit"]:
            self.is_running = False
            return "Shutdown initiated. Goodbye!"

        # 2. Math Operations Detection
        if any(char in user_input for char in "+-*/^%"):
            response = self.solve_math(user_input)
        
        # 3. Time Functions
        elif "time" in user_input_lower:
            response = f"Current time is: {time.strftime('%H:%M:%S')}"
            
        # 4. General Smart Interaction
        else:
            prefix = random.choice(self.responses)
            response = f"{prefix}\nI am Titan, your intelligent system. How can I assist you today?"

        # Save the interaction to learn
        self.memory["history"].append({"user": user_input, "titan": response})
        self._save_memory()
        
        return response

# --- Initialize and Run Titan ---
if __name__ == "__main__":
    titan = TitanSystemV18()
    print(f"--- Titan Core V{titan.version} Online ---")
    print("Type 'exit' to stop the system.")

    while titan.is_running:
        try:
            cmd = input("\nUser >> ")
            if not cmd.strip():
                continue
                
            # Visual thinking effect
            print("Titan is thinking...", end="\r")
            time.sleep(0.5)
            
            output = titan.process_input(cmd)
            print(f"Titan: {output}")
            
        except KeyboardInterrupt:
            break

    print("\n[Titan System Shutdown Successfully]")

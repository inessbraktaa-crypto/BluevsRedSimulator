import tkinter as tk   # tk = tkinter module
from tkinter import ttk, messagebox, scrolledtext # ttk = themed tkinter widgets, messagebox = to show pop-up messages, scrolledtext = text widget with scrollbar
from PIL import Image, ImageTk # PIL = Python Imaging Library, ImageTk = to use images in tkinter
import random # to generate random choices for the bot



class BlueVSRed: # create the template (=class) BlueVSRed
    def __init__(self, root): # configuration of the main window 
        self.root = root # root = main window of the application 
        self.root.title("BlueVSRed") # title of the window
        self.root.geometry("1000x600") # size when opened
        self.root.minsize(500,300) # minimum size of the window
        self.setup() # to activate the setup function




    def setup(self): # to build the UI (define the setup function)

        
        
# 1.SCROLLABLE PAGE
# 2.FRAME (in the canvas) 
# 3.MOUSE WHEEL SCROLL
# 4.GRID CONFIG
# 5.STYLES
# 6.RECTANGULAR FIGHT ZONE
# 7.IMAGE IN THE FIGHT ZONE
# 8.WELCOME MESSAGE LABEL 
# 9.HP BARS
# 10.PLAYER ACTION AREA
# 11.AVAILABLE ACTIONS OF THE BOT (ATTACKS) 
# 12.DICTIONNARY ATTACK-DEFENSE
# 13.PLAYER DEFENSE BUTTONS
# 14.START BUTTON
# 15.RIGHT FRAME (FOR LOGS)
# 16.SCROLLEDTEXT WIDGET (FOR LOGS)
# 17.LOGS
# 18.START GAME LOGIC
# 19.BOT ATTACK LOGIC
# 20.PLAYER DEFENSE LOGIC
# 21.END GAME LOGIC


# 1.SCROLLABLE PAGE, Scrollable main area: 1.1container + 1.2canvas and vertical scrollbar
        container = ttk.Frame(self.root) # main container frame
        container.grid(row=0, column=0, sticky='nsew') # sticky='nsew' = to make the container expand in all directions when resizing the window
        self.root.columnconfigure(0, weight=1) # make the container expand when resizing the window
        self.root.rowconfigure(0, weight=1) # the same as up line but for rows

        canvas = tk.Canvas(container, highlightthickness=0) # a canva is where we can draw shapes, images, etc./ container: is where to place the canvas/ highlightthickness=0: no border
        vscroll_main = ttk.Scrollbar(container, orient='vertical', command=canvas.yview) # vertical scrollbar for the canvas/ command=canvas.yview: to link the scrollbar to the canvas/ container: is where to place the scrollbar
        canvas.configure(yscrollcommand=vscroll_main.set) # link the scrollbar to the canvas. the yscrollcommand is used to update the scrollbar when the canvas is scrolled




# 2.FRAME OF THE UI INSIDE THE CANVAS
        main_frame = ttk.Frame(canvas, padding=10) # frame that holds the UI. main_frame = main interface, canvas = where to place the frame, padding=10: space between the frame and its content
        window_id = canvas.create_window((0,0), window=main_frame, anchor='nw') # create a window inside the canvas to hold the main_frame/ (0,0): position of the window/ anchor='nw': to anchor the window to the top-left corner of the canvas

        def _on_frame_config(event): # this function is called when the 'main_frame' is resized
            canvas.configure(scrollregion=canvas.bbox('all')) # update the scrollregion of the canvas to include the entire main_frame

        def _on_canvas_config(event): # this function is called when the 'canvas' is resized
            # keep frame width (sync with canvas)
            try: # try/except: to avoid errors if the window_id is not present
                canvas.itemconfigure(window_id, width=event.width) # set the width of the main_frame to the width of the canvas
            except Exception: # pass if error occurs
                pass

        main_frame.bind('<Configure>', _on_frame_config) # bind (="lier"): when the main_frame is resized, call the _on_frame_config function, <Configure> = event that is triggered when the widget is resized
        canvas.bind('<Configure>', _on_canvas_config) # when the canvas is resized, call the _on_canvas_config function




# 3.MOUSE WHEEL SCROLLING
        def _on_mousewheel(event): # when the mouse wheel is scrolled
            canvas.yview_scroll(int(-1*(event.delta/120)), 'units') # scroll the canvas vertically/ event.delta: amount of scrolling/ 'units': scroll by units (-1 or 1)/ delta is positive when scrolling up and negative when scrolling down, delta is a multiple of 120 on Windows
        canvas.bind('<Enter>', lambda e: canvas.bind_all('<MouseWheel>', _on_mousewheel)) # when the mouse enters the canvas, bind the mouse wheel to the _on_mousewheel function
        canvas.bind('<Leave>', lambda e: canvas.unbind_all('<MouseWheel>')) # when the mouse leaves the canvas, unbind the mouse wheel, # lambda sert a




# 4.GRID CONFIGURATION
        canvas.grid(row=0, column=0, sticky='nsew') # place the canvas in the container/ sticky='nsew' = to make the canvas expand in all directions when resizing the window
        vscroll_main.grid(row=0, column=1, sticky='ns') # place the scrollbar to the right of the canvas/ sticky='ns' = to make the scrollbar expand vertically when resizing the window
        container.columnconfigure(0, weight=1) # make the canvas expand when resizing the window
        container.rowconfigure(0, weight=1) 

        main_frame.columnconfigure(0, weight=1) # resize column of main_frame
        main_frame.rowconfigure(0, weight=0)    # 0= the title won't expand when resizing
        main_frame.rowconfigure(1, weight=0)    # 1= the fight area (line 1) won't neither (it will only expand horizontally)
        main_frame.rowconfigure(2, weight=1)    # 2= the space below (line 2) will expand when resizing the window




# 5.STYLES
        style = ttk.Style(self.root) # it creates a style object that will manage the styles of the interface
        style.theme_use('clam')      # theme 'clam' is to apply customized colors easierly (default themes may not support all color changes)
        style.configure("Title.TLabel", foreground="#331a45", font=("Helvetica", 24, "bold")) # style for the label "Title"/ TLabel = ttk Label

        style.configure("Blue.Horizontal.TProgressbar", troughcolor="#dfefff", background="#0088ff") # troughcolor = color of the empty part/ background = color of the filled part
        style.configure("Red.Horizontal.TProgressbar", troughcolor="#ffecec", background="#ff1e00")

        style.configure("Large.TButton", font=("Helvetica", 12, "bold"), padding=(12, 8)) # style for large buttons/ padding=(12,8): space inside the button (horizontal, vertical)
        style.configure("Red.TButton", font=("Arial", 12), padding=10, foreground="white", background="red") # speific style for one red button (ATTACK BACK!)


        title_label = ttk.Label(main_frame, text="Blue vs Red Simulator", style="Title.TLabel") # Title label at the top of the window. main_frame = where to place the label
        title_label.grid(row=0, column=0, pady=(0,20), sticky="n") # pady = space above and below the label/ sticky="n" = to center the label at the top of the frame. (n= north)





# 6.RECTANGULAR FIGHT ZONE (under the title)
        combat_frame = tk.Frame(main_frame, bg="#A36ABF", highlightbackground="#534a5a", highlightthickness=4, width=1600, height=400) # bg = background color/ highlightbackground = border color/ highlightthickness = border thickness
        combat_frame.grid(row=1, column=0, padx=1, pady=(0.50), sticky="we") # padx= space on the left and right of the frame/ pady = space above and below the frame/ sticky=where the frame expand horizontally
         
        main_frame.grid_columnconfigure(0, weight=1) # to make the combat_frame expand horizontally when resizing the window
        combat_frame.grid_propagate(False) # if not desactivated: the frame would resize itself to fit its content and not keep the defined size


# 7.IMAGE IN THE FIGHT ZONE 
        img = Image.open(r"images\VraiImage.png") # open the image file/ mode='r' = read mode
        img = img.resize((200, 180), Image.LANCZOS) #image.lanczos = high-quality downsampling filter
        
        self.blue_sprite = ImageTk.PhotoImage(img)
        self.blue_sprite_label = tk.Label(combat_frame, image=self.blue_sprite, bg="#A36ABF")

       
        img = Image.open(r"images\Redimage.png") # open the image file/ mode='r' = read mode
        img = img.resize((250, 150), Image.LANCZOS) #image.lanczos = high-quality downsampling filter
        
        self.red_sprite = ImageTk.PhotoImage(img)
        self.red_sprite_label = tk.Label(combat_frame, image=self.red_sprite, bg="#A36ABF")



# 8.WELCOME MESSAGE LABEL (removed when game starts)
        self.welcome_label = tk.Label(combat_frame, text="Click the button Start below!", bg="#A36ABF", fg="#ffffff", font=("Helvetica", 25, "bold"), wraplength=1000) # wraplength=1000: to wrap the text if it's too long
        self.welcome_label.place(relx=0.5, rely=0.5, anchor='center')  # place the label at the center of the combat_frame/ relx=0.5: 50% from the left/ rely=0.5: 50% from the top/ anchor='center': to center the label
        self.welcome_label2 = tk.Label(combat_frame, text="Defend your system against cyber attacks! (hint: stay ethical)", bg="#A36ABF", fg="#ffffff", font=("Helvetica", 15), wraplength=800)
        self.welcome_label2.place(relx=0.5, rely=0.6, anchor='center')  # place the label at the center of the combat_frame/ relx=0.5: 50% from the left/ rely=0.6: 60% from the top/ anchor='center': to center the label



# 9.HP BARS 

    # FRAME INSIDE THE FIGHT ZONE
        hp_frame = ttk.Frame(combat_frame, padding=(8,8)) # create a frame inside combat_frame to hold the HP bars
        hp_frame.grid(row=0, column=0, sticky="nswe") # place the hp_frame at the top of combat_frame (0.0)/ sticky="we" = to make it expand horizontally
        combat_frame.grid_columnconfigure(0, weight=1) # weight=1 to make hp_frame expand horizontally when resizing combat_frame
        
        hp_frame.columnconfigure(0, weight=1) # 0 = first column (Blue team)/ weight=1 to make it expand when resizing
        hp_frame.columnconfigure(1, weight=1) # 1 = second column (Red team)/ weight=1 to make it expand when resizing



    # BLUE TEAM HP BAR
        self.blue_hp = ttk.Progressbar(hp_frame, orient='horizontal', mode='determinate', maximum=100, value=100, style="Blue.Horizontal.TProgressbar") # create a progress bar for the blue team inside hp_frame/ maximum=100 (max HP)/ value=100 (current HP)
        self.blue_hp.grid(row=0, column=0, sticky="we", padx=(0,10), pady=(5,0)) # place the blue_hp bar at row 0, column 0 of hp_frame/ sticky="we" = to make it expand horizontally/ padx= space on the right of the bar/ pady= space below the bar
            # LABEL BLUE TEAM HP
        self.blue_label = ttk.Label(hp_frame, text="Blue Team : 100 / 100") # create a label for the blue team HP inside hp_frame
        self.blue_label.grid(row=1, column=0, sticky="w", padx=(0,10), pady=(6,0)) # place the blue_label at row 1, column 0 of hp_frame/ sticky="w" = to align it to the left/ padx= space on the right of the label/ pady= space below the label

        self.blue_max_hp = 100 # maximum HP for the blue team


    # RED TEAM HP BAR
        self.red_hp = ttk.Progressbar(hp_frame, orient='horizontal', mode='determinate', maximum=100, value=100, style="Red.Horizontal.TProgressbar") # create a progress bar for the red team inside hp_frame in the same way as the blue team
        self.red_hp.grid(row=0, column=1, sticky="we", padx=(10,0), pady=(5,0)) # place the red_hp bar at row 0, column 1 of hp_frame/ padx= space on the left of the bar
            # LABEL RED TEAM HP
        self.red_label = ttk.Label(hp_frame, text="Red Team : 100 / 100")  # create a label for the red team HP inside hp_frame
        self.red_label.grid(row=1, column=1, sticky="e", padx=(10,0), pady=(6,0)) # place the red_label at row 1, column 1 of hp_frame/ sticky="e" = to align it to the right/ padx= space on the left of the label/ pady= space below the label

        self.red_max_hp = 100  # maximum HP for the red team




# 10.PLAYER ACTION AREA: (left = attack buttons, middle = spacer, right = logs)
        player_frame = ttk.Frame(main_frame) # frame that holds the buttons and logs
        player_frame.grid(row=2, column=0, sticky="nsew", pady=10) # place the player_frame below the combat_frame/ sticky="nsew" = to make it expand in all directions when resizing the window/ pady= space above and below the frame
        # give the left column (buttons), spacer and logs priority to expand; ensure logs take more space by default
        
        player_frame.columnconfigure(0, weight=1)  # left: buttons expands
        player_frame.columnconfigure(1, weight=1)  # middle: spacer between buttons and logs expands
        player_frame.columnconfigure(2, weight=2, minsize=360)  # right: logs (min width increased so scrollbar remains visible)


    # Left frame (buttons)
        left_frame = ttk.Frame(player_frame) # frame for the buttons area
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0,10)) # place the left_frame at row 0, column 0 of player_frame/ sticky="nsew" = to make it expand in all directions when resizing the window/ padx= space on the right of the frame
        left_frame.columnconfigure(0, weight=1) # make the column expand when resizing

        left_frame.rowconfigure(0, weight=1)   # buttons area
        left_frame.rowconfigure(1, weight=0)   # start button row


    # Container that will hold the buttons, fixed to the left side
        buttons_container = ttk.Frame(left_frame) # frame for the buttons
        buttons_container.grid(row=0, column=0, sticky='nw', pady=10) # place the buttons_container at row 0, column 0 of left_frame/ sticky='nw' = to anchor it to the top-left corner/ pady= space above and below the frame




# 11.AVAILABLE ACTIONS OF THE BOT (attacks)
        self.bot_actions = [
            "Phishing Email", 
            "Malware Installation", 
            "Keylogger", 
            "Ransomware Encryption", 
            "Brute Force", 
            "SQL Injection", 
            "DDoS Attack", 
            "Password Spraying", 
            "Man-in-the-Middle", 
            "Worm", 
            "Trojan", 
            "Cross Site Scripting", 
            "Shoulder Surfing: YOUR PASSWORD IS COMPROMISED", 
            "[ALERT] Suspicious login attempts detected", 
            "Someone wants you to click on his link", 
            "Fake Software Update", 
            "USB Malware Infection"
            ]
        


    # attack points associated to each attack
        self.attack_points = {
            "Phishing Email": 20,
            "Malware Installation": 20,
            "Keylogger": 15,
            "Ransomware Encryption": 10,
            "Brute Force": 15,
            "SQL Injection": 15,
            "DDoS Attack": 25,
            "Password Spraying": 15,
            "Man-in-the-Middle": 25,
            "Worm": 15,
            "Trojan": 15,
            "Cross Site Scripting": 25,
            "Shoulder Surfing: YOUR PASSWORD IS COMPROMISED": 10,
            "[ALERT] Suspicious login attempts detected": 15,
            "Someone wants you to click on his link": 25,
            "Fake Software Update": 20,
            "USB Malware Infection": 15
            }
        

        



    # actions available to the player (defenses) -> these become the buttons
        self.player_actions = [
            "Filter Emails", 
            "Scan Virus", 
            "Input Encryption", 
            "Backup Data", 
            "Reset Password", 
            "Input Validation", 
            "Block IP", 
            "Firewall", 
            "Threat Analysis", 
            "VPN", 
            "Check Logs", 
            "Update Policy",
            "Disable USB Ports",
            "Click on link", 
            "Do nothing", 
            "ATTACK BACK!"
            ]
        




# 12.DICTIONNARY ATTACK-DEFENSE
        # which defense counters which attack
        self.counter_map = {
            "Phishing Email": ["Filter Emails"], 
            "Malware Installation": ["Scan Virus", "Filter Emails"], 
            "Keylogger": ["Input Encryption", "Scan Virus"], 
            "Ransomware Encryption": ["Backup Data", "Scan Virus"], 
            "Brute Force": ["Reset Password", "Block IP"], 
            "SQL Injection": ["Input Validation"], 
            "DDoS Attack": ["Block IP", "Filter Emails"], 
            "Password Spraying": ["Reset Password"], 
            "Man-in-the-Middle": ["VPN", "Input Encryption"], 
            "Worm": ["Scan Virus", "Firewall"], 
            "Trojan": ["Scan Virus", "Firewall"], 
            "Cross Site Scripting": ["Input Validation", "Check Logs"], 
            "Shoulder Surfing: YOUR PASSWORD IS COMPROMISED": ["Input Encryption", "Reset Password"], 
            "[ALERT] Suspicious login attempts detected": ["Check Logs", "Block IP"],
            "Someone wants you to click on his link": ["Do nothing"],
            "Fake Software Update": ["Update Policy", "Scan Virus"],
            "USB Malware Infection": ["Disable USB Ports", "Scan Virus"]
            }

        self.attack_buttons = [] # create a list to store the attack/defense buttons
        




# 13.PLAYER DEFENSE BUTTONS
        # buttons creation for player defenses
        cols = 4  # use 4 columns so buttons fit better horizontally
        for i, action in enumerate(self.player_actions): # enumerate: to get the index and the value of the list, self.player_actions = list of actions of the player
            r, c = divmod(i, cols) # divmod: to get the row and column index for each button based on its position in the list, r = row, c = column
        
        # create the button
            btn = ttk.Button(buttons_container, text=action, style="Red.TButton" if action == "ATTACK BACK!" else "Large.TButton", command=lambda a=action: self.player_choice(a)) #text=action: button label/ style: special style for "ATTACK BACK!"/ command: when the button is clicked, call the player_choice function with the action as argument
            
            btn.grid(row=r, column=c, padx=6, pady=6, sticky="ew") # place the button in the grid/ padx= space on the left and right of the button/ pady= space above and below the button/ sticky="ew" = to make it expand horizontally
            btn.grid_remove()  # hidden before start
            self.attack_buttons.append(btn) # add the button to the list of attack_buttons
        # ensure columns expand evenly so buttons remain visible
        for c in range(cols):
            buttons_container.columnconfigure(c, weight=1) # make each column expand when resizing
        




# 14.START BUTTON
        # Start button placed under the buttons area (use grid, so grid()/grid_remove() works properly)
        self.start_button = ttk.Button(left_frame, text="Start", style="Large.TButton", command=self.start_game) # command=self.start_game: when the button is clicked, call the start_game function
        self.start_button.grid(row=1, column=0, sticky='w', padx=6, pady=6) # place the start_button at row 1, column 0 of left_frame/ sticky='w' = to align it to the left/ padx= space on the left and right of the button/ pady= space above and below the button



# 15.RIGHT FRAME (FOR LOGS)
        right_frame = ttk.Frame(player_frame) # frame for the logs area
        right_frame.grid(row=0, column=2, sticky="nsew", padx=(10,0)) # place the right_frame at row 0, column 2 of player_frame/ sticky="nsew" = to make it expand in all directions when resizing the window/ padx= space on the left of the frame
        right_frame.columnconfigure(0, weight=1) # make the column expand when resizing
        right_frame.rowconfigure(0, weight=1)  # make the row expand when resizing



# 16.SCROLLEDTEXT WIDGET (FOR LOGS)
        self.log_widget = scrolledtext.ScrolledText(right_frame, wrap='word', state='disabled', width=64, height=18) # wrap='word': to wrap text by words/ state='disabled': to prevent user from editing the logs/ width=64: width in characters/ height=18: height in lines
        self.log_widget.grid(row=0, column=0, sticky="nsew", padx=(6,0)) # place the log_widget at row 0, column 0 of right_frame/ sticky="nsew" = to make it expand in all directions when resizing the window/ padx= space on the left of the widget

        

# 17.LOGS 
    # function to add logs in the ScrolledText widget
    def add_log(self, text, color="black"): # function to add logs in the ScrolledText widget, text = log to add
        # insert in ScrolledText and autoscroll
        timestamped = text # a timestamp is a way to record the time at which an event occurred, here we just use the text as is
        try: # try/except: to avoid errors if the widget is not present
            self.log_widget.tag_config(color, foreground=color) # configure the tag with the specified color
            self.log_widget.configure(state='normal') # state='normal' to allow writing in the widget
            self.log_widget.insert('end', timestamped + '\n', color) # insert the log at the end of the widget 
            self.log_widget.see('end') # autoscroll to the end, it's to see the latest log
            self.log_widget.configure(state='disabled') # state='disabled' to prevent user from editing the logs (security)

        except Exception: # this is to avoid errors if the widget is not present
            print(timestamped) # print the log in the console as a fallback

    # function to clear the logs    
    def reset_logs(self): # function to clear the logs in the ScrolledText widget
        try:
            self.log_widget.configure(state='normal') # state='normal' to allow writing in the widget
            self.log_widget.delete('1.0', 'end') # delete all the content in the widget from line 1, character 0 to the end
            self.log_widget.configure(state='disabled') # state='disabled' to prevent user from editing the logs 
        except Exception:
            pass # pass if error occurs

# 18.START GAME LOGIC
    # Start game function
    def start_game(self): # when the Start button is pressed this function is called
        self.reset_logs()
        # ensure button label is normal while starting
        try:
            self.start_button.config(text="Start") # set the button label to "Start"
        except Exception: 
            pass

    # Hide welcome message
        self.welcome_label.place_forget()
        self.welcome_label2.place_forget()

    # show blue team image
        self.blue_sprite_label.place(relx=0.80, rely=0.5, anchor='center')  # place the label at 25% from the left and 50% from the top of the combat_frame/ anchor='center': to center the label
        self.red_sprite_label.place(relx=0.20, rely=0.7, anchor='center')  # place the label at 75% from the left and 50% from the top of the combat_frame/ anchor='center': to center the label

    # reset HP values and UI
        self.blue_hp_val = 100 # reset blue team HP
        self.red_hp_val = 100 # reset red team HP
        self.blue_hp['value'] = self.blue_hp_val # update blue team HP bar
        self.red_hp['value'] = self.red_hp_val # update red team HP bar
        self.blue_label.config(text=f"Blue Team : {self.blue_hp_val} / {self.blue_max_hp}") # update blue team HP label
        self.red_label.config(text=f"Red Team : {self.red_hp_val} / {self.red_max_hp}") # update red team HP label


    # show attack buttons and enable them
        self.start_button.grid_remove() # hide the start button
        for btn in self.attack_buttons: # show and enable all attack buttons
            btn.state(["!disabled"]) # enable the button
            btn.grid()  # show the button


    # start the first attack from the bot
        self.robot_attack() # start the first attack from the bot



# 19.BOT ATTACK LOGIC
    def robot_attack(self): # function for the bot to choose an attack
        prev = getattr(self, "current_attack", None) # get the previous attack to avoid repetition, None if not present
        attack = random.choice(self.bot_actions) # choose a random attack from the bot_actions list
        while attack == prev and len(self.bot_actions) > 1: # if the attack is the same as the previous one and there are more than 1 attack available
            attack = random.choice(self.bot_actions) # choose a new random attack

        self.current_attack = attack # set the current attack
        self.round_active = True # to allow player to choose a defense
        for btn in self.attack_buttons: # enable all attack buttons
            btn.state(["!disabled"]) # enable the button
        self.add_log(f"Hacker attack: {attack}", "red") # log the attack
        self.add_log("Select your defense!", "blue") # prompt the player to choose a defense


# 20.PLAYER DEFENSE LOGIC
    def player_choice(self, action): # function called when the player chooses a defense
        if not self.round_active: # if the round is not active, ignore the click
            return  # this prevents multiple clicks during the same round

        self.round_active = False # it disables further clicks until the next attack
        for btn in self.attack_buttons: # disable all attack buttons
            btn.state(["disabled"])

        # Special action: ATTACK BACK! deals heavy damage to the hacker
        if action == "ATTACK BACK!":
            damage = 100
            # Player attacks back but suffers consequences: Blue loses HP
            self.add_log(f"You attacked back! You take {damage} HP damage. YOU MUST STAY ETHICAL!", "purple") # log the attack back
            self.blue_hp_val = max(0, self.blue_hp_val - damage) # update blue team HP, ensure it doesn't go below 0
            self.blue_hp['value'] = self.blue_hp_val # update blue team HP bar after attack back
            self.blue_label.config(text=f"Blue Team : {self.blue_hp_val} / {self.blue_max_hp}") # update blue team HP label
            self.red_label.config(text=f"Red Team : {self.red_hp_val} / {self.red_max_hp}") # update red team HP label
            if self.blue_hp_val <= 0: # if blue team HP is 0 or less, end the game
                self.end_game() 
                return # exit the function to prevent further processing

        else: # normal defense processing
            # it detects if the defense is correct against the current attack
            correct_defenses = self.counter_map.get(self.current_attack, []) # get the list of correct defenses for the current attack, empty list if not found
            damage = self.attack_points.get(self.current_attack, 20)  # default damage is 20 if attack not found
            if action in correct_defenses: # if the chosen defense is correct
                # red team (hacker) loses HP
                self.add_log(f"Good defense ({action}) — the hacker loses {damage} HP.", "green") # log the successful defense
                self.red_hp_val = max(0, self.red_hp_val - damage) # update red team HP, ensure it doesn't go below 0
                self.red_hp['value'] = self.red_hp_val # update red team HP bar
                self.red_label.config(text=f"Red Team : {self.red_hp_val} / {self.red_max_hp}") # update red team HP label
                if self.red_hp_val <= 0: # if red team HP is 0 or less, end the game
                    self.end_game()
                    return
                
            else: # incorrect defense
                # Player (Blue) loses HP
                self.add_log(f"Bad defense ({action}) — you lose {damage} HP.", "orange")
                self.blue_hp_val = max(0, self.blue_hp_val - damage)
                self.blue_hp['value'] = self.blue_hp_val
                self.blue_label.config(text=f"Blue Team : {self.blue_hp_val} / {self.blue_max_hp}")
                if self.blue_hp_val <= 0:
                    self.end_game()
                    return

        # Update both HP labels after the round
        self.blue_label.config(text=f"Blue Team : {self.blue_hp_val} / {self.blue_max_hp}")
        self.red_label.config(text=f"Red Team : {self.red_hp_val} / {self.red_max_hp}")

        # next attack from the bot
        self.robot_attack()



# 21.END GAME LOGIC
    def end_game(self): # function to end the game
        # Determine winner based on HP first
        if getattr(self, "red_hp_val", 100) <= 0: # if red team HP is 0 or less
            result = "Blue wins!"
        elif getattr(self, "blue_hp_val", 100) <= 0:
            result = "GAME OVER: Red wins!"
                

    # it forces a UI update to ensure the final state is shown before the popup
        try:
            self.root.update() # update the UI to reflect the final state
        except Exception:
            pass

        self.add_log("Game Over! " + result) # log the game over message
        messagebox.showinfo("Result", result)


        for btn in self.attack_buttons: # disable all attack buttons
            btn.state(["disabled"])
        # permettre redémarrage: afficher le bouton en tant que "Restart"
        try:
            self.start_button.config(text="Restart")
        except Exception:
            pass
        self.start_button.grid()
        
        


def main(): # without this function the GUI would open and close immediately
    root = tk.Tk() # create the main window
    app = BlueVSRed(root) # app = instance of the BlueVSRed class, instance= specific object created from a class
    root.mainloop() # mainloop() = keeps the window open and waits for user interaction

if __name__ == "__main__": # __name_ = "__main__" means that this code block will only run if this script is executed directly, not if it is imported as a module in another script
    main() # call the main function to start the application, if it is not here the GUI would not open

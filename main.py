from customtkinter import *
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import askyesno
from PIL import Image
import pyrebase 
import customtkinter
from datetime import datetime

firebaseConfig = { 
  "apiKey" : "",
  "authDomain" : "banking-application-1a9d4.firebaseapp.com",
  "databaseURL" : "https://banking-application-1a9d4-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "projectId" : "banking-application-1a9d4",
  "storageBucket" : "banking-application-1a9d4.firebasestorage.app",
  "messagingSenderId" : "386900208260",
  "appId": "1:386900208260:web:bf9f1a46d35d696da570d1",
  "measurementId": "G-BGMTK49WXZ"
}


firebase = pyrebase.initialize_app(firebaseConfig)


db = firebase.database()

global acc
acc = {}

def fetch_data_from_firebase():
  global acc
  accounts_data = db.child("accounts").get().val()
  if accounts_data:
      acc = accounts_data

def update_firebase_database():
  global acc
  db.child("accounts").set(acc)
  fetch_data_from_firebase
 
fetch_data_from_firebase()

def main():
  global root
  root = CTk()
  root.title("Bank Application")
  root.geometry("900x500")
  root.configure(bg="images/background.jpeg")
  root.maxsize(900,500)
  root.minsize(900,500)
  root._set_appearance_mode("Dark")
  
  def welcome():
    welcome_frame = CTkFrame(root, height=500, width=900, bg_color="transparent", fg_color="transparent")
    welcome_frame.place(x=0,y=0)
    
    imgbackl = CTkImage(dark_image=(Image.open("images/welcomebg.png")),size=(900, 500))
    img2 = CTkLabel(welcome_frame, image=imgbackl, text="")
    img2.place(x=0, y=0)
    
    CTkButton(welcome_frame, text="Sign In", width=150, height=30,text_color="black",fg_color="#e0e0e0",border_color="black",font=("Calibri",14,"bold"),border_width=1,hover_color="#b5b5b5", corner_radius=15, bg_color="black", command=SignIn).place(x=458,y=349)
    CTkButton(welcome_frame, text="Sign Up", width=150, height=30,text_color="white",border_color="white",fg_color="black",font=("Calibri",14,"bold"),border_width=1,hover_color="#0f0f0f", corner_radius=15, bg_color="black", command=SignUp).place(x=282,y=350)
  
  
  def homefn():
    global userid
    # userid = "rockindp"
    global pinval
    global tinfo
    pinval = False
    
    #pfp+usr change name,pass,pin,email signout
    def confirmsignout():
      ans = askyesno(title="Sign Out", message="Do you want to Sign Out?")
      if ans:
        SignIn()
    
    def transaction():
      global userid
      global mode
      global amt
      global targetuser
      date = datetime.now().strftime("%Y-%m-%d")
      time = datetime.now().strftime("%H:%M")
      timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
      transaction_id = f"{userid[:5]}{timestamp}"
      balance = db.child("accounts").child(userid).child("BAL").get().val()
      #"date", "time", "mode", "from","to","mon","bal","txn"
      match mode:
        case "Deposit" :  tinfo = f"{date} {time} {mode} {userid} BankAccount ₹{amt} ₹{balance} {transaction_id}"
        case "Withdraw" : tinfo = f"{date} {time} {mode} BankAccount {userid} ₹{amt} ₹{balance} {transaction_id}"
        case "Transfer" : tinfo = f"{date} {time} {mode} {userid} {targetuser} ₹{amt} ₹{balance} {transaction_id}"

      newt = {f"{transaction_id}":f"{tinfo}"}
      db.child("accounts").child(userid).child("history").update(newt)
      if mode == "Transfer":
        balance = db.child("accounts").child(targetuser).child("BAL").get().val()
        tinfo = f"{date} {time} {mode} {userid} {targetuser} ₹{amt} ₹{balance} {transaction_id}"
        newt = {f"{transaction_id}":f"{tinfo}"}
        db.child("accounts").child(targetuser).child("history").update(newt)
    
    def input_pin():
      global pinval
      pinval = False
      dialog = customtkinter.CTkInputDialog(text="Enter PIN",
                                            title="PIN Authentication", 
                                            fg_color="#171717", 
                                            font=("Calibri",16,"bold"), 
                                            button_text_color="white", 
                                            button_fg_color="#3d3d3d", 
                                            button_hover_color="#474747")
      try:
        pin = int(dialog.get_input())
        if pin == acc[userid]["PIN"] :
          pinval = True
        else:
          messagebox.showerror("Try Again","Incorrect PIN")
          pinval = False
      except:
        messagebox.showinfo("Verification Failed","Something went wrong")
        pinval = False

      
    def home_click():
      fetch_data_from_firebase()
      homepage_frame = CTkFrame(f1,
                                width=520,
                                height=400,
                                bg_color="transparent", 
                                fg_color="transparent")
      
      homepage_frame.place(x=230,y=0)

      profile_frame = CTkFrame(homepage_frame,
                               width=250,
                               height=95, 
                               bg_color="transparent",
                               fg_color="#292929",
                               corner_radius=60)
      profile_frame.place(x=134,y=44)
      
      imgpfp = CTkImage(dark_image=(Image.open("images/pfp.png")), 
                        size=(70, 70))
      imgP1 = CTkLabel(profile_frame, image=imgpfp, text="", fg_color="#292929",bg_color="#0F0F0F")
      imgP1.place(x=14, y=12)   
      
      CTkLabel(profile_frame,
               text=f"{acc[userid]["User"]}",
               bg_color="transparent",
               fg_color="transparent",
               text_color="white",width=105,height=24, 
               font=("Calibri",20,"bold"), 
               anchor="w").place(x=94,y=29)
      
      CTkLabel(profile_frame,
               text=f"{userid}",
               bg_color="transparent",
               fg_color="transparent",width=51,
               text_color="white",height=15,
               font=("Calibri",13,"bold"),
               anchor="w").place(x=100,y=51)
      
      balance_frame = CTkFrame(homepage_frame,width=220,height=25,fg_color="#828282",bg_color="transparent",corner_radius=50)
      balance_frame.place(x=150,y=147)
      
      CTkLabel(balance_frame,
               text=f"Balance : ",
               bg_color="transparent",
               fg_color="transparent", width=50,
               text_color="black",height=20, 
               font=("Calibri",16,"bold"), 
               anchor="w").place(x=10,y=2)
      
      CTkLabel(balance_frame,
               text=f"{acc[userid]["BAL"]}",
               bg_color="transparent",
               fg_color="transparent",
               text_color="black",height=20, 
               font=("Calibri",18,"bold"), 
               anchor="w").place(x=80,y=1)
      
      CTkLabel(homepage_frame,
               text=f"Name",
               bg_color="transparent",
               fg_color="transparent",width=40,
               text_color="white",height=17, 
               font=("Calibri",14,"bold"),corner_radius=4).place(x=80,y=189)
      
      CTkLabel(homepage_frame,
               text=f"{acc[userid]["User"]}",
               bg_color="transparent",
               fg_color="#1D1D1D",width=200,
               text_color="white",height=25, 
               font=("Calibri",12,"bold"),corner_radius=4).place(x=134,y=186)
      
      CTkButton(homepage_frame,
                text="Change",
                bg_color="transparent",
                fg_color="#1D1D1D",width=125,
                text_color="white",height=25,hover_color="#212121",
                font=("Calibri",13,"bold"),corner_radius=40).place(x=350,y=186)
      
      CTkLabel(homepage_frame,
               text=f"Email",
               bg_color="transparent",
               fg_color="transparent",width=40,
               text_color="white",height=17, 
               font=("Calibri",14,"bold"),corner_radius=4).place(x=80,y=225)
      
      CTkLabel(homepage_frame,
               text=f"{acc[userid]["email"]}",
               bg_color="transparent",
               fg_color="#1D1D1D",width=200,
               text_color="white",height=25, 
               font=("Calibri",12,"bold"),corner_radius=4).place(x=134,y=225)
      
      CTkButton(homepage_frame,
                text="Change",
                bg_color="transparent",
                fg_color="#1D1D1D",width=125,
                text_color="white",height=25,hover_color="#212121",
                font=("Calibri",13,"bold"),corner_radius=40).place(x=350,y=225)

      CTkButton(homepage_frame,
                text="Password Change",
                bg_color="transparent",
                fg_color="#1D1D1D",width=150,
                text_color="white",height=25,hover_color="#212121",
                font=("Calibri",13,"bold"),corner_radius=40).place(x=109,y=271)
      
      CTkButton(homepage_frame,
                text="PIN Change",
                bg_color="transparent",
                fg_color="#1D1D1D",width=120,
                text_color="white",height=25,hover_color="#212121",
                font=("Calibri",13,"bold"),corner_radius=40).place(x=274,y=271)      
      
      Signout_button = CTkButton(homepage_frame,
                                 text="Sign Out", 
                                 width=90,height=20,
                                 text_color="white",
                                 bg_color="transparent",
                                 fg_color="transparent",
                                 border_color="white",
                                 border_width=1, 
                                 corner_radius=20, 
                                 hover_color="#1c1c1c",
                                 font=("Calibri",13,"bold"),
                                 command=confirmsignout)
      
      Signout_button.place(x=214,y=335)
      
      CTkButton(homepage_frame,
               text=f"Copyright©",
               bg_color="transparent",
               fg_color="transparent",width=51,
               text_color="white",height=11,
               hover_color="#121212",
               font=("Calibri",10,"bold"),corner_radius=4).place(x=83,y=370)
      
      CTkButton(homepage_frame,
               text=f"Support",
               bg_color="transparent",
               fg_color="transparent",width=35,
               text_color="white",height=11, hover_color="#121212",
               font=("Calibri",10,"bold"),corner_radius=4).place(x=154,y=370)
      
      CTkButton(homepage_frame,
               text=f"About",
               bg_color="transparent",
               fg_color="transparent",width=29,
               text_color="white",height=11, hover_color="#121212",
               font=("Calibri",10,"bold"),corner_radius=4).place(x=210,y=370)
      
      CTkButton(homepage_frame,
               text=f"Privacy Policy",
               bg_color="transparent",
               fg_color="transparent",width=60,
               text_color="white",height=11, hover_color="#121212",
               font=("Calibri",10,"bold"),corner_radius=4).place(x=260,y=370)
      
      CTkButton(homepage_frame,
               text=f"Contact",
               bg_color="transparent",
               fg_color="transparent",width=35,
               text_color="white",height=11, hover_color="#121212",
               font=("Calibri",10,"bold"),corner_radius=4).place(x=340,y=370)
      
      CTkButton(homepage_frame,
               text=f"Socials",
               bg_color="transparent",
               fg_color="transparent",width=31,
               text_color="white",height=11, hover_color="#121212",
               font=("Calibri",10,"bold"),corner_radius=4).place(x=393,y=370)
      
    def deposit_click():
      fetch_data_from_firebase()
      def deposit():
        global userid
        global pinval
        global mode
        global amt
        pinval = False
        try:
          amt = int(deposit_entry.get())
          if amt<=1000000 and amt>=1000:
            input_pin()
            if pinval == True :
              acc[userid]["BAL"] += amt
              update_firebase_database()
              mode = "Deposit"
              transaction()
              deposit_click()
              messagebox.showinfo("Deposit Successful",f"Deposit of Rs.{amt} to ID: {userid} successful")
          elif amt<1000000:
            messagebox.showinfo('Deposit Failed','Minimum Deposit Limit is Rs.1000')
          else:
            messagebox.showinfo("Deposit Failed","Maximum Deposit Limit is Rs.10 Lakh")
        except:
              messagebox.showinfo("Deposit Failed","Something went wrong \n(Try entering valid amount)")
          
      deposit_frame = CTkFrame(f1,
                               width=520,
                               height=400, 
                               bg_color="transparent",
                               fg_color="transparent")
      deposit_frame.place(x=230,y=0)
      
      imgpfp = CTkImage(dark_image=(Image.open("images/deposit.png")), 
                        size=(160, 160))
      imgP1 = CTkLabel(deposit_frame, image=imgpfp, text="")
      imgP1.place(x=180, y=20)
      
      CTkLabel(deposit_frame, 
               text=f"Current Balance  ", 
               bg_color="transparent",
               fg_color="transparent", 
               text_color="white",
               font=("Calibri",16,"bold")).place(x=165,y=200)
      CTkLabel(deposit_frame, 
               text=f"{acc[userid]["BAL"]}",
               bg_color="transparent",
               fg_color="transparent", 
               text_color="white", 
               font=("Calibri",18,"bold"), 
               anchor="w").place(x=290,y=200)
      
      deposit_entry = CTkEntry(deposit_frame,
                               width=200,
                               placeholder_text="Amount...", 
                               placeholder_text_color="grey",
                               border_width=0, 
                               bg_color="transparent", 
                               fg_color="transparent", 
                               font=("Calibri",18,"bold"))
      deposit_entry.place(x=220,y=250)
      
      CTkFrame(deposit_frame,
               height=2,
               width=240, 
               bg_color="black", 
               fg_color="white", 
               corner_radius=20).place(x=140,y=280)
      
      DEP_BUTTON = CTkButton(deposit_frame,
                             text="Deposit",
                             width=100,height=30,
                             text_color="white",
                             bg_color="transparent", 
                             fg_color="transparent",
                             border_color="white",
                             border_width=1,
                             corner_radius=20,
                             hover_color="#1c1c1c",
                             font=("Calibri",18,"bold"),
                             command=deposit)
      DEP_BUTTON.place(x=210,y=314)
      
      
    def withdraw_click():
      fetch_data_from_firebase()
      def withdraw():
        global userid
        global pinval
        global mode
        global amt
        pinval = False
        try:
          amt = int(withdraw_entry.get())
          if amt<=200000 and amt<=acc[userid]["BAL"]:
            input_pin()
            if pinval == True :
              acc[userid]["BAL"] -= amt
              update_firebase_database()
              mode = "Withdraw"
              transaction()
              withdraw_click()
              messagebox.showinfo("Withdraw Successful",f"Withdraw of Rs.{amt} from ID: {userid} successful")
          elif amt>200000:
            messagebox.showinfo('Withdraw Failed','Maximum withdraw Limit is Rs.2 Lakh')
          else:
            messagebox.showinfo("Withdraw Failed","Insufficient Funds")
        except:
              messagebox.showinfo("Withdraw Failed","Something went wrong \n(Try entering valid amount)")
          
      withdraw_frame = CTkFrame(f1, 
                                width=520, 
                                height=400, 
                                bg_color="transparent",
                                fg_color="transparent")
      withdraw_frame.place(x=230,y=0)
      
      imgpfp = CTkImage(dark_image=(Image.open("images/withdraw.png")), 
                        size=(200, 200))
      imgP1 = CTkLabel(withdraw_frame, image=imgpfp, text="")
      imgP1.place(x=160, y=20)
      
      CTkLabel(withdraw_frame, 
               text=f"Current Balance  ",
               bg_color="transparent", 
               fg_color="transparent",
               text_color="white", 
               font=("Calibri",16,"bold")).place(x=165,y=200)
      
      CTkLabel(withdraw_frame,
               text=f"{acc[userid]["BAL"]}", 
               bg_color="transparent",
               fg_color="transparent", 
               text_color="white",
               font=("Calibri",18,"bold"),
               anchor="w").place(x=290,y=200)
      
      withdraw_entry = CTkEntry(withdraw_frame,
                                width=200,
                                placeholder_text="Amount...", 
                                placeholder_text_color="grey",
                                border_width=0, 
                                bg_color="transparent", 
                                fg_color="transparent", 
                                font=("Calibri",18,"bold"))
      withdraw_entry.place(x=220,y=250)
      
      CTkFrame(withdraw_frame, 
               height=2, width=240,
               bg_color="black",
               fg_color="white", 
               corner_radius=20).place(x=140,y=280)
      
      WITH_BUTTON = CTkButton(withdraw_frame,
                             text="Withdraw",
                             width=100,height=30, 
                             text_color="white",
                             bg_color="transparent", 
                             fg_color="transparent", 
                             border_color="white",
                             border_width=1,
                             corner_radius=20, 
                             hover_color="#1c1c1c",
                             font=("Calibri",18,"bold"),
                             command=withdraw)
      WITH_BUTTON.place(x=210,y=314)
    
    def transfer_click():
      global istarget
      istarget = False
      
      def checkiftarget():
        global istarget
        targetuser = transfer_entry.get()
        try:
          if targetuser in acc:
            istarget = True
            messagebox.showinfo("Info","Target Account Found")
          else:
            istarget = False
            messagebox.showerror("Error","Account Not Found")
        except:
          messagebox.showerror("Error","Something is wrong \n(Try again)")

      def transferto():
        global userid
        global pinval
        global istarget
        global mode
        global amt
        global targetuser
        
        pinval = False
        amt = int(amount_entry.get())
        targetuser = transfer_entry.get()
        
        if targetuser in acc:
          istarget = True
        
        if istarget != False:
          try:
            if amt<=200000 and amt<=acc[userid]["BAL"]:
              input_pin()
              if pinval == True :
                acc[userid]["BAL"] -= amt
                acc[targetuser]["BAL"] += amt
                update_firebase_database()
                mode = "Transfer"
                transaction()
                transfer_click()
                messagebox.showinfo("Transfer Successful",f"Transaction of Rs{amt} to ID: {targetuser} successful")
                fetch_data_from_firebase()
                update_firebase_database()
                transfer_click()
                
            elif amt>200000:
              messagebox.showinfo('transfer Failed','Maximum transfer Limit is Rs.2 Lakh')
            else:
              messagebox.showinfo("transfer Failed","Insufficient Funds")
          except:
                messagebox.showinfo("transfer Failed","Something went wrong \n(Try entering valid amount)")
        else:
          messagebox.showerror("Error","Target Account Not Found")
              
      transfer_frame = CTkFrame(f1, 
                               width=520,
                               height=400,
                               bg_color="transparent",
                               fg_color="transparent")
      transfer_frame.place(x=230,y=0)
      
      imgpfp = CTkImage(dark_image=(Image.open("images/stack.png")), 
                        size=(190, 170))
      imgP1 = CTkLabel(transfer_frame, image=imgpfp, text="")
      imgP1.place(x=165, y=0)
      
      CTkLabel(transfer_frame, 
               text=f"Current Balance :",
               bg_color="transparent", 
               fg_color="transparent", 
               text_color="white",width=141,height=22,
               font=("Calibri",16,"bold")).place(x=150,y=152)
      CTkLabel(transfer_frame, 
               text=f"{acc[userid]["BAL"]}",
               bg_color="transparent", 
               fg_color="transparent",
               text_color="white",width=69,height=22, 
               font=("Calibri",18,"bold")).place(x=280,y=152)
  
      transfer_entry = CTkEntry(transfer_frame,
                                width=250,height=40,
                                placeholder_text="upi id...", 
                                placeholder_text_color="#9B9B9B",
                                border_width=2,corner_radius=30, 
                                bg_color="transparent", 
                                fg_color="#323232", 
                                font=("Calibri",18,"bold"))
      transfer_entry.place(x=85,y=200)
      
      CTkButton(transfer_frame,
                text="Search",
                bg_color="transparent",
                fg_color="#323232",width=100,
                text_color="white",height=40,hover_color="#212121",border_width=2,border_color="#858585",
                font=("Calibri",18,"bold"),corner_radius=40, command=checkiftarget).place(x=350,y=200)
      
      amount_entry = CTkEntry(transfer_frame,
                              placeholder_text="Amount...",
                              placeholder_text_color="#696969",
                              bg_color="transparent",
                              fg_color="#323232",
                              corner_radius=60,
                              width=200,height=40,
                              font=("Calibri",18,"bold"))
      
      amount_entry.place(x=160,y=270)
      
      transfer_button = CTkButton(transfer_frame,
                                 text="Transfer", 
                                 width=90,height=30,
                                 text_color="white",
                                 bg_color="transparent",
                                 fg_color="transparent",
                                 border_color="white",
                                 border_width=1, 
                                 corner_radius=20, 
                                 hover_color="#1c1c1c",
                                 font=("Calibri",18,"bold"),
                                 command=transferto)
      
      transfer_button.place(x=214,y=335)
      
    def history_click():
      history_frame = CTkFrame(f1, 
                               width=520,
                               height=400,
                               bg_color="transparent",
                               fg_color="transparent")
      history_frame.place(x=230,y=0)
      
      imgpfp = CTkImage(dark_image=(Image.open("images/pile.png")),
                        size=(120, 120))
      imgP1 = CTkLabel(history_frame, image=imgpfp, text="")
      imgP1.place(x=80, y=20)
      
      CTkLabel(history_frame, text="Transaction History", font=("Calibri",30,"bold")).place(x=190,y=61)
      trans_history = db.child("accounts").child(userid).child("history").get().val()
      
      # history_listbox = Listbox(history_frame, font=("Arial",12,"bold"), height=15, width=65, bg="#b0b0b0")
      # if trans_history:
      #   for transaction_id, transaction_info in trans_history.items():
      #     history_listbox.insert(0, f"{transaction_info} TXN:{transaction_id[-17:]}")
      # history_listbox.place(x=29,y=180)
      history_table = ttk.Treeview(history_frame, columns=("date", "time", "mode", "from","to","mon","bal","txn"), show="headings")
      history_table.place(x=0,y=180)
      history_table.heading("mon", text="Amount")
      history_table.column("mon", width=60)
      history_table.heading("mode", text="Mode")
      history_table.column("mode", width=60)
      history_table.heading("from", text="Sender")
      history_table.column("from", width=100)
      history_table.heading("to", text="Receiver")
      history_table.column("to", width=100)
      history_table.heading("date", text="Date")
      history_table.column("date", width=70)
      history_table.heading("time", text="Time")
      history_table.column("time", width=40)
      history_table.heading("txn", text="TXN ID")
      history_table.column("txn", width=140)
      history_table.heading("bal", text="Balance")
      history_table.column("bal", width=80)
      tval = ()
      for transaction_id, transaction_info in trans_history.items():
        tval = transaction_info.split(" ")
        history_table.insert(parent="", index=0, values=tval)
      
    homeframe = CTkFrame(root, width=900, height=500)
    homeframe.place(x=0, y=0)

    imgbackl = CTkImage(dark_image=(Image.open("images/background.jpeg")),
                        size=(900, 500))
    img2 = CTkLabel(homeframe, image=imgbackl, text="")
    img2.place(x=0, y=0)

    f1 = CTkFrame(homeframe, 
                  width=750, 
                  border_color="black",
                  border_width=0, 
                  height=400,
                  corner_radius=18,
                  fg_color="#0f0f0f",
                  bg_color="black")
    f1.place(x=75, y=50)
    
    f2 = CTkFrame(f1, height=400, width=230, fg_color="#1c1c1c", bg_color="#0f0f0f")
    f2.place(x=0,y=0)
    
    home_click()
    
    home_button = CTkButton(f2,
                            text="H O M E",
                            corner_radius=3,
                            height=50, 
                            width=228,
                            hover_color="#242424", 
                            font=("Calibri",18,"bold"),
                            fg_color="transparent",
                            bg_color="transparent",
                            command=home_click)
    home_button.place(x=1,y=75)

    deposit_button = CTkButton(f2, 
                               text="D E P O S I T",
                               corner_radius=3,
                               height=50,
                               width=228,
                               hover_color="#242424", 
                               font=("Calibri",18,"bold"), 
                               fg_color="transparent",
                               bg_color="transparent",
                               command=deposit_click)
    deposit_button.place(x=1,y=125)
    
    withdraw_button = CTkButton(f2, 
                                text="W I T H D R A W",
                                corner_radius=3,
                                height=50, 
                                width=228,
                                hover_color="#242424",
                                font=("Calibri",18,"bold"), 
                                fg_color="transparent",
                                bg_color="transparent", 
                                command=withdraw_click)
    withdraw_button.place(x=1,y=175)
    
    transfer_button = CTkButton(f2, 
                                text="T R A N S F E R",
                                corner_radius=3,
                                height=50,
                                width=228,
                                hover_color="#242424",
                                font=("Calibri",18,"bold"),
                                fg_color="transparent",
                                bg_color="transparent", 
                                command=transfer_click)
    transfer_button.place(x=1,y=225)
    
    history_button = CTkButton(f2, text="H I S T O R Y",
                               corner_radius=3,
                               height=50,
                               width=228,
                               hover_color="#242424", 
                               font=("Calibri",18,"bold"), 
                               fg_color="transparent",
                               bg_color="transparent", 
                               command=history_click)
    history_button.place(x=1,y=275)
    
  def SignIn():

    def showp():
        if password_entry.cget('show') == '*':
            password_entry.configure(show='')
        else:
            password_entry.configure(show='*')

    def checkAccount():
      global acc
      global userid
      userid = username_entry.get()
      passid = password_entry.get()
      
      if userid in acc and passid == acc[userid]["Pass"]:
        messagebox.showinfo("Success","Logged In Successfully!")
        homefn()
      elif userid in acc:
        messagebox.showerror("Try Again","Incorrect Password")
      else:
        messagebox.showerror("Try Again","Username not Found")
    
    MainFrame = CTkFrame(root, width=900, height=500)
    MainFrame.place(x=0,y=0)
    
    
    imgback = customtkinter.CTkImage(dark_image=(Image.open("images/background.jpeg").transpose(Image.Transpose.ROTATE_90)),
                                     size=(900,500))
    img1 = customtkinter.CTkLabel(MainFrame, image=imgback, text="")
    CTkLabel(MainFrame, image=img1.place(x=0,y=0))
    
    
    f1 = CTkFrame(MainFrame,
                  width=750,
                  height=400, 
                  corner_radius=18, 
                  fg_color="#171717",
                  bg_color="black")
    f1.place(x=75,y=50)
    
    my_image = customtkinter.CTkImage(dark_image=Image.open("images/signin.png"), 
                                      size=(300,250))
    image_label = customtkinter.CTkLabel(f1, image=my_image, text="")
    CTkLabel(f1, image=image_label.place(x=60,y=75))
    
    f2 = CTkFrame(f1,
                  width=330, 
                  height=400, 
                  fg_color="white", 
                  corner_radius=18,
                  bg_color="transparent")
    f2.place(x=420,y=0)
    
    signin_label = CTkLabel(f2, 
                            text="Sign In",
                            text_color="black",
                            font=("Microsoft YaHei UI Light",35,"bold"))
    signin_label.place(x=110,y=45)
    
    username_entry = CTkEntry(f2, 
                              placeholder_text="Username", 
                              width=230,
                              height= 40,
                              text_color="black",
                              bg_color="white",
                              fg_color="white",
                              placeholder_text_color="grey",
                              border_width=0)
    username_entry.place(x=50,y=130)
    CTkFrame(f2,width=250,height=2,bg_color='black').place(x=50,y=170)
    
    password_entry = CTkEntry(f2, 
                              show='*',
                              placeholder_text="Password",
                              width=230,
                              height= 40,
                              text_color="black",
                              bg_color="white",
                              fg_color="white",
                              placeholder_text_color="grey",
                              border_width=0)
    password_entry.place(x=50,y=180)
    CTkFrame(f2,width=250,height=2,bg_color='black').place(x=50,y=220)
    
    passcheckbox = CTkCheckBox(f2,
                               text="Show password",
                               hover_color="#b8b8b8",
                               checkbox_height=20, 
                               checkbox_width=20, 
                               checkmark_color="white",
                               fg_color="black", 
                               text_color="black", 
                               corner_radius=26,
                               command=showp)
    passcheckbox.place(x=50, y=240)
    
    signin_button = CTkButton(f2, 
                              text="Sign In",
                              hover_color="#b8b8b8",
                              font=("Calibri",15),
                              width=110,
                              border_width=2, 
                              fg_color="white", 
                              border_color="black",
                              text_color="black",
                              corner_radius=30,
                              command=checkAccount)
    signin_button.place(x=110,y=290)
    
    infolabel = CTkLabel(f2,
                         text="Dont have an account?",
                         text_color="grey",
                         font=("Microsoft YaHei UI Light",12,"bold"))
    infolabel.place(x=50,y=325)
    
    create_button = CTkButton(f2, 
                              text="Create Account",
                              width=0,
                              height=0,
                              font=("Calibri",12,"bold"),
                              border_width=0,
                              fg_color="transparent",
                              bg_color="transparent",
                              hover_color="#f2f2f2", 
                              text_color="black", command=SignUp)
    create_button.place(x=197,y=329)
      
      
      
  def SignUp():
    def showp():
        if password_entry.cget('show') == '*':
            password_entry.configure(show='')
        else:
            password_entry.configure(show='*')
    
    def createAccount():
      global acc
      userid = str(new_username_entry.get())
      Nname = str(nickname_entry.get())
      passid = str(password_entry.get())
      
      if userid !="" and Nname !="" and passid != "":
        if userid not in acc and passid:
          db.child("accounts").child(userid).set({"BAL":100,
                                                  "Pass":passid,
                                                  "User":Nname,
                                                  "email":f"{userid}@rockin.com",
                                                  "PIN":1234,
                                                  "history":""})
          messagebox.showinfo("Success","Sign Up Successfull!")
          fetch_data_from_firebase()
          SignIn()
        else:
          messagebox.showerror("Try Again","Account Already exists")
      else:
        messagebox.showerror("Error","All Fields are required")
    
    SignUpFrame = CTkFrame(root, width=900, height=500)
    SignUpFrame.place(x=0,y=0)
      
    imgback = customtkinter.CTkImage(dark_image=(Image.open("images/background.jpeg").transpose(Image.Transpose.ROTATE_90)),
                                     size=(900,500))
    img1 = customtkinter.CTkLabel(SignUpFrame, image=imgback, text="")
    CTkLabel(SignUpFrame, image=img1.place(x=0,y=0))
    
    
    f1 = CTkFrame(SignUpFrame,
                  width=750,
                  height=400,
                  fg_color="#171717",
                  corner_radius=18,
                  bg_color="black")
    f1.place(x=75,y=50)

    my_image = customtkinter.CTkImage(dark_image=Image.open("images/signup.png"), 
                                      size=(400,250))
    image_label = customtkinter.CTkLabel(f1, image=my_image, text="")
    CTkLabel(f1, image=image_label.place(x=0,y=55))
    
    f2 = CTkFrame(f1,
                  width=330,
                  height=400,
                  fg_color="white", 
                  corner_radius=18, 
                  bg_color="transparent")
    f2.place(x=420,y=0)

    signup_label = CTkLabel(f2, 
                            text="Sign Up",
                            text_color="black",
                            font=("Microsoft YaHei UI Light",35,"bold"))
    signup_label.place(x=100,y=35)
    
    new_username_entry = CTkEntry(f2, 
                                  placeholder_text="Username", 
                                  width=230, 
                                  height= 40,
                                  text_color="black",
                                  bg_color="white",
                                  fg_color="white",
                                  placeholder_text_color="grey",
                                  border_width=0)
    new_username_entry.place(x=50,y=110)
    CTkFrame(f2,width=250,height=2,bg_color='black').place(x=50,y=150)
    
    nickname_entry = CTkEntry(f2,
                              placeholder_text="Name", 
                              width=230, 
                              height= 40,
                              text_color="black",
                              bg_color="white",
                              fg_color="white", 
                              placeholder_text_color="grey",
                              border_width=0)
    nickname_entry.place(x=50,y=160)
    CTkFrame(f2,width=250,height=2,bg_color='black').place(x=50,y=200)
    
    password_entry = CTkEntry(f2, 
                              show='*',
                              placeholder_text="Password",
                              width=230, 
                              height= 40,
                              text_color="black",
                              bg_color="white",
                              fg_color="white", 
                              placeholder_text_color="grey", 
                              border_width=0)
    password_entry.place(x=50,y=210)
    CTkFrame(f2,width=250,height=2,bg_color='black').place(x=50,y=250)
    
    passcheckbox = CTkCheckBox(f2, 
                               text="Show password",
                               hover_color="#b8b8b8",
                               checkbox_height=20, 
                               checkbox_width=20, 
                               checkmark_color="white",
                               fg_color="black", 
                               text_color="black", 
                               corner_radius=26,
                               command=showp)
    passcheckbox.place(x=50, y=265)
    
    signup_button = CTkButton(f2, 
                              text="Sign Up",
                              hover_color="#b8b8b8",
                              font=("Calibri",15),
                              width=110,border_width=2,
                              fg_color="white", 
                              border_color="black",
                              text_color="black", 
                              corner_radius=30,
                              command=createAccount)
    signup_button.place(x=110,y=310)
    
    infolabel = CTkLabel(f2, 
                         text="Already have an account",
                         text_color="grey", 
                         font=("Microsoft YaHei UI Light",12,"bold"))
    infolabel.place(x=65,y=340)
    
    signin_button = CTkButton(f2, 
                              text="Sign in",
                              width=0,
                              height=0,
                              font=("Calibri",12,"bold"),
                              border_width=0,
                              fg_color="transparent",
                              bg_color="transparent",
                              hover_color="#f2f2f2",
                              text_color="black", 
                              command=SignIn)
    signin_button.place(x=217,y=344)

  # homefn()
  # SignIn()
  welcome()
  root.mainloop()
  
main()

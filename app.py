from tkinter import * 
from tkinter import messagebox , simpledialog , filedialog
from PIL import Image, ImageTk
from datetime import date
prod_list = []

file = open("products.csv", "r")

lines = file.readlines()
for line in lines:
    newline = line.split(",")
    print(newline)
    newItem = {
        'id': f"{newline[0]}",
        'name': f"{newline[1]}",
        'img': f"{newline[2]}",
        'price': f"{newline[3]}",
    }

    prod_list.append(newItem)

file.close()


root = Tk()
root.title("Aryans Shop")
root.minsize(800, 500)
root.configure(bg="#f5f5f5")


cart_items = {}


def empty():
    cart_items.clear()
    show_cart(cart_items)


def delete():
    selected_indices = [index for index in prod_box.curselection()]
    with open("products.csv", "r") as file:
        lines = file.readlines()

    if len(lines) == 1:   
        with open("products.csv", "w"):
            pass 
        prod_list.clear()
    else:
        modified_lines = []
        line_number = 1
        for line in lines:
            if line_number not in selected_indices:
                modified_lines.append(line)
            line_number += 1

        with open("products.csv", "w") as file:
            file.writelines(modified_lines)

        prod_list.clear()
        with open("products.csv", "r") as file:
            for line in file:
                newLine = line.strip().split(",")
                newItem = {
                    'id': newLine[0]  ,
                    'name': newLine[1],
                    'img': newLine[2] ,
                    'price': newLine[3],
                }
                prod_list.append(newItem)
      
        prod_box.destroy()
        delete_btn.destroy()
        add_btn.destroy()
        show_prod_box()
        show_prod(prod_list)


def add_prod():

    def add_to_file(name,price,img):
        prod_id = "P-" + str(len(prod_list) + 1)
        file = open("products.csv","a")
        file.write(f"{prod_id},{name},{img},{price}\n")
        file.close()

        newItem = {
            'id': f"{prod_id}",
            'name': f"{name}",
            'img': f"{img}",
            'price': f"{price}",
        }
        prod_list.append(newItem)
        product_window.destroy()
        messagebox.showinfo("Success","Product Added Successfull")

    def select_image():
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            img_entry.delete(0, END)  
            img_entry.insert(0, file_path)

    product_window = Toplevel(root)
    Label(product_window, text="Product name : ").grid(row=0, column=0)
    name_entry = Entry(product_window)
    name_entry.grid(row=0, column=1)

    Label(product_window, text="Product price : ").grid(row=1, column=0)
    price_entry = Entry(product_window)
    price_entry.grid(row=1, column=1)

    Label(product_window, text="Product image : ").grid(row=2, column=0)
    img_entry = Entry(product_window)
    img_entry.grid(row=2, column=1)

    
    select_img_btn = Button(product_window, text="Select Image", command=select_image)
    select_img_btn.grid(row=2, column=2)

    btn = Button(product_window, text="Add Product", command=lambda: add_to_file(name_entry.get(), price_entry.get(), img_entry.get()))
    btn.grid(row=3, columnspan=2)


def show_prod_box():
        global prod_box
        prod_box = Listbox(admin_frame,selectmode=MULTIPLE)
        for i in prod_list:
            prod_box.insert(END,f"{i['id']} {i['name']}")

        prod_box.pack(padx=20,pady=(12,22),anchor="nw",side="left")
        global delete_btn
        global add_btn
        delete_btn = Button(admin_frame,text="Dlete Prod",command=lambda:delete())
        delete_btn.pack(padx=20,pady=2)

        add_btn = Button(admin_frame,text="Add Prod ",command=lambda:add_prod())
        add_btn.pack(padx=20,pady=2)
        
def login(username,password):
    file = open("pass.csv","r")
    lines = file.readlines() 
    for line in lines:
        listn = line.split(",")
        print(listn[0],listn[1])
        print(f"{username} {password}")

        if (username == str(listn[0])) and (password == str(listn[1])):

            window.destroy()
            global admin_frame
            admin_window = Toplevel(root)
            admin_window.geometry("500x300")
            admin_window.minsize(500,300)
            admin_window.maxsize(500,300)
            admin_frame = Frame(admin_window)
            admin_frame.pack()

            Label(admin_frame,text="Products ").pack(padx=20,pady=4,anchor="nw",side="top")
            
            show_prod_box()
            return True
        
    messagebox.showerror("Error", "Invalid username or password")
        
        

def admin():
    global window
    window = Toplevel(root)

    window.geometry("250x250")
    new = Frame(window)
    new.pack(anchor="center",pady=60)

    user_label = Label(new,text= " Enter Username ")
    user_label.grid(row =0 , column= 0,pady=10)
    user_entry = Entry(new)
    user_entry.grid(row = 0, column=1,pady=10)

    pass_label = Label(new,text= " Enter Password ")
    pass_label.grid(row=1,column=0)
    pass_entry = Entry(new)
    pass_entry.grid(row=1,column=1)

    login_btn = Button(new,text="Login Now" ,command=lambda :login(user_entry.get(),pass_entry.get()))
    login_btn.grid(pady=10)


def view_order():
    def login_func():
        username = user_name_entry.get()
        password = pass_word_entry.get()
        with open("pass.csv","r") as file:
            line = file.readlines()
        file.close()
        for i in line:
            temp = i.split(",")
            print(temp)
            if temp[0] == username and temp[1] == password:
                Order_window = Toplevel(new_wind)
                order_box = Listbox(Order_window,width=40)
                order_list = []
                with open("file.csv","r") as file:
                    lines = file.readlines()
                
                for i in lines:
                    if len(i) > 4:
                        temp = i.split(",")
                        print(temp)   
                        item = {
                            'date' : f"{temp[0]}",
                            'address' : f"{temp[1]}",
                            'product' : f"{temp[2]}",
                            'Quantity' : f"{temp[3]}",
                            'amount' : f"{temp[4]}",
                        }
                        order_list.append(item)
                
                for i in order_list:
                    order_box.insert(END,f"{i['address']}  {i['product']} {i['Quantity']}  {i['date']} {i['amount']}")
                order_box.pack(padx=20,pady=(12,22),anchor="nw",side="left")

    new_wind = Toplevel(root)
    user_name_label = Label(new_wind,text="Enter Username ")
    user_name_label.grid(row=0,column=0)
    user_name_entry = Entry(new_wind)
    user_name_entry.grid(row=0,column=1)
    pass_word_label = Label(new_wind,text="Enter Password ")
    pass_word_label.grid(row=1,column=0)
    pass_word_entry = Entry(new_wind)
    pass_word_entry.grid(row=1,column=1)

    login_btn = Button(new_wind,text="Login" , command=login_func)
    login_btn.grid(row=2,column=0)


    pass
    

# Navigation BAR
menu = Menu(root)

file_menu = Menu(menu, tearoff=0)
file_menu.add_command(label="Admin" ,command=admin)
file_menu.add_command(label="Orders",command=view_order)
file_menu.add_separator()
file_menu.add_command(label="Exit",command=lambda :root.quit())

file_options = Menu(menu, tearoff=0)
file_options.add_command(label="Empty Cart", command=empty)
file_options.add_separator()
file_options.add_command(label="Exit",command=lambda :root.quit())

menu.add_cascade(label="Dropdown", menu=file_menu)
menu.add_cascade(label="Cart", menu=file_options)

root.config(menu=menu, padx=10)


def search(query):
    new_list = []
    if str(query).isnumeric():
        for i in prod_list:
            if str(query).lower() in str(i['price']).lower():
                new_list.append(i)
    else:
        for i in prod_list:
            if str(query).lower() in str(i['name']).lower():
                new_list.append(i)

    show_prod(new_list)

search_frame = Frame(root, bg="#fff", pady=10, padx=20)
search_frame.pack(anchor="nw", pady=3)

search_entry = Entry(search_frame, text="Search")
search_entry.grid(row=0, column=1, sticky="ew", padx=10)

search_label = Label(search_frame, text="Search ", bg="#fff")
search_label.grid(row=0, column=0)

search_entry.bind("<KeyRelease>", lambda event: search(search_entry.get()))


def add_to_cart(prod_id):

    if len(cart_items) < 6:
        if prod_id in cart_items.keys():
            cart_items[prod_id]['quantity'] += 1
        else:
            x = [i for i in prod_list if i['id'] == prod_id]
            cart_item = {
                str(prod_id): {
                    'name': str(x[0]['name']),
                    'quantity': 1,
                    'price': str(x[0]['price'])
                }
            }
            cart_items.update(cart_item)
    else:
        messagebox.showinfo("Limit Excedded" , "You cannot select moe than 6 items at a time !")

    show_cart(cart_items)



def show_prod(iterable):
    for j in shop_frame.winfo_children():
        j.destroy()

    row, column = 0, 0
    for i in iterable:
        item_frame = Frame(shop_frame, bg="#fff", bd=1, relief="solid", padx=10, pady=10)
        item_frame.grid(row=row, column=column, padx=5, pady=10)

        img = Image.open(i['img'])
        img = img.resize((130, 130))
        img = ImageTk.PhotoImage(img)
        img_label = Label(item_frame, image=img, bg="#fff")
        img_label.image = img
        img_label.pack()

        prod_name = Label(item_frame, text=f"{i['name']}", font=("Arial", 12, "bold"), fg="#333", bg="#fff")
        prod_name.pack(pady=5)

        prod_price = Label(item_frame, text=f"${i['price']}", font=("Arial", 10), fg="#555", bg="#fff")
        prod_price.pack()

        add_cart_btn = Button(item_frame, text="Add to Cart", bg="#fb8d1A", fg="white", relief="flat",
                              command=lambda id=i['id']: add_to_cart(id))
        add_cart_btn.pack(pady=10)

        column += 1
        if column % 6 == 0:
            row += 1
            column = 0



def show_cart(iterable):
    for j in cart_frame.winfo_children():
        j.destroy()

    total = 0
    row = 0
    for item_id, item_info in iterable.items():
        item_frame = Frame(cart_frame, relief="solid", bd=1, padx=10, pady=5, bg="#fff")
        item_frame.pack(fill="x", pady=5)

        price = int(item_info['price']) * int(item_info['quantity'])
        item_info_label = Label(item_frame,
                                text=f"{item_info['name']} x {item_info['quantity']}  ${price}",
                                bg="#fff")
        item_info_label.pack(side="left")

        item_btn_1 = Button(item_frame, text="+", command=lambda id=item_id: add(id), bg="#fb8d1A", fg="white",
                            relief="flat")
        item_btn_1.pack(side="right")

        item_btn_2 = Button(item_frame, text="-", command=lambda id=item_id: sub(id), bg="#fb8d1A", fg="white",
                            relief="flat")
        item_btn_2.pack(side="right", padx=(5, 5))

        total += price
        row += 1

    if total > 0:
        order_btn = Button(cart_frame, text=f"Order Now  for ${total}  ", bg="#fb8d1A", fg="white",
        command=lambda: order(total))
        order_btn.pack()


def add(prod_id):
    if(cart_items[prod_id]['quantity']  < 5):
        cart_items[prod_id]['quantity'] += 1
        show_cart(cart_items)
    else:
        messagebox.showinfo("Limit Exceeded ", "Maximum no of products added ! ")

def sub(prod_id):
    if cart_items[prod_id]['quantity'] > 1:
        cart_items[prod_id]['quantity'] -= 1
    else:
        cart_items.pop(prod_id)
    show_cart(cart_items)



order_count = 0


def order(price):
    global order_count
    confir = messagebox.askyesno("Confirm Order", f"Place order for ${price}?")
    
    if confir:
       
        current_date = date.today()
        
        address_prompt = "Please enter your address:"
        address = simpledialog.askstring("Address", address_prompt)
        
        order_count += 1
        print(f"Order placed for ${price}")
        file = open("file.csv", "a")
        for prod_id, details in cart_items.items():
            file.write(f"{current_date},{address},{details['name']},{details['quantity']},{details['price']}")
        
        messagebox.showinfo("Order Placed " , f"Order successfully placed for {price} at {address}")
        cart_items.clear()
        show_cart(cart_items)



cart_main_frame = Frame(root, padx=30, bg="#f5f5f5")
cart_main_frame.pack(side='right', anchor="ne", padx=30)

cart_label = Label(cart_main_frame, font=('calivri', 13, 'bold'), text="Your Cart ", bg="#f5f5f5", fg="#fb8d1A")
cart_label.pack(side="top")

cart_frame = Frame(cart_main_frame, bg="#f5f5f5")
cart_frame.pack()



canvas_shop = Canvas(root, bg="#f5f5f5")
canvas_shop.pack(side="left", fill="both", expand=True)


shop_frame = Frame(canvas_shop, bg="#f5f5f5")
shop_frame.pack(anchor="nw")

scrollbar_shop = Scrollbar(root, orient="vertical", command=canvas_shop.yview)
scrollbar_shop.pack(side="right", fill="y")

canvas_shop.configure(yscrollcommand=scrollbar_shop.set)
canvas_shop.create_window((0, 0), window=shop_frame, anchor="nw")

shop_frame.bind("<Configure>", lambda event: canvas_shop.configure(scrollregion=canvas_shop.bbox("all")))

show_prod(prod_list)

root.mainloop()


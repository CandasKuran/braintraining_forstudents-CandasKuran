import tkinter as tk
import geo01
import info02
import info05
import displayResult
import loginPage
import database

# exercises array
a_exercise = ["geo01", "info02", "info05"]
albl_image = [None, None, None] # label (with images) array
a_image = [None, None, None] # images array
a_title = [None, None, None] # array of title (ex: GEO01)

dict_games = {"geo01": geo01.open_window_geo_01, "info02": info02.open_window_info_02, "info05": info05.open_window_info_05}


# pour attiribuer le role
def open_assign_teacher_window():
    rgb_color = (139, 201, 194)
    hex_color = '#%02x%02x%02x' % rgb_color
    window.configure(bg=hex_color)
    window.grid_columnconfigure((0, 1, 2), minsize=300, weight=1)

    assign_window = tk.Toplevel()
    assign_window.title("Attribuer un rôle de professeur")
    assign_window.geometry("200x150+650+400")

    assign_window.grab_set()

    # input pour Nom de l'étudiant à promouvoir
    tk.Label(assign_window, text="Nom de l'étudiant à promouvoir:").pack()
    student_name_entry = tk.Entry(assign_window)
    student_name_entry.pack()

    # input pour psw de session actuelle
    tk.Label(assign_window, text="Votre mot de passe:").pack()
    password_entry = tk.Entry(assign_window, show="*")
    password_entry.pack()


    tk.Button(assign_window, text="Attribuer",
              command=lambda: assign_teacher_role(student_name_entry.get(), password_entry.get(), assign_window)).pack()


# verification d'utilisateur et psw
def assign_teacher_role(student_name, password, window):
    # verification de psw de session actuelle
    if database.check_user(loginPage.current_user, password):
        if database.assign_teacher_role(student_name):
            tk.messagebox.showinfo("Succès", f"Le rôle de professeur a été attribué à {student_name}.")
            window.destroy()
        else:
            tk.messagebox.showerror("Erreur", "Utilisateur introuvable ou déjà professeur.")
    else:
        tk.messagebox.showerror("Erreur", "Mot de passe incorrect.")

def logout():
    global window
    if window:
        window.destroy()
    loginPage.create_login_window(show_main_menu)


def exercise(event, exer):
    dict_games[exer](window)

def show_main_menu():
    global window
    window = tk.Tk()
    window.title("Training, entrainement cérébral")
    window.geometry("1400x650")

    # color définition
    rgb_color = (139, 201, 194)
    hex_color = '#%02x%02x%02x' % rgb_color
    window.configure(bg=hex_color)
    window.grid_columnconfigure((0, 1, 2), minsize=300, weight=1)

    # Title création
    lbl_title = tk.Label(window, text="TRAINING MENU", font=("Arial", 15))
    lbl_title.grid(row=0, column=1, ipady=5, padx=40, pady=40)

    lbl_current_user = tk.Label(window,
                                text=f"Session actuelle: '{loginPage.current_user}' en tant que {loginPage.current_role}",
                                font=("Arial", 13, "bold"))
    lbl_current_user.grid(row=0, column=2, sticky="ne")

    # labels creation and positioning
    for ex in range(len(a_exercise)):
        a_title[ex] = tk.Label(window, text=a_exercise[ex], font=("Arial", 15))
        a_title[ex].grid(row=1+2*(ex//3), column=ex % 3, padx=40, pady=10)

        a_image[ex] = tk.PhotoImage(file="img/" + a_exercise[ex] + ".gif")
        albl_image[ex] = tk.Label(window, image=a_image[ex])
        albl_image[ex].grid(row=2 + 2*(ex // 3), column=ex % 3, padx=40, pady=10)
        albl_image[ex].bind("<Button-1>", lambda event, ex=ex: exercise(event=None, exer=a_exercise[ex]))



    # Buttons, display results & quit
    btn_display = tk.Button(window, text="Display results", font=("Arial", 15))
    btn_display.grid(row=1+ 2*len(a_exercise)//3, column=1)
    btn_display.bind("<Button-1>", lambda e: displayResult.create_result_window())

    btn_finish = tk.Button(window, text="Quitter", font=("Arial", 15))
    btn_finish.grid(row=2+ 2*len(a_exercise)//3, column=1)
    btn_finish.bind("<Button-1>", quit)

    btn_logout = tk.Button(window, text="Déconnexion", command=logout, font=("Arial", 15))
    btn_logout.grid(row=5, column=1)

    if loginPage.current_role == "Professeur":
        btn_assign_teacher = tk.Button(window, text="Attribuer un rôle de professeur", command=open_assign_teacher_window,
                                       font=("Arial", 15))
        btn_assign_teacher.grid(row=6, column=1)

    window.mainloop()

if __name__ == "__main__":
    loginPage.create_login_window(show_main_menu)

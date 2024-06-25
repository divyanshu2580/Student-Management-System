import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import simpledialog , messagebox
import pymysql
from PIL import Image , ImageTk
import hashlib
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

password = os.getenv("PASSWORD")
adminPassword = os.getenv("ADMIN_PASSWORD")
adminUsername = os.getenv("ADMIN_USERNAME")

connection_params = {
    'host': 'localhost',  
    'user': 'root',       
    'password': password, 
    'database': 'eduschema', 
}
try:
    conn = pymysql.connect(**connection_params)
    print("Connection successful")
    

    def show_data_in_text_widget(data):
        text_widget.delete(1.0, tk.END)  
        for row in data:
            text_widget.insert(tk.END, row)
            text_widget.insert(tk.END, "\n")

    def add_course():
        c_name = simpledialog.askstring("Input", "Enter the Course Name :")
        credit = simpledialog.askinteger("Input", "Enter the Course Credits :")
        d_id = simpledialog.askinteger("Input", "Enter the Department ID :")
        query = f"insert into course (c_name ,credits ,d_id ) values (%s , %s, %s) "
        cursor = conn.cursor()
        cursor.execute(query, (c_name ,credit ,d_id  ))
        conn.commit()
        display_course()

    def display_course():
        query= f"select c_id , c_name, credits , d_id   from course where is_deleted = 'No'"
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"SHOW COLUMNS FROM course")
                columns = ['c_id', 'c_name', 'credits', 'd_id']
                
                cursor.execute(query)
                data = cursor.fetchall()

                text_widget.delete(1.0, tk.END)  

                header = '      |      '.join(columns)
                text_widget.insert(tk.END, header + "\n")
                text_widget.insert(tk.END, "-" * len(header) + "\n")
                
                for row in data:
                    row_text = '    |    '.join(map(str, row))
                    text_widget.insert(tk.END, row_text + "\n\n")

        except pymysql.MySQLError as e:
            print(f"MySQL error: {e}")

    def display_deleted_course():
        query= f"select c_id , c_name, credits , d_id from course where is_deleted = 'Yes'"
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"SHOW COLUMNS FROM course")
                columns = ['c_id', 'c_name', 'credits', 'd_id']
                
                cursor.execute(query)
                data = cursor.fetchall()

                text_widget.delete(1.0, tk.END)  

                header = '      |      '.join(columns)
                text_widget.insert(tk.END, header + "\n")
                text_widget.insert(tk.END, "-" * len(header) + "\n")
                
                for row in data:
                    row_text = '    |    '.join(map(str, row))
                    text_widget.insert(tk.END, row_text + "\n\n")  

        except pymysql.MySQLError as e:
            print(f"MySQL error: {e}")

    def delete_course():
        display_course()
        course_id = simpledialog.askinteger("Input", "Enter the Course ID to delete:")
        if course_id is not None:
            query = f"update course set is_deleted ='Yes' where c_id=  {course_id}"
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    conn.commit()
                    messagebox.showinfo("Success", f"Course with ID {course_id} deleted successfully.")
                    display_deleted_course()  

            except pymysql.MySQLError as e:
                messagebox.showerror("Error", f"MySQL error: {e}")

    def restore_course():
        display_deleted_course()
        course_id = simpledialog.askinteger("Input", "Enter the Course ID to Restore:")
        if course_id is not None:
            query = f"update course set is_deleted ='No' where c_id=  {course_id}"
            try:
                
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    conn.commit()
                    messagebox.showinfo("Success", f"Course with ID {course_id} restored successfully.")
                    display_course()  

            except pymysql.MySQLError as e:
                messagebox.showerror("Error", f"MySQL error: {e}")

    def display_student():
        query= f"select s_id , s_name, s_dob , s_address , s_phone  , s_email  , en_date  , gender  ,d_id from student where is_deleted = 'No'"
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"SHOW COLUMNS FROM student")
                columns = ['s_id ', 's_name', 's_dob' ,'s_address' , 's_phone'  , 's_email'  ,'en_date'  , 'gender'  ,'d_id' ]
                
                cursor.execute(query)
                data = cursor.fetchall()

                text_widget1.delete(1.0, tk.END)  

                header = '      |      '.join(columns)
                text_widget1.insert(tk.END, header + "\n")
                text_widget1.insert(tk.END, "-" * len(header) + "\n")
                
                for row in data:
                    row_text = '     |    '.join(map(str, row))
                    text_widget1.insert(tk.END, row_text + "\n\n")  

        except pymysql.MySQLError as e:
            print(f"MySQL error: {e}")

    def add_student():
        s_name = simpledialog.askstring("Input", "Enter the  Name :")
        d_o_b = simpledialog.askstring("Input", "Enter the Date of birth(YYYY-MM-DD) :")
        d_id = simpledialog.askinteger("Input", "Enter the Department ID :")
        en_date = simpledialog.askstring("Input", "Enter the Date of enrollement(YYYY-MM-DD) :")
        s_address = simpledialog.askstring("Input", "Enter the Address :")
        s_phone = simpledialog.askstring("Input", "Enter the Mobile number :")
        gender = simpledialog.askstring("Input", "Enter the Gender (Male-M)\n(Female-F) :")
        s_email = simpledialog.askstring("Input", "Enter the email :")
        query = f"insert into student (s_name ,s_dob ,d_id,en_date,s_address,s_phone,gender,s_email ) values (%s , %s, %s,%s , %s, %s,%s,%s) "
        cursor = conn.cursor()
        cursor.execute(query, (s_name ,d_o_b ,d_id,en_date,s_address,s_phone,gender,s_email ))
        conn.commit()
        display_student()

    def delete_student():
        std_id = simpledialog.askinteger("Input", "Enter the Student ID to delete:")
        if std_id is not None:
            query = f"update student set is_deleted ='Yes' where s_id=  {std_id}"
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    conn.commit()
                    messagebox.showinfo("Success", f"Student with ID {std_id} deleted successfully.")
                    display_deleted_student()  

            except pymysql.MySQLError as e:
                messagebox.showerror("Error", f"MySQL error: {e}")

    def restore_student():
            std_id = simpledialog.askinteger("Input", "Enter the Student ID to Restore:")
            if std_id is not None:
                query = f"update student set is_deleted ='No' where s_id=  {std_id}"
                try:
                    with conn.cursor() as cursor:
                        cursor.execute(query)
                        conn.commit()
                        messagebox.showinfo("Success", f"Student with ID {std_id} restored successfully.")
                        display_student()  

                except pymysql.MySQLError as e:
                    messagebox.showerror("Error", f"MySQL error: {e}")

    def display_deleted_student():
        query= f"select s_id , s_name, s_dob , s_address , s_phone  , s_email  , en_date  , gender  ,d_id from student where is_deleted = 'Yes'"
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"SHOW COLUMNS FROM student")
                columns = ['s_id ', 's_name', 's_dob' ,'s_address' , 's_phone'  , 's_email'  ,'en_date'  , 'gender'  ,'d_id' ]
                
                cursor.execute(query)
                data = cursor.fetchall()

                text_widget1.delete(1.0, tk.END) 

                header = '      |      '.join(columns)
                text_widget1.insert(tk.END, header + "\n")
                text_widget1.insert(tk.END, "-" * len(header) + "\n")
                
                for row in data:
                    row_text = '   |   '.join(map(str, row))
                    text_widget1.insert(tk.END, row_text + "\n\n")

        except pymysql.MySQLError as e:
            print(f"MySQL error: {e}")

    def display_instructors():
        query= f"select i_id,  i_name  , i_dob , i_address  , i_phone  , i_email  ,gender  , qualifications ,  joining_date  ,salary , experience from instructor where is_deleted ='No'"
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"SHOW COLUMNS FROM instructor ")
                columns = ['i_id','i_name'  , 'i_dob' , 'i_address'  , 'i_phone'  , 'i_email'  ,'gender'  , 'qualifications' ,  'joining_date'  ,'salary' , 'experience']
                
                cursor.execute(query)
                data = cursor.fetchall()

                text_widget2.delete(1.0, tk.END) 

                header = '    |   '.join(columns)
                text_widget2.insert(tk.END, header + "\n")
                text_widget2.insert(tk.END, "-" * len(header) + "\n")
                
                for row in data:
                    row_text = '   | '.join(map(str, row))
                    text_widget2.insert(tk.END, row_text + "\n\n")  

        except pymysql.MySQLError as e:
            print(f"MySQL error: {e}")

    def add_instructor():
        i_name = simpledialog.askstring("Input", "Enter the  Name :")
        d_o_b = simpledialog.askstring("Input", "Enter the Date of birth(YYYY-MM-DD) :")
        exp = simpledialog.askinteger("Input", "Enter the years of experience :")
        joining_date = simpledialog.askstring("Input", "Enter the Date of enrollement(YYYY-MM-DD) :")
        i_address = simpledialog.askstring("Input", "Enter the Address :")
        i_phone = simpledialog.askstring("Input", "Enter the Mobile number :")
        i_gender = simpledialog.askstring("Input", "Enter the Gender (Male-M)\n(Female-F) : ")
        i_email = simpledialog.askstring("Input", "Enter the email :")
        qual = simpledialog.askstring("Input", "Enter the Qualification :")
        salary = simpledialog.askfloat("Input","Enter the Salary : ")
        query = f"insert into instructor (i_name  , i_dob , i_address  , i_phone  , i_email  ,gender  , qualifications ,  joining_date  ,salary , experience) values (%s , %s, %s,%s , %s, %s,%s , %s, %s,%s) "
        cursor = conn.cursor()
        cursor.execute(query, (i_name , d_o_b, exp,joining_date , i_address , i_phone,i_gender,i_email,qual,salary))
        conn.commit()
        display_instructors()

    def restore_instructor():
            ins_id = simpledialog.askinteger("Input", "Enter the Instructor ID to Restore:")
            if ins_id is not None:
                query = f"update instructor set is_deleted ='No' where i_id=  {ins_id}"
                try:
                    with conn.cursor() as cursor:
                        cursor.execute(query)
                        conn.commit()
                        messagebox.showinfo("Success", f"Student with ID {ins_id} restored successfully.")
                        display_instructors()  

                except pymysql.MySQLError as e:
                    messagebox.showerror("Error", f"MySQL error: {e}")

    def delete_instructor():
        ins_id = simpledialog.askinteger("Input", "Enter the Instructor ID to delete:")
        if ins_id is not None:
            query = f"update instructor set is_deleted ='Yes' where i_id=  {ins_id}"
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    conn.commit()
                    messagebox.showinfo("Success", f"Instructor with ID {ins_id} deleted successfully.")
                    display_deleted_instructor()  

            except pymysql.MySQLError as e:
                messagebox.showerror("Error", f"MySQL error: {e}")

    def display_deleted_instructor():
        query= f"select i_id,  i_name  , i_dob , i_address  , i_phone  , i_email  ,gender  , qualifications ,  joining_date  ,salary , experience from instructor where is_deleted = 'Yes'"
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"SHOW COLUMNS FROM instructor")
                columns = ['i_id','i_name'  , 'i_dob' , 'i_address'  , 'i_phone'  , 'i_email'  ,'gender'  , 'qualifications' ,  'joining_date'  ,'salary' , 'experience']
                
                cursor.execute(query)
                data = cursor.fetchall()

                text_widget2.delete(1.0, tk.END) 

                header = '    |   '.join(columns)
                text_widget2.insert(tk.END, header + "\n")
                text_widget2.insert(tk.END, "-" * len(header) + "\n")
                
                for row in data:
                    row_text = '   | '.join(map(str, row))
                    text_widget2.insert(tk.END, row_text + "\n\n") 

        except pymysql.MySQLError as e:
            print(f"MySQL error: {e}")

    def display_grades():
        query= f"select gr_id , grades , grading_date , s_id , sec_id from grades"
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"SHOW COLUMNS FROM grades")
                columns = ['gr_id' , 'grades' , 'grading_date' , 's_id' , 'sec_id']
                
                cursor.execute(query)
                data = cursor.fetchall()

                text_widget3.delete(1.0, tk.END)  

                header = '  |  '.join(columns)
                text_widget3.insert(tk.END, header + "\n")
                text_widget3.insert(tk.END, "-" * len(header) + "\n")
                
                for row in data:
                    row_text = '     |     '.join(map(str, row))
                    text_widget3.insert(tk.END, row_text + "\n\n")  

        except pymysql.MySQLError as e:
            print(f"MySQL error: {e}")

    def delete_grades():
        gr_id = simpledialog.askinteger("Input", "Enter the Grade ID to delete:" )
        if gr_id is not None:
            query = f"update grades set is_deleted ='Yes' where gr_id=  {gr_id}"
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    conn.commit()
                    messagebox.showinfo("Success", f"Grade with ID {gr_id} deleted successfully.")
                    display_deleted_grades()  

            except pymysql.MySQLError as e:
                messagebox.showerror("Error", f"MySQL error: {e}")

    def add_grades():
        grades= simpledialog.askinteger("Input", "Enter the Grades :")
        g_date = simpledialog.askstring("Input", "Enter the Date of Grading(YYYY-MM-DD) :")
        s_id = simpledialog.askinteger("Input", "Enter the Srudent ID :")
        sec_id = simpledialog.askinteger("Input", "Enter the Section ID :")
        query = f"insert into grades (grades , grading_date , s_id , sec_id ) values (%s , %s, %s,%s)"
        cursor = conn.cursor()
        cursor.execute(query, (grades, g_date, s_id, sec_id  ))
        conn.commit()
        display_grades()

    def restore_grades():
            gr_id = simpledialog.askinteger("Input", "Enter the Grade ID to Restore:")
            if gr_id is not None:
                query = f"update grades set is_deleted ='No' where gr_id=  {gr_id}"
                try:
                    with conn.cursor() as cursor:
                        cursor.execute(query)
                        conn.commit()
                        messagebox.showinfo("Success", f"Student with ID {gr_id} restored successfully.")
                        display_grades()  

                except pymysql.MySQLError as e:
                    messagebox.showerror("Error", f"MySQL error: {e}")

    def display_deleted_grades():
        query= f"select gr_id , grades , grading_date , s_id , sec_id from grades where is_deleted = 'Yes'"
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"SHOW COLUMNS FROM grades")
                columns = ['gr_id' , 'grades' , 'grading_date' , 's_id' , 'sec_id']
                
                cursor.execute(query)
                data = cursor.fetchall()

                text_widget3.delete(1.0, tk.END) 

                header = '  |  '.join(columns)
                text_widget3.insert(tk.END, header + "\n")
                text_widget3.insert(tk.END, "-" * len(header) + "\n")
                
                for row in data:
                    row_text = '     |     '.join(map(str, row))
                    text_widget3.insert(tk.END, row_text + "\n\n")  

        except pymysql.MySQLError as e:
            print(f"MySQL error: {e}")

    def display_department():
        clear5()
        query= f"select * from department"
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"SHOW COLUMNS FROM department")
                columns = [col[0] for col in cursor.fetchall()]
                
                cursor.execute(query)
                data = cursor.fetchall()

                text_widget4.delete(1.0, tk.END) 

                header = '  |  '.join(columns)
                text_widget4.insert(tk.END, header + "\n")
                text_widget4.insert(tk.END, "-" * len(header) + "\n")
                
                for row in data:
                    row_text = '       |       '.join(map(str, row))
                    text_widget4.insert(tk.END, row_text + "\n\n") 

        except pymysql.MySQLError as e:
            print(f"MySQL error: {e}")

    def admin_instructor():
        clear5()
        query= f"select * from instructor "
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"SHOW COLUMNS FROM instructor ")
                columns = [col[0] for col in cursor.fetchall()]
                
                cursor.execute(query)
                data = cursor.fetchall()

                text_widget4.delete(1.0, tk.END) 

                header = '    |   '.join(columns)
                text_widget4.insert(tk.END, header + "\n")
                text_widget4.insert(tk.END, "-" * len(header) + "\n")
                
                for row in data:
                    row_text = '   | '.join(map(str, row))
                    text_widget4.insert(tk.END, row_text + "\n\n")  

        except pymysql.MySQLError as e:
            print(f"MySQL error: {e}")

    def admin_student():
        clear5()
        query= f"select * from student "
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"SHOW COLUMNS FROM student ")
                columns = [col[0] for col in cursor.fetchall()]
                
                cursor.execute(query)
                data = cursor.fetchall()

                text_widget4.delete(1.0, tk.END) 

                header = '    |   '.join(columns)
                text_widget4.insert(tk.END, header + "\n")
                text_widget4.insert(tk.END, "-" * len(header) + "\n")
                
                for row in data:
                    row_text = '   | '.join(map(str, row))
                    text_widget4.insert(tk.END, row_text + "\n\n") 
                    
        except pymysql.MySQLError as e:
            print(f"MySQL error: {e}") 

    def admin_course():
        clear5()
        query= f"select * from course "
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"SHOW COLUMNS FROM course ")
                columns = [col[0] for col in cursor.fetchall()]
                
                cursor.execute(query)
                data = cursor.fetchall()

                text_widget4.delete(1.0, tk.END) 

                header = '    |   '.join(columns)
                text_widget4.insert(tk.END, header + "\n")
                text_widget4.insert(tk.END, "-" * len(header) + "\n")
                
                for row in data:
                    row_text = '   | '.join(map(str, row))
                    text_widget4.insert(tk.END, row_text + "\n\n")  

        except pymysql.MySQLError as e:
            print(f"MySQL error: {e}")

    def display_users():
        clear5()
        query= f"select * from users "
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"SHOW COLUMNS FROM users ")
                columns = [col[0] for col in cursor.fetchall()]
                
                cursor.execute(query)
                data = cursor.fetchall()

                text_widget4.delete(1.0, tk.END) 

                header = '    |   '.join(columns)
                text_widget4.insert(tk.END, header + "\n")
                text_widget4.insert(tk.END, "-" * len(header) + "\n")
                
                for row in data:
                    row_text = '   | '.join(map(str, row))
                    text_widget4.insert(tk.END, row_text + "\n\n")  

        except pymysql.MySQLError as e:
            print(f"MySQL error: {e}")

    def admin_grades():
        clear5()
        query= f"select * from grades"
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"SHOW COLUMNS FROM grades ")
                columns = [col[0] for col in cursor.fetchall()]
                
                cursor.execute(query)
                data = cursor.fetchall()

                text_widget4.delete(1.0, tk.END) 

                header = '    |   '.join(columns)
                text_widget4.insert(tk.END, header + "\n")
                text_widget4.insert(tk.END, "-" * len(header) + "\n")
                
                for row in data:
                    row_text = '   | '.join(map(str, row))
                    text_widget4.insert(tk.END, row_text + "\n\n")  

        except pymysql.MySQLError as e:
            print(f"MySQL error: {e}")

    def login():
        username = entry_username.get()
        password = entry_password.get()

        if username and password:
            hashed_password = hash_password(password)

            try:
                with conn.cursor() as cursor:
                    sql = "SELECT pass_hash FROM users WHERE u_name = %s"
                    cursor.execute(sql, (username,))
                    result = cursor.fetchone()

                    if result:
                        db_hashed_password = result[0]  # Access the first element of the tuple
                        if hashed_password == db_hashed_password:
                            messagebox.showinfo("Success", "Login successful!")
                            entry_username.delete(0, tk.END)
                            entry_password.delete(0, tk.END)
                            show_frame(home_frame)
                            # Add code to switch frames or perform other actions upon successful login
                        else:
                            messagebox.showerror("Login Failed", "Incorrect password!")
                    else:
                        messagebox.showerror("Login Failed", "Username not found!")

            except pymysql.Error as e:
                messagebox.showerror("Database Error", f"Error: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    def database_image():
        global image_label
        clear5()
        image_path = "database.jpg"  
        image = Image.open(image_path)
        image = image.resize((900, 570), Image.ANTIALIAS)  
        photo = ImageTk.PhotoImage(image)

        image_label = tk.Label(text_widget4, image=photo)
        image_label.image = photo  
        image_label.pack(pady=20)

    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register():
        username = entry_usernameadm.get()
        password = entry_passwordadm.get()
        if username and password:
            hashed_password = hash_password(password)
            try:
                with conn.cursor() as cursor:
                    # Insert user data into the database
                    sql = "INSERT INTO users (u_name, pass_hash) VALUES (%s, %s)"
                    cursor.execute(sql, (username, hashed_password))
                    conn.commit()

                messagebox.showinfo("Success", "User registered successfully!")
                entry_usernameadm.delete(0, tk.END)
                entry_passwordadm.delete(0, tk.END)
                show_frame(login_frame)

            except pymysql.Error as e:
                messagebox.showerror("Database Error", f"Error: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    
    def admin_login():
        admin_username= entry_username_admin.get()
        admin_password= entry_password_admin.get()
        if admin_username == adminUsername and admin_password == adminPassword:
                messagebox.showinfo("Admin Login Success",f"Welcome {admin_username}")
                entry_username_admin.delete(0, tk.END)
                entry_password_admin.delete(0, tk.END)
                show_frame(admin_frame)
    def clear1():
        text_widget.delete(1.0, tk.END)

    def clear2():
        text_widget1.delete(1.0, tk.END)

    def clear3():
        text_widget2.delete(1.0, tk.END)

    def clear4():
        text_widget3.delete(1.0, tk.END)
    
    def clear5():
        text_widget4.delete(1.0, tk.END)
        if image_label:
            image_label.destroy()  

    def clear6():
        entry_username.delete(0,tk.END)
        entry_password.delete(0,tk.END)

    def clear7():
        entry_usernameadm.delete(0,tk.END)
        entry_passwordadm.delete(0,tk.END)

    def close():
        root.destroy()

    root = tk.Tk()
    root.title('EduSchema ')
    root.geometry('1225x750')

    btn_hlb_bg = 'dim gray'
    btn_font = ('Times New Roman', 13)

    def show_frame(frame):
        frame.tkraise()

    container = tk.Frame(root)
    container.pack(side="top", fill="both", expand=True)

    home_frame = tk.Frame(container)
    course_frame = tk.Frame(container)
    student_frame = tk.Frame(container)
    instr_frame= tk.Frame(container)
    grades_frame = tk.Frame(container)
    admin_frame = tk.Frame(container)
    login_frame = tk.Frame(container)
    registration_frame=tk.Frame(container)
    admin_login_frame = tk.Frame(container)


    for frame in (home_frame, course_frame, student_frame,instr_frame,grades_frame,admin_frame,login_frame,registration_frame , admin_login_frame):
        frame.grid(row=0, column=0, sticky='nsew')

#home Frame 
    home_label = tk.Label(home_frame, text="Home Page", font=('Times New Roman', 20, 'bold'))
    home_label.pack(side="top", pady=10)

    nav_frame = tk.Frame(home_frame, bg="gray26")
    nav_frame.pack(side="top", fill="x")

    tk.Button(nav_frame, text='Home', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(home_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(nav_frame, text='Course', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(course_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(nav_frame, text='Student', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(student_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(nav_frame, text='Instructor', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(instr_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(nav_frame, text='Grades', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(grades_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(nav_frame, text='Admin', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(admin_login_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(nav_frame, text='Sign Up', font=('Times New Roman', 13), bg='dim gray', border=4, width=17, fg='white',command= lambda : show_frame(registration_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(nav_frame, text='Exit', font=('Times New Roman', 13), bg='dim gray', border=4, width=17, fg='white', command=root.quit).pack(side="left", padx=0, pady=5)

    image_path = "Untitled.png"  
    image = Image.open(image_path)
    image = image.resize((900, 570), Image.ANTIALIAS)  
    photo = ImageTk.PhotoImage(image)

    image_label = tk.Label(home_frame, image=photo)
    image_label.pack(pady=20)

    label = tk.Label(home_frame, text="Made by Divyanshu", font=('Times New Roman', 10, 'underline'))
    label.pack(side="right", fill="both")

#course Page 
    course_label = tk.Label(course_frame, text="Course Page", font=('Times New Roman', 20, 'bold'))
    course_label.pack(side="top", pady=10)

    course_nav_frame = tk.Frame(course_frame, bg="gray26")
    course_nav_frame.pack(side="top", fill="x")

    course_bottom_frame = tk.Frame(course_frame , bg="gray26")
    course_bottom_frame.pack(side="bottom", fill="x")

    text_widget = tk.Text(course_frame, wrap=tk.NONE, bg="gray63", font=('Times New Roman', 13))
    text_widget.pack(fill=tk.BOTH, expand=True)

    tk.Button(course_nav_frame, text='Home', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(home_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(course_nav_frame, text='Course', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(course_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(course_nav_frame, text='Student', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(student_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(course_nav_frame, text='Instructor', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(instr_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(course_nav_frame, text='Grades', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(grades_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(course_nav_frame, text='Admin', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(admin_login_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(course_nav_frame, text='Clear', font=('Times New Roman', 13), bg='dim gray', border=4, width=17, fg='white', command= clear1).pack(side="left", padx=0, pady=5)

    tk.Button(course_nav_frame, text='Exit', font=('Times New Roman', 13), bg='dim gray', border=4, width=17, fg='white', command=root.quit).pack(side="left", padx=0, pady=5)
    label = tk.Label(course_frame, text="Made by Divyanshu", font=('Times New Roman', 10, 'underline'))
    label.pack(side="right", fill="both")

    tk.Button(course_bottom_frame, text='Display Course ', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command= display_course).pack(side="left", padx=5, pady=5)

    tk.Button(course_bottom_frame, text='Add Course  ', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command= add_course).pack(side="left", padx=5, pady=5)

    tk.Button(course_bottom_frame, text='Delete Course', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command= delete_course).pack(side="left", padx=5, pady=5)

    tk.Button(course_bottom_frame, text='Restore Course ', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command= restore_course).pack(side="left", padx=5, pady=5)

    tk.Button(course_bottom_frame, text='Display Deleted Course ', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command= display_deleted_course).pack(side="left", padx=5, pady=5)

    tk.Button(course_bottom_frame, text='Clear', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command=clear1).pack(side="left", padx=5, pady=5)
    
#student page 

    student_label = tk.Label(student_frame, text="Student Page", font=('Times New Roman', 20, 'bold'))
    student_label.pack(side="top", pady=10)

    student_nav_frame = tk.Frame(student_frame, bg="gray26")
    student_nav_frame.pack(side="top", fill="x")

    student_bottom_frame = tk.Frame(student_frame, bg="gray26")
    student_bottom_frame.pack(side="bottom", fill="x")

    text_widget1 = tk.Text(student_frame, wrap=tk.NONE, bg="gray63", font=('Times New Roman', 13))
    text_widget1.pack(fill=tk.BOTH, expand=True)

    tk.Button(student_nav_frame, text='Home', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(home_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(student_nav_frame, text='Course', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(course_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(student_nav_frame, text='Student', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(student_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(student_nav_frame, text='Instructor', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(instr_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(student_nav_frame, text='Grades', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(grades_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(student_nav_frame, text='Admin', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(admin_login_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(student_nav_frame, text='Clear', font=('Times New Roman', 13), bg='dim gray', border=4, width=17, fg='white', command=clear2).pack(side="left", padx=0, pady=5)

    tk.Button(student_nav_frame, text='Exit', font=('Times New Roman', 13), bg='dim gray', border=4, width=17, fg='white', command=close).pack(side="left", padx=0, pady=5)

    label = tk.Label(student_frame, text="Made by Divyanshu", font=('Times New Roman', 10, 'underline'))
    label.pack(side="right", fill="both")

    tk.Button(student_bottom_frame, text='Display Student ', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command= display_student).pack(side="left", padx=5, pady=5)

    tk.Button(student_bottom_frame, text='Add Student  ', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command= add_student).pack(side="left", padx=5, pady=5)

    tk.Button(student_bottom_frame, text='Delete Student', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command= delete_student).pack(side="left", padx=5, pady=5)

    tk.Button(student_bottom_frame, text='Restore Student ', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command= restore_student).pack(side="left", padx=5, pady=5)

    tk.Button(student_bottom_frame, text='Display Deleted Student ', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command= display_deleted_student).pack(side="left", padx=5, pady=5)

    tk.Button(student_bottom_frame, text='Clear', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command=clear2).pack(side="left", padx=5, pady=5)
    
    
# instructor page 


    instructor_label = tk.Label(instr_frame, text="Instructor Page", font=('Times New Roman', 20, 'bold'))
    instructor_label.pack(side="top", pady=10)

    instructor_nav_frame = tk.Frame(instr_frame, bg="gray26")
    instructor_nav_frame.pack(side="top", fill="x")

    instructor_bottom_frame = tk.Frame(instr_frame, bg="gray26")
    instructor_bottom_frame.pack(side="bottom", fill="x")

    text_widget2 = tk.Text(instr_frame, wrap=tk.NONE, bg="gray63", font=('Times New Roman', 13))
    text_widget2.pack(fill=tk.BOTH, expand=True)

    tk.Button(instructor_nav_frame, text='Home', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(home_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(instructor_nav_frame, text='Course', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(course_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(instructor_nav_frame, text='Student', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(student_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(instructor_nav_frame, text='Instructor', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(instr_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(instructor_nav_frame, text='Grades', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(grades_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(instructor_nav_frame, text='Admin', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(admin_login_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(instructor_nav_frame, text='Clear', font=('Times New Roman', 13), bg='dim gray', border=4, width=17, fg='white', command=clear3).pack(side="left", padx=0, pady=5)

    tk.Button(instructor_nav_frame, text='Exit', font=('Times New Roman', 13), bg='dim gray', border=4, width=17, fg='white', command=close).pack(side="left", padx=0, pady=5)

    label = tk.Label(instr_frame, text="Made by Divyanshu", font=('Times New Roman', 10, 'underline'))
    label.pack(side="right", fill="both")

    tk.Button(instructor_bottom_frame, text='Display Instructor ', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command= display_instructors).pack(side="left", padx=5, pady=5)

    tk.Button(instructor_bottom_frame, text='Add Instructor  ', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command= add_instructor).pack(side="left", padx=5, pady=5)

    tk.Button(instructor_bottom_frame, text='Delete Instructor', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command= delete_instructor).pack(side="left", padx=5, pady=5)

    tk.Button(instructor_bottom_frame, text='Restore Instructor ', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command= restore_instructor).pack(side="left", padx=5, pady=5)

    tk.Button(instructor_bottom_frame, text='Display Deleted Instructor ', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command= display_deleted_instructor).pack(side="left", padx=5, pady=5)

    tk.Button(instructor_bottom_frame, text='Clear', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command=clear3).pack(side="left", padx=5, pady=5)

    
    
# Grades page 


    grades_label = tk.Label(grades_frame, text="Grades Page", font=('Times New Roman', 20, 'bold'))
    grades_label.pack(side="top", pady=10)

    grades_nav_frame = tk.Frame(grades_frame, bg="gray26")
    grades_nav_frame.pack(side="top", fill="x")

    grades_bottom_frame = tk.Frame(grades_frame, bg="gray26")
    grades_bottom_frame.pack(side="bottom", fill="x")


    text_widget3 = tk.Text(grades_frame, wrap=tk.NONE, bg="gray63", font=('Times New Roman', 13))
    text_widget3.pack(fill=tk.BOTH, expand=True)

    tk.Button(grades_nav_frame, text='Home', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(home_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(grades_nav_frame, text='Course', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(course_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(grades_nav_frame, text='Student', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(student_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(grades_nav_frame, text='Instructor', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(instr_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(grades_nav_frame, text='Grades', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(grades_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(grades_nav_frame, text='Admin', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(admin_login_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(grades_nav_frame, text='Clear', font=('Times New Roman', 13), bg='dim gray', border=4, width=17, fg='white', command=clear4).pack(side="left", padx=0, pady=5)

    tk.Button(grades_nav_frame, text='Exit', font=('Times New Roman', 13), bg='dim gray', border=4, width=17, fg='white', command=close).pack(side="left", padx=0, pady=5)

    label = tk.Label(grades_frame, text="Made by Divyanshu", font=('Times New Roman', 10, 'underline'))
    label.pack(side="right", fill="both")

    tk.Button(grades_bottom_frame, text='Display Grades ', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command= display_grades).pack(side="left", padx=5, pady=5)

    tk.Button(grades_bottom_frame, text='Add Grades  ', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command= add_grades).pack(side="left", padx=5, pady=5)

    tk.Button(grades_bottom_frame, text='Delete Grades', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command= delete_grades).pack(side="left", padx=5, pady=5)

    tk.Button(grades_bottom_frame, text='Restore Grades ', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command= restore_grades).pack(side="left", padx=5, pady=5)

    tk.Button(grades_bottom_frame, text='Display Deleted Grades ', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command= display_deleted_grades).pack(side="left", padx=5, pady=5)

    tk.Button(grades_bottom_frame, text='Clear', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command=clear4).pack(side="left", padx=5, pady=5)


#admin Page

    admin_label = tk.Label(admin_frame, text="Admin Page", font=('Times New Roman', 20, 'bold'))
    admin_label.pack(side="top", pady=10)

    admin_nav_frame = tk.Frame(admin_frame, bg="gray26")
    admin_nav_frame.pack(side="top", fill="x")
    admin_nav_frame1 = tk.Frame(admin_frame, bg="gray26")
    admin_nav_frame1.pack(side="top", fill="x")

    admin_center_frame = tk.Frame(admin_frame, bg="gray26")
    admin_center_frame.pack(side="top", fill="x")
    
    tk.Button(admin_nav_frame, text='Home', font=('Times New Roman', 13), bg='dim gray', border=4, width=15, fg='white', command=lambda: show_frame(home_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(admin_nav_frame,text='Show Database ', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command= database_image).pack(side="left", padx=5, pady=5)

    text_widget4 = tk.Text(admin_frame, wrap=tk.NONE, bg="gray63", font=('Times New Roman', 13))
    text_widget4.pack(fill=tk.BOTH, expand=True)


    tk.Button(admin_nav_frame,text='Exit', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command=close).pack(side="right", padx=5, pady=5)

    tk.Button(admin_nav_frame,text='Clear', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command=clear5).pack(side="right", padx=5, pady=5)


    tk.Button(admin_nav_frame1,text='Display Students', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command= admin_student).pack(side="left", padx=5, pady=5)

    tk.Button(admin_nav_frame1,text='Display Instructors', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command= admin_instructor).pack(side="left", padx=5, pady=5)

    tk.Button(admin_nav_frame1,text='Display Grades', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command= admin_grades).pack(side="left", padx=5, pady=5)

    tk.Button(admin_nav_frame1,text='Display Courses', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command= admin_course).pack(side="left", padx=5, pady=5)

    tk.Button(admin_nav_frame1,text='Display Departments', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command= display_department).pack(side="left", padx=5, pady=5)

    tk.Button(admin_nav_frame1,text='Display Users', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command= display_users).pack(side="left", padx=5, pady=5)

    
    label = tk.Label(admin_frame, text="Made by Divyanshu", font=('Times New Roman', 10, 'underline'))
    label.pack(side="right", fill="both")

# login page 
    login_label = tk.Label(login_frame, text="Login Page", font=('Times New Roman', 20, 'bold'))
    login_label.pack(side="top", pady=10)

    login_nav_frame = tk.Frame(login_frame, bg="gray26")
    login_nav_frame.pack(side="top", fill="x")

    login_center_frame = tk.Frame(login_frame, bg="gray26")
    login_center_frame.pack(side="top", fill="x")


    # tk.Button(login_nav_frame, text='Home', font=('Times New Roman', 13), bg='dim gray', border=4, width=17, fg='white', command=lambda: show_frame(home_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(login_nav_frame, text='Sign up ', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command=lambda: show_frame(registration_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(login_nav_frame, text='Exit', font=('Times New Roman', 13), bg='dim gray', border=4, width=17, fg='white', command=close).pack(side="right", padx=0, pady=5)

    tk.Button(login_nav_frame,text='Clear', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command=clear6).pack(side="right", padx=0, pady=5)

    image_path1 = "login.png"  
    image1 = Image.open(image_path1)
    image1 = image1.resize((350,200), Image.ANTIALIAS)  
    photo1 = ImageTk.PhotoImage(image1)

    image_label1 = tk.Label(login_center_frame, image=photo1 , bg="gray26")
    image_label1.pack(pady=10)

    label_username = tk.Label(login_center_frame, text="Username:",bg='gray26', fg='white',font=('Times New Roman', 20))
    label_username.pack(pady=10)
    entry_username = tk.Entry(login_center_frame, bg='dim gray',font=('Times New Roman', 15))
    entry_username.pack(pady=5)

    label_password = tk.Label(login_center_frame, text="Password:",bg='gray26',fg='white',font=('Times New Roman', 20))
    label_password.pack(pady=10)
    entry_password = tk.Entry(login_center_frame, show="*", bg='dim gray',font=('Times New Roman', 15))  # Show * for password
    entry_password.pack(pady=5)

    signup_page_label = tk.Label(login_center_frame, text="Don't have account ??", font=('Times New Roman', 10 ,"underline"), bg="gray26" ,fg="steel blue")
    signup_page_label.pack(side="top")
    signup_page_label.bind("<Button-1>",lambda e: show_frame(registration_frame))

    tk.Button(login_center_frame, text='Login', font=('Times New Roman', 13), bg='dim gray', border=4, width=17, fg='white', command=login).pack(side="bottom", padx=0, pady=25)

    
    label = tk.Label(login_frame, text="Made by Divyanshu", font=('Times New Roman', 10, 'underline'))
    label.pack(side="right", fill="both",padx=10)

#registration page 
    registration_label = tk.Label(registration_frame, text="Sign Up Page", font=('Times New Roman', 20, 'bold'))
    registration_label.pack(side="top", pady=10)

    signup_nav_frame = tk.Frame(registration_frame, bg="gray26")
    signup_nav_frame.pack(side="top", fill="x")

    signup_center_frame = tk.Frame(registration_frame, bg="gray26")
    signup_center_frame.pack(side="top", fill="x")

    
    
    # tk.Button(signup_nav_frame, text='Home', font=('Times New Roman', 13), bg='dim gray', border=4, width=17, fg='white', command=lambda: show_frame(home_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(signup_nav_frame, text='login  ', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command=lambda: show_frame(login_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(signup_nav_frame, text='Exit', font=('Times New Roman', 13), bg='dim gray', border=4, width=17, fg='white', command=close).pack(side="right", padx=0, pady=5)

    tk.Button(signup_nav_frame,text='Clear', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command=clear7).pack(side="right", padx=0, pady=5)

    image_path2 = "signup.png"  
    image2 = Image.open(image_path2)
    image2 = image2.resize((350,100), Image.ANTIALIAS)  
    photo2 = ImageTk.PhotoImage(image2)

    image_label2 = tk.Label(signup_center_frame, image=photo2 , bg="gray26")
    image_label2.pack(pady=10)


    label_usernameadm = tk.Label(signup_center_frame, text="Enter Username:",bg='gray26', fg='white',font=('Times New Roman', 20))
    label_usernameadm.pack(pady=10)
    entry_usernameadm = tk.Entry(signup_center_frame, bg='dim gray',font=('Times New Roman', 15))
    entry_usernameadm.pack(pady=5)

    label_passwordadm = tk.Label(signup_center_frame, text="Create your Password:",bg='gray26',fg='white',font=('Times New Roman', 20))
    label_passwordadm.pack(pady=10)
    entry_passwordadm = tk.Entry(signup_center_frame, bg='dim gray',font=('Times New Roman', 15) ,show="*")  # Show * for password
    entry_passwordadm.pack(pady=5)

    login_page_label = tk.Label(signup_center_frame, text="already signed up ??", font=('Times New Roman', 10 ,"underline"), bg="gray26" ,fg="steel blue")
    login_page_label.pack(side="top")
    login_page_label.bind("<Button-1>",lambda e: show_frame(login_frame))

    tk.Button(signup_center_frame, text='Sign Up', font=('Times New Roman', 13), bg='dim gray', border=4, width=17, fg='white', command=register).pack(side="bottom", padx=0, pady=25)

#login page for adminn 
    
    admin_login_label = tk.Label(admin_login_frame, text="Admin Login Page", font=('Times New Roman', 20, 'bold'))
    admin_login_label.pack(side="top", pady=10)

    adminlogin_nav_frame = tk.Frame(admin_login_frame, bg="gray26")
    adminlogin_nav_frame.pack(side="top", fill="x")

    admin_login_center_frame = tk.Frame(admin_login_frame, bg="gray26")
    admin_login_center_frame.pack(side="top", fill="x")


    tk.Button(adminlogin_nav_frame, text='Home', font=('Times New Roman', 13), bg='dim gray', border=4, width=17, fg='white', command=lambda: show_frame(home_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(adminlogin_nav_frame, text='Sign up ', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command=lambda: show_frame(registration_frame)).pack(side="left", padx=0, pady=5)

    tk.Button(adminlogin_nav_frame, text='Exit', font=('Times New Roman', 13), bg='dim gray', border=4, width=17, fg='white', command=close).pack(side="right", padx=0, pady=5)

    tk.Button(adminlogin_nav_frame,text='Clear', font=('Times New Roman', 13), bg='dim gray', border=4, width=20, fg='white', command=clear6).pack(side="right", padx=0, pady=5)

    image_path3 = "login.png"  
    image3 = Image.open(image_path3)
    image3 = image3.resize((350,200), Image.ANTIALIAS)  
    photo3 = ImageTk.PhotoImage(image3)

    image_label3 = tk.Label(admin_login_center_frame, image=photo3 , bg="gray26")
    image_label3.pack(pady=10)

    label_username_admin = tk.Label(admin_login_center_frame, text="Username:",bg='gray26', fg='white',font=('Times New Roman', 20))
    label_username_admin.pack(pady=10)
    entry_username_admin = tk.Entry(admin_login_center_frame, bg='dim gray',font=('Times New Roman', 15))
    entry_username_admin.pack(pady=5)

    label_password_admin = tk.Label(admin_login_center_frame, text="Password:",bg='gray26',fg='white',font=('Times New Roman', 20))
    label_password_admin.pack(pady=10)
    entry_password_admin = tk.Entry(admin_login_center_frame, show="*", bg='dim gray',font=('Times New Roman', 15))  
    entry_password_admin.pack(pady=5)

    tk.Button(admin_login_center_frame, text='Login', font=('Times New Roman', 13), bg='dim gray', border=4, width=17, fg='white', command=admin_login).pack(side="bottom", padx=0, pady=25)

    label = tk.Label(admin_login_frame, text="Made by Divyanshu", font=('Times New Roman', 10, 'underline'))
    label.pack(side="right", fill="both",padx=10)


    show_frame(login_frame  )
    root.update()
    root.mainloop()
    
except pymysql.MySQLError as e:
    print(f"MySQL error: {e}")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    
    if 'conn' in locals() and conn:
        conn.close()
        print("Connection closed")
    else:
        print("No connection to close")

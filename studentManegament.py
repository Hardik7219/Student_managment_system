import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
import json
import os

DATA_FILE = "students.json"
THEME="dark"
ISEDIT=False
# LOGIC
def load(): #load the present data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []
def save(): #save the info
    with open(DATA_FILE,"w") as f:
        json.dump(students,f,indent=4)
        
students=load()
def add(): #add the student
    name = Name.get()
    rollno= rollNo.get()
    course_name= course.get()
    cls= Class.get()
    if( name=="" or rollno =="" or course_name =="" or cls==""):
        messagebox.showwarning("input error","Fields are empty")
    else :
        students.append({
            "Rollno": rollno,
            "Name": name,
            "Class": cls,
            "Course": course_name
        })

        student_table.insert(
        "",
        "end",
        values=(rollno, name, cls, course_name)
    )
    Name.delete(0, "end")
    rollNo.delete(0, "end")
    course.delete(0, "end")
    Class.delete(0, "end")
    save()
    
def refresh_view(data=None): #refresh the table
    student_table.delete(*student_table.get_children())
    if data:
        for student in data:
            student_table.insert(
                "",
                "end",
                values=(
                    student["Rollno"],
                    student["Name"],
                    student["Class"],
                    student["Course"]
                )
            )
    else:
        for student in students:
            student_table.insert(
                "",
                "end",
                values=(
                    student["Rollno"],
                    student["Name"],
                    student["Class"],
                    student["Course"]
                )
            )

def delete():#delete the student info
    confirm=messagebox.askyesno("Delete","Do you want delete?")
    if not confirm :
        return
    selectIndex= student_table.focus()
    if not selectIndex :
        return
    indexSel= student_table.index(selectIndex)
    students.pop(indexSel)
    save()
    refresh_view()
    
def edit():#edit the student
    global ISEDIT
    selected = student_table.focus()
    if not selected:
        messagebox.showwarning("Select Error", "Please select a student to edit")
        return

    values = student_table.item(selected, "values")

    Name.delete(0, "end")
    rollNo.delete(0, "end")
    Class.delete(0, "end")
    course.delete(0, "end")

    rollNo.insert(0, values[0])
    Name.insert(0, values[1])
    Class.insert(0, values[2])
    course.insert(0, values[3])
    ISEDIT=True
def update():#update the editade info
    global ISEDIT
    selectIndex= student_table.focus()
    name = Name.get()
    rollno= rollNo.get()
    course_name= course.get()
    cls= Class.get()
    if not selectIndex or name=="" or rollno =="" or course_name =="" or cls=="" or ISEDIT==False:
        messagebox.showwarning("input error","Fields are empty or First click Edit Button ")
        return
    new_data = (
        rollNo.get(),
        Name.get(),
        Class.get(),
        course.get()
    )
    student_table.item(selectIndex, values=new_data)
    indexSel= student_table.index(selectIndex)
    students[indexSel]={
        "Rollno": new_data[0],
        "Name": new_data[1],
        "Class": new_data[2],
        "Course": new_data[3]
    }    
    ISEDIT=False
    save()
def clearField():#clear input fields
    Name.delete(0, "end")
    rollNo.delete(0, "end")
    Class.delete(0, "end")
    course.delete(0, "end")

def searchStudent():
    val=searchName.get().lower()
    filterDAta= [s for s in students if val in s["Name"].lower() or val in s["Rollno"]]
    refresh_view(filterDAta)
    
def toggleTheme(): # change the theme 
    global THEME
    if THEME =="dark" :
        THEME = "light"
    else :
        THEME ="dark"
    ctk.set_appearance_mode(THEME)
    theme_btn.configure(text=THEME.upper())




#UI
ctk.set_appearance_mode(THEME)
root=ctk.CTk()
root.geometry("900x500")
root.title("Student Management System")
root.resizable(False,False)
root.columnconfigure(0,weight=1)

#title or nav 
navbar_frame=ctk.CTkFrame(
    root,
    fg_color="transparent"
)
navbar_frame.grid(
    row=0, 
    column=0, 
    pady=5,
    sticky="we"
)
navbar_frame.grid_columnconfigure(0, weight=1)

#input and add button
search_frame=ctk.CTkFrame(
    navbar_frame,
    fg_color="transparent",
)
search_frame.grid(
    row=0,
    column=0,
    pady=5,
    padx=5,
)

searchName=ctk.CTkEntry(
    search_frame,
    width=250,
    placeholder_text="Search student..."
)
searchName.grid(
    pady=10,
    row=0,
    column=1
)
search_button=ctk.CTkButton(
    search_frame,
    text="Search",
    fg_color="lightgreen",
    height=30,
    width=50,
    text_color="black",
    command=searchStudent
)
search_button.grid(
    row=0,
    column=2,
    padx=5
)
action_frame = ctk.CTkFrame(
    navbar_frame,
    fg_color="transparent"
)
action_frame.grid(
    row=0,
    column=1,
    padx=10,
    pady=5
)
theme_btn=ctk.CTkButton(
    action_frame,
    height=30,
    width=50,
    command=toggleTheme,
    text_color="white",
    hover_color="gray",
    fg_color="#5a605e"
)
theme_btn.grid(
    row=0,
    column=0,
    sticky="we"
)
theme_btn.configure(text=THEME.upper())



main_frame=ctk.CTkFrame(
    root,
    fg_color="transparent",
    height=400

)
main_frame.grid(
    sticky="we"
)
main_frame.columnconfigure(0,weight=1)
main_frame.grid_propagate(False)

input_frames=ctk.CTkFrame(
    main_frame,
    fg_color="transparent",
    width=300,
    height=400
)
input_frames.grid(
    row=0,
    column=0,
    sticky="w"
)
input_frames.columnconfigure(0,weight=1)
input_frames.grid_propagate(False)

field_frame=ctk.CTkFrame(
    input_frames,
    fg_color="transparent",
    height=250,
)
field_frame.grid(
    row=0,
    column=0,
    sticky="we"

)
field_frame.columnconfigure(0,weight=1)
field_frame.grid_propagate(False)

ctk.CTkLabel(
    field_frame,
    text="STUDENT DETAIL",
    font=("arial",20,"bold")
).grid(
    row=0,
    column=0
    )

Name=ctk.CTkEntry(
    field_frame,
    placeholder_text="Name",
    width=290,
    height=30
)
Name.grid(
    row=1,
    column=0,
    pady=10,
    padx=5,

)
rollNo=ctk.CTkEntry(
    field_frame,
    placeholder_text="rollNo",
    width=290,
    height=30
)
rollNo.grid(
    row=2,
    column=0,
    pady=10,
    padx=5
    )
course=ctk.CTkEntry(
    field_frame,
    placeholder_text="course",
    width=290,
    height=30
)
course.grid(
    row=3,
    column=0,
    pady=10,
    padx=5
    )
Class=ctk.CTkEntry(
    field_frame,
    placeholder_text="Class",
    width=290,
    height=30
)
Class.grid(
    row=4,
    column=0,
    pady=10,
    padx=5
    )

option_frame=ctk.CTkFrame(
    input_frames,
    fg_color="transparent",
    height=150
)
option_frame.grid(
    row=1,
    column=0,
    sticky="we"
)
option_frame.columnconfigure(0,weight=1)
option_frame.grid_propagate(False)

add_button=ctk.CTkButton(
    option_frame,
    text="ADD",
    width=100,
    command=add
)
add_button.grid(
    row=0,
    column=0,
    padx=5,
    pady=5,
    sticky="w"
)

delete_button=ctk.CTkButton(
    option_frame,
    text="delete",
    width=100,
    command=delete
)
delete_button.grid(
    row=0,
    column=1,
    padx=5,
    pady=5,
)
    
edit_button=ctk.CTkButton(
    option_frame,
    text="Edit",
    width=100,
    command=edit
)
edit_button.grid(
    row=1,
    column=0,
    padx=5,
    pady=5,
    sticky="w" 
)
update_button=ctk.CTkButton(
    option_frame,
    text="Update",
    width=100,
    command=update
)
update_button.grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)

clear_button=ctk.CTkButton(
    option_frame,
    text="clear",
    width=100,
    command=clearField
)
clear_button.grid(
    row=2,
    column=0,
    padx=5,
    pady=5,
    sticky="w"
)

refresh_button=ctk.CTkButton(
    option_frame,
    text="Refresh",
    width=100,
    command=refresh_view
)
refresh_button.grid(
    row=2,
    column=1,
    padx=5,
    pady=5
)
list_frame=ctk.CTkFrame(
    main_frame,
    fg_color="transparent",
    width=600,
    height=400
)
list_frame.grid(
    row=0,
    column=1,
)


list_frame.columnconfigure(0,weight=1)
list_frame.grid_propagate(False)

columns = ("Roll No","Name", "Class","Course")

student_table = ttk.Treeview(
    list_frame,
    columns=columns,
    height=300,
    show="headings"
)
student_table.grid(
    row=0,
    column=0,
    sticky="we"
)

for col in columns:
    student_table.heading(col,text=col)


student_table.column("Roll No", width=60, anchor="center")
student_table.column("Name", width=300, anchor="center")
student_table.column("Class", width=60, anchor="center")
student_table.column("Course", width=60, anchor="center")

refresh_view()

root.mainloop()
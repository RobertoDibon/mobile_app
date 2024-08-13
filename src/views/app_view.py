import flet as ft
from db_conection import DbDataUser
from fpdf import FPDF
import datetime
import string
import random
import time
    
class AppView(ft.View):
    def __init__(
        self,
        page: ft.Page,
    ):
        
        super().__init__() 

        #Variables
        self.page = page

        self.data = DbDataUser()

        self.selected_row = None

        self.reference = ft.TextField(
            label= "Reference", 
            border_color= "blue", 
            label_style = ft.TextStyle(color = "#F2F2F2"),
            width = 100
        )

        self.user = ft.TextField(
            label= "User", 
            border_color= "blue",
            label_style = ft.TextStyle(color = "#F2F2F2"),
            width = 100
        )

        self.password = ft.TextField(
            label= "Password", 
            border_color= "blue",
            label_style = ft.TextStyle(color = "#F2F2F2"),
            width = 100,
            tooltip = "Max 10 Characters",
        )

        self.search_field = ft.TextField(
            width = 120,
            label = "Search",
            suffix_icon = ft.icons.SEARCH,
            border = ft.InputBorder.UNDERLINE,
            border_color = "blue",
            label_style = ft.TextStyle(color = "#F2F2F2"),
            on_change = self.search_data
        )

        self.data_table = ft.DataTable(
            show_checkbox_column = True,
            checkbox_horizontal_margin = 5,
            column_spacing = 5,
         

            columns = [
                ft.DataColumn(
                    ft.Text("Reference", size = 14,
                    color = "#F2F2F2"
                    )
                ),
                ft.DataColumn(
                    ft.Text("User", size = 14,
                    color = "#F2F2F2"
                    )
                ),
                ft.DataColumn(
                    ft.Text("Pass", size = 14,
                    color = "#F2F2F2",
                    )
                )
            ],
        )

        self.error_field = ft.Text(value = "", italic = True, size = 0)

        self.password_switch = ft.Switch(
            scale = 0.45,
            tooltip = "Show password",
            value = False,
            on_change = self.switch_pass
        ) 
        

        self.show_data()


        self.controls = [
            ft.SafeArea(
                minimum = 5,
                content = ft.Column(
                    horizontal_alignment = "center",
                    controls = [    
                        #Top menu
                        ft.Container(
                            border_radius = ft.border_radius.only(top_left = 15, top_right = 15),
                            content = ft.Row(
                                alignment = ft.MainAxisAlignment.SPACE_AROUND,
                                controls = [
                                        ft.Image(
                                            src=f"src/img/lock.svg",
                                            width= 80,
                                            height= 80,
                                        ),
                                        self.search_field,
                                        ft.IconButton(
                                            scale = 0.85,
                                            icon = ft.icons.EDIT,
                                            on_click =  self.edit_field
                                        ),
                                        ft.IconButton(
                                            scale = 0.85,
                                            tooltip = "Download Pdf List",
                                            icon = ft.icons.PICTURE_AS_PDF,
                                            on_click =  self.save_pdf
                                        ),
                                        ft.IconButton(
                                            scale = 0.85,
                                            icon = ft.icons.EXIT_TO_APP_SHARP,
                                            on_click = lambda e: self.exit_app(),
                                        ),
                                    ]
                                ),
                                gradient = ft.LinearGradient([
                                    ft.colors.BLUE_ACCENT,
                                    ft.colors.BLACK87
                                ])  
                        ),

                        #Entry data menu
                        ft.Container(
                            border_radius = 20,
                            content = ft.Row(
                                alignment = ft.MainAxisAlignment.SPACE_AROUND,
                                controls = [
                                    ft.TextButton(
                                        text = "Generate Pass",
                                        icon = ft.icons.PASSWORD,
                                        tooltip = "New Random Pass",
                                        on_click =  self.generate_password
                                    ),
                                    ft.IconButton(
                                        icon = ft.icons.SAVE,
                                        on_click = self.add_data
                                    ),
                                    ft.IconButton(
                                        icon = ft.icons.UPDATE,
                                        on_click = self.update_data
                                    ),
                                    ft.IconButton(
                                        icon = ft.icons.DELETE,
                                        on_click = self.delete_data
                                    ),     
                                    self.password_switch
                                ]
                            )
                        ),

                        ft.Divider(height = 3, color = "transparent"),    
                        self.error_field,
                    
                        #Entry data
                        ft.Container(
                            content = ft.Row(
                                alignment = ft.MainAxisAlignment.SPACE_AROUND,
                                controls = [
                                    self.reference,
                                    self.user,
                                    self.password
                                ]
                            )
                        ),

                        #Data table
                        ft.Container(
                            border = ft.border.all(1, "blue"),
                            border_radius = 15,
                            content = ft.Column(
                                spacing = 5,
                                height = 370,
                                scroll = ft.ScrollMode.AUTO,
                                controls = [
                                    ft.ResponsiveRow([
                                        self.data_table,
                                    ])
                                ]
                            )
                        )
                    ]
                )
            )
        ]
    
    
    #Methods
    def show_data(self):
        self.data_table.rows = []
        sorted_data = sorted(self.data.get_reference(), key=lambda x: x[1])
        for x in sorted_data:
            self.data_table.rows.append(
                ft.DataRow(
                    on_select_changed=self.get_index,
                    cells=[
                        ft.DataCell(ft.Text(x[1])),
                        ft.DataCell(ft.Text(x[2])),
                        ft.DataCell(ft.Text("********"))
                    ]
                )
            )
        self.update()

    def show_password(self):
        self.data_table.rows = []
        sorted_data = sorted(self.data.get_reference(), key=lambda x: x[1])

        for x in sorted_data:
            self.data_table.rows.append(
                ft.DataRow(
                    on_select_changed=self.get_index,
                    cells=[
                        ft.DataCell(ft.Text(x[1])),
                        ft.DataCell(ft.Text(x[2])),
                        ft.DataCell(ft.Text(x[3])),
                    ]
                )
            )
    
    #Gets the content of each row
    def get_index(self, e):
        if e.control.selected:
            e.control.selected = False
        else:
            e.control.selected = True
        
        reference = e.control.cells[0].content.value
        for row in self.data.get_reference():
            if row[1] == reference:
                self.selected_row = row
                break
        
        self.update()
    
    def add_data(self, e):
        reference_comparative = self.reference.value.lower()
        user = self.user.value
        password = self.password.value

        if len(reference_comparative) >0 and len(user) >0 and len(password)>0:
            existing_data = False
            for row in self.data.get_reference():
                if row[1].lower() == reference_comparative:
                    existing_data = True
                    
                    self.error_field.value = "Reference already exist"
                    self.error_field.color = "red"
                    self.error_field.size = 12
                    self.error_field.update()
                    time.sleep(1)
                    self.error_field.size = 0
                    self.error_field.update()
                    
                    break

            if not existing_data:
                reference = self.reference.value
                self.clean_fields()
                self.data.add_reference(reference, user, password)
                
                self.error_field.value = "New reference add"
                self.error_field.color = "blue"
                self.error_field.size = 12 
                self.error_field.update()
                time.sleep(1)
                self.error_field.size = 0
                self.error_field.update()

                self.show_data()

        else:
            self.error_field.value = "Complete all fields..."
            self.error_field.color = "red"
            self.error_field.size = 12
            self.error_field.update()
            time.sleep(1)
            self.error_field.size = 0
            self.error_field.update()
            

    def update_data(self, e):
        reference = self.reference.value
        user = self.user.value
        password = self.password.value

        if len(reference) and len(user) and len(password)>0:
            self.clean_fields()
            self.data.update_reference(self.selected_row[0], reference, user, password)
            
            self.error_field.value = "Reference updated"
            self.error_field.color = "blue"
            self.error_field.size = 12
            self.error_field.update()
            time.sleep(1)
            self.error_field.size = 0
            self.error_field.update()

            self.search_field.value = ""
            self.show_data()

        else:
            self.error_field.value = "No data selected"
            self.error_field.color = "red"
            self.error_field.size = 12
            self.error_field.update()
            time.sleep(1)
            self.error_field.size = 0
            self.error_field.update()
            
    def delete_data(self, e):
        self.data.delete_reference(self.selected_row[0]) 

        self.error_field.value = "Reference deleted"
        self.error_field.color = "red"
        self.error_field.size = 12
        self.error_field.update()
        time.sleep(1)
        self.error_field.size = 0
        self.error_field.update()

        self.search_field.value = ""
        self.clean_fields()
        self.show_data()

    def search_data(self, e):
        search = self.search_field.value.lower()
        reference = list(filter(lambda x: search in x[1].lower(), self.data.get_reference()))
        self.data_table.rows = []
        if not self.search_field.value == "":
            if len (reference)>0:
                for x in reference:
                    self.data_table.rows.append(
                        ft.DataRow(
                            on_select_changed = self.get_index,
                            cells = [
                                ft.DataCell(ft.Text(x[1])),
                                ft.DataCell(ft.Text(x[2])),
                                ft.DataCell(ft.Text("********"))
                            ]
                        )
                    )
                    self.update()
        else:
            self.show_data()  

    def edit_field(self, e):
        try:
            self.reference.value = self.selected_row[1]
            self.user.value = self.selected_row[2]
            self.password.value = self.selected_row[3]
            self.search_field.value = ""
            self.update()
            
            
        except TypeError:
            self.error_field.value = "No row selected"
            self.error_field.color = "red"
            self.error_field.size = 12
            self.error_field.update()
            time.sleep(1)
            self.error_field.size = 0
            self.error_field.update()

    def clean_fields(self):
        self.reference.value = ""
        self.user.value = ""
        self.password.value = ""
    
    def save_pdf(self, e):
        pdf = Pdf()
        pdf.add_page()
        columns_widths = [40, 80, 40] 
        data = sorted(self.data.get_reference(), key=lambda x: x[1])
        header = ("REFERENCE", "USER", "PASSWORD")  
        filtered_data = []
        for row in data:
            filtered_row = [row[1], row[2], row[3]]  #Filtered rows, without ID
            filtered_data.append(filtered_row)

        filtered_data.insert(0, header)  

        for row in filtered_data:
            for item, width in zip(row, columns_widths):
                pdf.cell(width, 10, str(item), border=1)
            pdf.ln()

        file_name = datetime.datetime.now()
        file_name = file_name.strftime("My_list %Y-%m-%d_%H-%M-%S") + ".pdf"
        pdf.output(file_name)

        self.error_field.value = "Pdf created successfully"
        self.error_field.color = "blue"
        self.error_field.size = 12
        self.error_field.update()
        time.sleep(1)
        self.error_field.size = 0
        self.error_field.update()

    def generate_password(self, e):
        characteres = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characteres) for _ in range(10))
        self.password.value = password
        self.show_data()

    def exit_app(self):
        self.page.window_destroy()

    def switch_pass(self, e):
        if e.control.value :
            self.show_password()
        else:
            self.show_data()
        self.update()
    
class Pdf(FPDF):
    def header(self):
        self.set_font("Arial", "", 12),
        self.cell(0, 10, "MY PASSWORDS", 0, 1, "C")

    def footer(self):
        self.set_y(-15),
        self.set_font("Arial", "B", 8),
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")
    

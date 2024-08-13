import flet as ft
from db_conection import DbUser
import time
from werkzeug.security import check_password_hash

class LoginView(ft.View):
    def __init__(
        self,
        page: ft.Page,
    ):
        #Constructor variables
        self.page = page
       
        self.db_user = DbUser()
       
        self.error_field = ft.Text(value = "", italic = True, size = 0)

        super().__init__()

        #Variables
        self.image = ft.Image(
            src=f"src/img/lock.svg",
            width= 100,
            height= 100,
        )
      
        self.password = ft.TextField(
            width = 280,
            height = 40,
            hint_text = "Password",
            border = "underline",
            color = "white",
            prefix_icon = ft.icons.LOCK,
            password = True,
            can_reveal_password = True
        )

        self.controls = [
            ft.SafeArea(
                minimum = 5, 
                content = ft.Column(
                    horizontal_alignment = "center",
                    controls = [
                        #Top menu
                        ft.Container(
                            alignment = ft.alignment.center,
                            border_radius = ft.border_radius.only(top_left = 15, top_right = 15),
                            content = ft.Row(
                                height = 80,
                                alignment = "end",
                                controls =[
                                    ft.IconButton(
                                        scale = 0.85,
                                        icon = ft.icons.EXIT_TO_APP_SHARP,
                                        on_click = lambda e: self.exit_app(),
                                    ),
                                ],
                            ),
                            gradient = ft.LinearGradient([
                                ft.colors.BLUE_ACCENT,
                                ft.colors.BLACK87
                            ])  
                        ),

                        ft.Divider(height = 10, color = "transparent"),    
                        self.error_field,

                        #Logo
                        ft.Container(
                            alignment = ft.alignment.center,
                            border_radius = ft.border_radius.only(top_left = 15, top_right = 15),
                            content = ft.Column(
                                horizontal_alignment = "center",
                                controls = [
                                self.image,
                                ft.Text(
                                    "Login",
                                    size = 30,
                                    width = 320,
                                    text_align = "center",
                                    weight = "w900",
                                    ),
                                ],
                            ), 
                        ),

                        #Entry data
                        ft.Container(
                            alignment = ft.alignment.center,
                            content = ft.Column(
                                controls = [
                                    ft.Container(
                                        content = ft.Column(
                                            horizontal_alignment = "center",
                                            controls = [
                                                self.password,
                                                ft.ElevatedButton(
                                                    text = "Enter",
                                                    width = 280,
                                                    bgcolor = "black",
                                                    on_click = lambda e: self.check_user(),
                                                ),
                                            ]
                                        )
                                    )
                                ]
                            )
                        ),

                        ft.Divider(height = 80, color = "transparent"),

                        #Footer
                        ft.Container(
                            alignment = ft.alignment.center,
                            border_radius = ft.border_radius.only(bottom_left = 15, bottom_right = 15),
                            content = ft.Row(
                                height = 80,
                                alignment = "center",
                                controls =[
                                    ft.Text(
                                        "New to the app ? Register",
                                        spans = [
                                            ft.TextSpan(
                                                " here,", 
                                                style = ft.TextStyle(italic = True),
                                                on_click = lambda _: page.go('/register')
                                            )
                                        ],
                                    ),
                                ],
                            ),
                            gradient = ft.LinearGradient([
                                ft.colors.BLUE_ACCENT,
                                ft.colors.BLACK87
                            ])  
                        ),
                    ],
                ), 
            )
        ]
    
    
    #Methods
    def check_user(self):
        password = self.password.value

        if len (password) > 0:
            #If there is an entry but there is no data in the database
            if not self.db_user.has_records():
                self.error_field.value = "Please register!"
                self.error_field.color = "red"
                self.error_field.size = 12
                self.error_field.update()
                time.sleep(1)
                self.error_field.size = 0
                self.error_field.update()  
                self.clean_fields()
                self.update()
            else:
                pwd_encrypted = self.db_user.get_password()
            
                #If the password was found, verify it
                if check_password_hash(pwd_encrypted, password):
                    self.error_field.value = "Access successfully!"
                    self.error_field.color = "blue"
                    self.error_field.size = 12
                    self.error_field.update()
                    time.sleep(1)
                    self.error_field.size = 0
                    self.error_field.update()
                    self.clean_fields()
                    self.page.go('/app')   
                else:
                    self.error_field.value = "**The password is incorrect**"
                    self.error_field.color = "red"
                    self.error_field.size = 12
                    self.error_field.update()
                    time.sleep(1)
                    self.error_field.size = 0
                    self.error_field.update()  
                    self.clean_fields()
                    self.update()
        #If there is no entry
        else:    
            self.error_field.value = "Please enter a valid password!"
            self.error_field.color = "red"
            self.error_field.size = 12
            self.error_field.update()
            time.sleep(1)
            self.error_field.size = 0
            self.error_field.update()  
            self.clean_fields()
            self.update()  

    def clean_fields(self):
        self.password.value = ""

    def exit_app(self):
        self.page.window_destroy()
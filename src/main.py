import flet as ft
from views.login_view import LoginView
from views.register_view import RegisterView
from views.app_view import AppView

#Main function
def main(page: ft.Page):
    page.window_height = 660
    page.window_width = 360
    page.window_min_height = 660
    page.window_min_width = 360
    page.title = 'Password Reminder App'    


    #Variables
    login = LoginView(page)
    register = RegisterView(page)
    app = AppView(page)


    #Function
    def change_route(route):
        page.views.clear()

        if page.route =="/":
            page.views.append(login)

        if page.route =="/register":
            page.views.append(register)

        if page.route =="/app":
            page.views.append(app)
        
        page.update()

    page.views.append(login) 
    page.on_route_change = change_route

    page.update()

ft.app(main)
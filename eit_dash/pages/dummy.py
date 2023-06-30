from dash import html, register_page

# from app import app

register_page(__name__, path='/right')

layout = html.Div('this is a dummy page')

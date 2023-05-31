from dash import register_page, html
# from app import app

register_page(__name__, path='/left')

layout = html.Div('this is the left page')

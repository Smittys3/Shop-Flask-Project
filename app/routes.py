from flask_login import current_user
from app import app
from flask import render_template, request, redirect, url_for, flash

from app.forms import PokemonForm

from .models import User, Pokemon

import requests

@app.route('/')
def index():
    users = User.query.order_by(User.username).all()
    new_list = []
    following_set = set()
    if current_user.is_authenticated:
        following = current_user.followed.all()
        following_set = {f.id for f in following}
    for u in users:
        if u.id in following_set:
            u.flag = True        

    return render_template('index.html', names=users)

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/hi')
def hi():
    return render_template('contact.html')


@app.route('/search', methods=["GET", "POST"])
def searchForPokemon():
    form = PokemonForm()
    pokemon_dict={}
    is_caught = False
    if request.method == "POST":
        if form.validate():
            name = form.pokemon_name.data

            response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}')
            data = response.json()
            pokemon_dict = {
                'name':data['name'],
                'ability':data['abilities'][0]['ability']['name'],
                'hp':str(data['stats'][0]['base_stat']),
                'attack':str(data['stats'][1]['base_stat']),
                'defense':str(data['stats'][2]['base_stat']),
                'img_url':data['sprites']['front_shiny']
            }
            pokemon = Pokemon.query.filter_by(name=pokemon_dict['name']).first()
            if not pokemon:
                pokemon = Pokemon(pokemon_dict['name'], pokemon_dict['ability'], pokemon_dict['hp'], pokemon_dict['attack'], pokemon_dict['defense'], pokemon_dict['img_url'])
                pokemon.save()

            if current_user.team.filter_by(name=pokemon.name).first():
                is_caught = True
                
    return render_template('search.html', form = form, pokemon_dict=pokemon_dict, is_caught=is_caught)


@app.route('/catch/<string:pokemon_name>')
def catchPokemon(pokemon_name):
    # user
    current_user
    # pokemon
    pokemon = Pokemon.query.filter_by(name=pokemon_name).first()
    if len(current_user.team.all()) < 5:
        current_user.team.append(pokemon)
        current_user.saveToDB()
    else:
        flash('Your team is already full!', 'danger')

    # assume catch function works
    return redirect(url_for('searchForPokemon'))

@app.route('/release/<string:pokemon_name>')
def releasePokemon(pokemon_name):
    pokemon = Pokemon.query.filter_by(name=pokemon_name).first()
    current_user.team.remove(pokemon)
    current_user.saveToDB()
    return redirect(url_for('searchForPokemon'))

@app.route('/team')
def getMyTeam():
    team = current_user.team.all()
    return render_template('myteam.html', team = team)

@app.route('/battle/<string:opponent>')
def battle(opponent):
    op = User.query(name=opponent)
    op.team.all()
    current_user.team.all()
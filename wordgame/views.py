from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from authorization.models import Profile
from .models import Word, Attempt, Game
from .forms import GuessWordForm

def initialize_game(request):
    """Инициализация игры, если она еще не начата."""
    word = Word.objects.order_by('?').first()
    game = Game.objects.create(user=request.user, word=word)
    request.session['game_id'] = game.id
    request.session['attempts'] = 6
    return game

def get_previous_attempts(game):
    """Получение предыдущих попыток пользователя и форматирование их для отображения."""
    previous_attempts = []
    for attempt in Attempt.objects.filter(game=game):
        previous_attempt = ""
        for i in range(5):
            if attempt.guessed_word[i].lower() == game.word.word[i].lower():
                previous_attempt += f'<input type="text" class="code-input green" value="{attempt.guessed_word[i].upper()}" readonly>'
            elif attempt.guessed_word[i].lower() in game.word.word.lower():
                previous_attempt += f'<input type="text" class="code-input orange" value="{attempt.guessed_word[i].upper()}" readonly>'
            else:
                previous_attempt += f'<input type="text" class="code-input gray" value="{attempt.guessed_word[i].upper()}" readonly>'
        previous_attempts.append(previous_attempt)
    return previous_attempts

def process_post_request(request, form, game, attempts):
    """Обработка POST-запроса: проверка угаданного слова и обновление попыток."""
    if form.is_valid():
        guessed_word = form.cleaned_data['guessed_word']
        attempts -= 1
        request.session['attempts'] = attempts
        
        attempt = Attempt(game=game, guessed_word=guessed_word, attempts=attempts)
        attempt.save()

        if guessed_word.lower() == game.word.word.lower():
            return redirect('game_win')

        if attempts <= 0:
            return redirect('game_lose')

        return redirect('game_home')

@login_required
def game_home(request):
    if 'game_id' not in request.session:
        game = initialize_game(request)
    else:
        game = get_object_or_404(Game, id=request.session['game_id'])
    attempts = request.session.get('attempts', 6)
    form = GuessWordForm()
    
    previous_attempts = get_previous_attempts(game)

    if request.method == 'POST':
        form = GuessWordForm(request.POST)
        response = process_post_request(request, form, game, attempts)
        if response:
            return response

    return render(request, 'wordgame/game_home.html', {'form': form, 'attempts': attempts, 'word': game.word.word, 'previous_attempts': previous_attempts})

@login_required
def game_win(request):
    game = get_object_or_404(Game, id=request.session['game_id'])
    game.completed_at = timezone.now()
    game.win = True
    game.save()

    profile = request.user.profile
    profile.rating += 5
    profile.save()
    
    request.session.pop('game_id', None)
    request.session.pop('attempts', None)
    return render(request, 'wordgame/game_win.html')

@login_required
def game_lose(request):
    game = get_object_or_404(Game, id=request.session['game_id'])
    game.completed_at = timezone.now()
    game.save()
    word = game.word.word
    request.session.pop('game_id', None)
    request.session.pop('attempts', None)
    return render(request, 'wordgame/game_lose.html', {'word': word})

@login_required
def game_history(request):
    games = Game.objects.filter(user=request.user, completed_at__isnull=False).order_by('-created_at')
    return render(request, 'wordgame/game_history.html', {'games': games})

@login_required
def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id, user=request.user)
    attempts = get_previous_attempts(game)
    return render(request, 'wordgame/game_detail.html', {'game': game, 'attempts': attempts})


def leaderboard(request):
    # Получить первые 10 пользователей, отсортированных по рейтингу в убывающем порядке
    top_players = Profile.objects.order_by('-rating')[:100]
    return render(request, 'wordgame/leaderboard.html', {'top_players': top_players})



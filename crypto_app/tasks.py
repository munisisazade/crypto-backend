from __future__ import absolute_import, unicode_literals
from .models import Alphabed
import math
from itertools import *

from celery import shared_task


# Use celery shared_task documentation here
# http://docs.celeryproject.org/en/latest/faq.html
@shared_task
def topla(a, b):
    return a + b


@shared_task
def create_alphabet(_list):
    iterable_symbols = tuple(_list)  # elifba tuple - a convert edir "ABCDE" => ("A", "B", "C", "D", "E" )
    number_of_repeats = math.factorial(
        len(iterable_symbols))  # Əlifbanin sayına uyğun olaraq bütün mümkün variantların sayını tapıram
    number_of_iterables = len(iterable_symbols)  # Əlifabanın hərflərinin sayını tapıram
    number_of_conditions = number_of_repeats / number_of_iterables  # Bir hərflə başlayan sətrlərin sayı
    letters = list()
    for m in permutations(iterable_symbols):  # Əlifbanın hərflərinə uyğun bütün mümkün variantları iterasiya edərək
        letters.append(m)  # letters listinə yazır
    # os.remove('alphabet.txt') if Path('alphabet.txt').exists() else os.system('touch alphabet.txt')
    Alphabed.objects.all().delete()
    f = Alphabed(title=_list)
    _letters = ""
    for i in range(int(number_of_conditions)):  # Hər hərflə başlayan sətrləri iterasiya edirəm | range(6) => 0..5
        for j, y in enumerate(letters):  # Hər iterasiyada ötürülmüş listi enumerate vasitəsilə indexləyərək iterasiya edirəm   exmple: j=0, y=("A", "B", "C", "D", "E" )
            if (i + j) % number_of_conditions == 0 or j % number_of_conditions == number_of_conditions:
                line = (j, y)
                _letters += str(line) + "\n"
    f.letters = _letters
    f.save()

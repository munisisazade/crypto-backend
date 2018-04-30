import math
import random


class Encoder:  # şifrələmək prosesini yerine yetirən class

    letters = list()

    def __init__(self, token, alphabet):  # classın constructoruna açar söz ötürürəm
        self.alphabet = list()  # class dəyişənlərini təyin edirəm
        self.token = token
        self.alpabet_interruption = False
        if alphabet:
            self.ALPHABET = alphabet.title
            content = alphabet.letters.replace("\n", ",")
            number_of_repeats = math.factorial(len(self.ALPHABET))
            number_of_iterables = len(self.ALPHABET)
            self.number_of_conditions = number_of_repeats / number_of_iterables
            for el in eval(content):
                self.alphabet.append(el)
        else:
            return

    def decode(self, encoded_text):  # şifrəni deşifrələmək üçün funksiya
        decoded_text = list()  # deşifrələnmiş simvollarin yığmaq üçün boş list yaradıram
        token_length = len(self.token)  # tokenin simvol sayı
        _lst_encoded = encoded_text.split("&")  # sifrənin içindəki
        text = _lst_encoded[0]  # şifrələnmiş sözü
        random_lines = _lst_encoded[1:]  # və random sətrləri ayırıram
        devided_alphabet = self.devide_alphabet()  # devide_alphabet() funksiyası vasitəsilə əlifbanı hər hərflə
        # başlaya sətrlərin sayı qədər hissəyə bölürəm
        for i, x in enumerate(text):  # şifrələnmiş sözü iterasiya edib
            if i <= token_length:  # açar sözün simvol sayı şifrənin simvol sayını aşmırsa
                token_index = i % token_length  # açar sözün cari indexi sifrənin cari indexinin açarsözün simvol
                # sayına bölünməsindən alınan qalığa bərabər olur
            else:  # açar sözün simvol sayı şifrənin simvol sayını aşırsa
                token_index = (i - 1) % token_length  # çar sözün cari indexi (i-1)%token_length düsturu ilə hesablanır
            if self.token[token_index] in self.ALPHABET:  # əgər açar sözün cari indexindəki simvol əlifbada varsa
                token_alphabet_index = self.ALPHABET.index(self.token[token_index])  # əgər açar sözün cari
                # indexindəki simvol əlifbada varsa onun indexini tapiram
                selected_lines = devided_alphabet[
                    token_alphabet_index]  # hissələrə bölünmüş əlifbadan yuxarıdakı indexdəki listi selected_lines
                # dəyişəninə təyin edirəm
                selected_line = selected_lines[int(random_lines[i])]  # açar sözə uyğun seçilmiş sətrlərdən(
                # selected_lines) şifrənin içindəki random str indexlərindən uyğun olanı seçib selected_line
                # dəyişninə mənimsədirəm
                index = selected_line[1].index(x)  # həmin sətrdə şifrələnmiş sözün uyğun simvolunun indexini tapıram
                decoded_text.append(self.ALPHABET[index])  # sonda həmin indexdəki əlifba simvolu deşifrələnmiş
                # simvol olur və onu deşifrələnmiş simvollarin yığmaq üçün boş listə əlavə edirəm
            else:  # əgər açar sözün cari indexindəki simvol əlifbada yoxdursa yəni əlifbadan kənara çıxılarsa
                return "Elifbadan kenara cixmayin"
        return "".join(decoded_text)  # hər şey qaydasında bitərsə şifrələnmiş simvolların
        #  yığıldığı list stringify edərək return edirəm

    def devide_alphabet(self):
        devided_list = list()
        temp_lst = list()
        for i, k in enumerate(self.alphabet):
            if i % self.number_of_conditions == 0 and i != 0:
                devided_list.append(temp_lst)
                temp_lst = [k]
            elif i == len(self.alphabet) - 1:
                temp_lst.append(k)
                devided_list.append(temp_lst)
            else:
                temp_lst.append(k)
        return devided_list

    def encode(self, text):
        encode_token = list()
        encoded_text = list()
        token_length = len(self.token)
        selected_lines = list()

        for i, x in enumerate(text):
            index = self.ALPHABET.index(x)  # sifrelenecek simvolun indexi
            if i <= token_length:  #
                token_index = i % token_length  # acar sozun cari indexi
            else:
                token_index = (i - 1) % token_length  # acar sozun cari indexi
            encode_symbol = self.token[token_index]  # acar sozun cari simvolu
            cycle = self.number_of_conditions - 1  # her herf ucun mumkun tekrarlanmalarin sayi

            if x not in self.ALPHABET or encode_symbol not in self.ALPHABET:
                print("Elifbadan kenara cixmayin!")
                self.alpabet_interruption = True
                return
            if encode_symbol in self.ALPHABET:
                k = self.ALPHABET.index(encode_symbol)  #
            x = int(k + cycle * k)  # acar sozun hansi indexler araliginda sifrelenecek
            y = int(k + cycle + cycle * k)  # acar sozun hansi indexler araliginda sifrelenecek
            for line_index in range(x, y + 1):
                selected_lines.append(self.alphabet[line_index])
            selected_line_index = random.choice(range(x, y + 1))  # hemin araligda random bir setrin index
            selected_line = self.alphabet[selected_line_index]  # hemin araligda random bir setr
            random_index = range(x, y + 1).index(selected_line_index)
            encode_token.append(random_index)  # acar soze uygun random secilmis setrin indexi liste elave olunur
            encoded_text.append(selected_line[1][index])  # acar soze uygun random secilmis setrde sifrelenecek soze
            # uygun simvol liste elave olunur
        return "".join(encoded_text) + "&" + '&'.join(str(x) for x in encode_token)

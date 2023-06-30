import os
import sys
import time

import save_list
from connect_ta import ConnectTA
from requirements import check_req

connectTa = ConnectTA()

if not check_req():
    print("Gerekli paketler kurulamadı")
    sys.exit()


def get_option():
    select = input("\nSeçiminiz: ")

    if select.isdigit():
        return int(select)
    else:
        print("Hatalı seçim")
        time.sleep(0.5)
        return -1


def save_type_menu(movies, tp):
    while True:
        os.system("cls")
        print(" Kayıt Türü ".center(50, "#"))
        print("")

        print("1 - Txt Olarak Kaydet")
        print("2 - Html Olarak Kaydet")

        print("\n0 - Ana Menüye Dön")

        save_opt = get_option()

        if save_opt == 1:
            save_list.save_txt(movies, tp)
            input()

        if save_opt == 2:
            save_list.save_html(movies, tp)
            input()

        if save_opt == 0:
            break


while True:

    os.system("cls")

    if not connectTa.login_is_ok:
        username = input("Kullanıcı Adı Girin: ")
        password = input("Parola Girin: ")
        connectTa.login(username, password)
    else:
        any_list_full = len(connectTa.movies_list) > 0 or len(connectTa.series_list) > 0
        movies_is_full = len(connectTa.movies_list) > 0
        series_is_full = len(connectTa.series_list) > 0

        print("".center(50, "#"))
        print(f" Hoşgeldiniz: {connectTa.username} ".center(50, "#"))
        print("".center(50, "#"))

        print("Ana Menü\n")

        if any_list_full:
            print(f"Listeye alınan {len(connectTa.movies_list)} film ve {len(connectTa.series_list)} dizi var.\n")
        print("1 - Film Listesini Al")
        print("2 - Dizi Listesini Al")

        if any_list_full:
            print("3 - Alınan Listeyi Görüntüle")
            print("4 - Alınan Listeyi Kaydet")

        print("\n0 - Programı Sonlandır")

        option = get_option()

        if option == 1:
            connectTa.reset_list(connectTa.MOVIES)
            connectTa.get_movies_list(1)

        if option == 2:
            connectTa.reset_list(connectTa.SERIES)
            connectTa.get_series_list(1)

        if option == 3 and any_list_full:

            while True:

                os.system("cls")
                print(" Görüntüleme Menüsü ".center(50, "#"))
                print("")

                if movies_is_full:
                    print("1 - Film Listesini Göster")
                if series_is_full:
                    print("2 - Dizi Listesini Göster")

                print("\n0 - Ana Menüye Dön")

                show_opt = get_option()

                if show_opt == 1 and movies_is_full:
                    for x in connectTa.movies_list:
                        print(x)
                    input()
                if show_opt == 2 and series_is_full:
                    for x in connectTa.series_list:
                        print(x)
                    input()
                if show_opt == 0:
                    break

        if option == 4 and any_list_full:

            while True:
                os.system("cls")
                print(" Kayıt Menüsü ".center(50, "#"))
                print("")

                if movies_is_full:
                    print("1 - Film Listesini Kaydet")
                if series_is_full:
                    print("2 - Dizi Listesini Kaydet")

                print("\n0 - Ana Menüye Dön")

                show_opt = get_option()

                if show_opt == 1 and movies_is_full:
                    save_type_menu(connectTa.movies_list, "Film")
                if show_opt == 2 and series_is_full:
                    save_type_menu(connectTa.series_list, "Dizi")
                if show_opt == 0:
                    break

        if option == 0:
            break

from getpass import getpass
from os import getcwd

from IG_followers_following import InstagramScraper



def write_to_txt(total_matches: set) -> None:
    with open(f'{getcwd()}\personas_non_grata.txt', 'w+') as file:
        for user in total_matches:
            file.write(f'{user}\n')


if __name__ == '__main__':
    user = input('Introduce tu usuario de IG: ').replace('@', '')
    pw = getpass('Introduce tu contraseña de IG: ')

    ig = InstagramScraper(username=user, password=pw)

    ig.login()
    ig.go_to_profile()

    print('Buscando coincidencias...')

    followers = ig.get_follow('followers')
    following = ig.get_follow('following')
    
    result = following - followers

    if result:
        print('Encontradas. Generando fichero de texto...')

        write_to_txt(result)

    else:
        print('Sin resultados')


    print('Cerrando navegador...')
    ig.close_nav()
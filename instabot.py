from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from random import randint
import pandas as pd



''' Configuracón '''

chromedriver_path = 'chromedriver.exe' # Pon aquí tu ruta al chromedriver (puede ser en la misma carpeta que este archivo)
webdriver = webdriver.Chrome(executable_path=chromedriver_path)
sleep(2)



webdriver.get('https://www.instagram.com')
sleep(3)

username = webdriver.find_element_by_name('username')
username.send_keys('xxxxx')
password = webdriver.find_element_by_name('password')
password.send_keys('yyyyyyyy*')



button_login = webdriver.find_element_by_css_selector('#loginForm > div > div:nth-child(3) > button')
button_login.click()
sleep(3)



notnow = webdriver.find_element_by_css_selector('#react-root > section > main > div > div > div > div > button')
notnow.click() # Comenta estas dos lineas si no te sale un pop up de notificaciones




''' Seleccionar Hashtag '''

hashtag_list = ['instatraveler']


''' Lineas para generar la lista de Seguidos '''

prev_user_list = [] # si es la primea vez que usas este script, usa esta linea y comenta las dos siguientes
# prev_user_list = pd.read_csv('list.csv', delimiter=',').iloc[:,1:2] # useful to build a user log
# prev_user_list = list(prev_user_list['0'])

new_followed = []
tag = -1
followed = 0
likes = 0
comments = 0



for hashtag in hashtag_list:
    tag += 1
    webdriver.get('https://www.instagram.com/explore/tags/'+ hashtag_list[tag] + '/')
    sleep(5)
    first_thumbnail = webdriver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')
    ''' Abriendo la primera foto '''
    first_thumbnail.click()
    sleep(randint(1,2))    
    try:        
        for x in range(1,100):
            username = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/span/a').text
            
            if username not in prev_user_list:
                # If we already follow, do not unfollow
                if webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').text == 'Seguir':
                    
                    ''' Seguir '''
                    webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()
                    
                    new_followed.append(username)
                    followed += 1

                    ''' Dar like a la foto '''
                    button_like = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[1]/button')
                    
                    button_like.click()
                    likes += 1
                    sleep(randint(18,25))

                    ''' Comentario Aleatorio '''
                    comm_prob = randint(1,10)
                    print('{}_{}: {}'.format(hashtag, x,comm_prob))
                    if comm_prob > 3:
                        comments += 1
                        webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[2]/button').click()
                        comment_box = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/section[3]/div/form/textarea')

                        if (comm_prob < 7):
                            comment_box.send_keys('Muy bueno! ❤️❤️')
                            sleep(1)
                        elif comm_prob <= 8:
                            comment_box.send_keys('Me encanta :) ❤️')
                            sleep(1)
                        elif comm_prob == 9:
                            comment_box.send_keys('Flipas!! ❤️')
                            sleep(1)
                        elif comm_prob == 10:
                            comment_box.send_keys('Buenísimo!!! ❤️ ❤️ ❤️:)')
                            sleep(1)
                        # Enter to post comment
                        comment_box.send_keys(Keys.ENTER)
                        sleep(randint(22,28))

                ''' Siguiente '''
                webdriver.find_element_by_link_text('Siguiente').click()
                sleep(randint(25,29))
            else:
                webdriver.find_element_by_link_text('Siguiente').click()
                sleep(randint(20,26))
    
    except:
        continue

for n in range(0,len(new_followed)):
    prev_user_list.append(new_followed[n])
    
updated_user_df = pd.DataFrame(prev_user_list)
updated_user_df.to_csv('{}_users_followed_list.csv'.format(strftime("%Y%m%d-%H%M%S")))
print('{} likes a fotos.'.format(likes))
print('{} fotos comentadas.'.format(comments))
print('{} personas seguidas.'.format(followed))

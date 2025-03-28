from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
#Importem modul per als selects
from selenium.webdriver.support.ui import Select

class MySeleniumTests(StaticLiveServerTestCase):
    # carregar una BD de test
    #fixtures = ['testdb.json',]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)
        # creem superusuari
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()

    @classmethod
    def tearDownClass(cls):
        # tanquem browser
        # comentar la propera línia si volem veure el resultat de l'execució al navegador
        #cls.selenium.quit()
        super().tearDownClass()

    def test_crear_grup(self):
        # anem directament a la pàgina d'accés a l'admin panel
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))

        # comprovem que el títol de la pàgina és el que esperem
        self.assertEqual( self.selenium.title , "Log in | Django site admin" )

        # introduïm dades de login i cliquem el botó "Log in" per entrar
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('isard')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()

        # testejem que hem entrat a l'admin panel comprovant el títol de la pàgina
        self.assertEqual( self.selenium.title , "Site administration | Django site admin" )

	#Busquem el boto que porta a crear grup
        self.selenium.find_element(By.XPATH, '//a[@href="/admin/auth/group/add/"]').click()

	# testejem que hem entrat a la pàgina de grups amb  el títol de la pàgina
        self.assertEqual( self.selenium.title , "Add group | Django site admin" )

	# Busquem el camp de text del nom del grup i omplim el nom
        entrada_grup = self.selenium.find_element(By.NAME,"name")
        entrada_grup.send_keys('grup_eac')

	#Busquem el boto que assigna tots els permisos
        self.selenium.find_element(By.ID,'id_permissions_add_all_link').click()

        #Busquem el boto que guarda l'usuari
        self.selenium.find_element(By.NAME,'_save').click()

        # Assegurem que estem a la pagina de grups
        self.assertEqual( self.selenium.title , "Select group to change | Django site admin" )

        #Comprovem si existeix el element th de classe fiel.__st__ i que conte el text grup_eac
        grup = self.selenium.find_element(By.XPATH, '//th[@class="field-__str__"]/a[text()="grup_eac"]')
        grup.click()

        #Mirem si realment ha entrat al grup grup_eac mirant si existeix el titol h2 amb el text grup_eac
        self.selenium.find_element(By.XPATH, '//h2[text()="grup_eac"]')
        #Final creacio grup

        #Podem crear un usuari pero usarem l'usuari isard, bper anar als usuaris i fem clic
        self.selenium.find_element(By.XPATH, '//a[@href="/admin/auth/user/"]').click()

        #Comprovem si existeix el element th de classe fiel.__st__ i que conte el text grup_eac
        usuari = self.selenium.find_element(By.XPATH, '//th[@class="field-username"]/a[text()="isard"]')
        usuari.click()

        #Busquem el grup a l'element select
        grup_seleccionat = self.selenium.find_element(By.XPATH, '//select[@id="id_groups_from"]/option[@title="grup_eac"]')

        #Fem clic al grup
        grup_seleccionat.click()

        #Busquem el boto que assigna els permisos
        self.selenium.find_element(By.ID,'id_groups_add_link').click()

        #Busquem el boto save per guardar el grup
        guardar = self.selenium.find_element(By.XPATH, '//div[@class="submit-row"]/input[@value="Save"]')
        guardar.click()

        #Busquem a la llista del lateral dret el text grup_eac per filtrar els usuaris per grup
        filtre_grup = self.selenium.find_element(By.XPATH, '//ul/li/a[text()="grup_eac"]')
        filtre_grup.click()

        #Assegurem que el filtre esta seleccionat
        filtre_seleccionat = len(self.selenium.find_elements(By.XPATH, '//ul/li[@class="selected"]/a[text()="grup_eac"]')) > 0
        print("Grup_eac seleccionat = " + str(filtre_seleccionat))

        #Comprovem amb el filtre seleccionat si apareix el grup isard
        isard_pertany = len(self.selenium.find_elements(By.XPATH, '//th[@class="field-username"]/a[text()="isard"]')) > 0
        print("Apareix isard? " + str(isard_pertany))


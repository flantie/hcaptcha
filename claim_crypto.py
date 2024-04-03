    def claim_crypto(self):
        self.handle_modal()
        self.accept_cookies()
        
        data = {"method": "hcaptcha", "pageurl": "https://bnbfree.in", "sitekey": "2ca356f0-8121-44d8-9596-6aeb24529e95"}
        g_response = api.run(data)
        
        if g_response != 0:
            print("g_response: "+g_response[:40])
        else:
            print("task finished with error !!!")
        
        try:
            # Trouver le conteneur du captcha
            captcha_container = self.wait_for_element(By.CSS_SELECTOR, "#free_play_recaptcha > form > div", clickable=False)
            print("h-captcha trouvé")

            # Trouver l'iframe du captcha et basculer vers celui-ci
            iframe = captcha_container.find_element(By.TAG_NAME, "iframe")
            self.browser.switch_to.frame(iframe)
            
            # Attendre et cliquer sur la case à cocher du captcha
            try:
                checkbox_button = WebDriverWait(self.browser, 10).until(
                    EC.element_to_be_clickable((By.ID, "checkbox"))
                )
                checkbox_button.click()
            except TimeoutException:
                print("Case à cocher h-captcha non disponible.")

            # Revenir au contexte parent pour modifier l'attribut de l'iframe
            self.browser.switch_to.default_content()
            self.browser.execute_script("arguments[0].setAttribute('data-hcaptcha-response', arguments[1]);", iframe, g_response)
            print("L'attribut data-hcaptcha-response de l'iframe modifié")
            
            # Re-basculer vers l'iframe pour interagir avec d'autres éléments
            self.browser.switch_to.frame(iframe)

            # Attendre que le textarea soit chargé et accessible
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='h-captcha-response']"))
            )

            # Modifier le style du textarea pour le rendre visible, insérer la réponse, puis le masquer à nouveau
            self.browser.execute_script('document.querySelector("textarea[name=\'h-captcha-response\']").style.display = "";')
            self.browser.execute_script("""arguments[0].value = arguments[1]""", 
                                        self.browser.find_element(By.CSS_SELECTOR, "textarea[name='h-captcha-response']"), 
                                        g_response)
            self.browser.execute_script('document.querySelector("textarea[name=\'h-captcha-response\']").style.display = "none";')

            free_play_form_button = self.wait_for_element(By.ID, "free_play_form_button", clickable=True)
            free_play_form_button.click()
            print("Réclamation standard effectuée.")
            time.sleep(20)  # Attendre un moment pour que l'action soit traitée
        except TimeoutException:
            print("Le contenu hCaptcha n'est pas disponible.")

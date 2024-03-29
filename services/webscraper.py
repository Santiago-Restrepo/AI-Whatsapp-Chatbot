from playwright.sync_api import sync_playwright, Page, Browser
import requests
import json


class Scraper:
    def __init__(self):
        self.base_url = "https://www.personeriamedellin.gov.co"

    def run(self):
        extracted_data = self.extract()

        with open('data/data.json', 'w') as f:
            json.dump(extracted_data, f)

        # transform()
        # load()

    def extract(self):
        with sync_playwright() as playwright:
            chromium = playwright.chromium  # or "firefox" or "webkit".
            browser = chromium.launch()
            page = browser.new_page()

            business_information = self.get_business_information(page)
            business_history = self.get_business_history(page)
            business_ethics = self.get_business_ethics(page)
            business_objectives = self.get_business_objectives(page)
            business_services = self.get_business_services(browser)
            business_fqa = self.get_business_fqa(page)

            browser.close()

        return {
            'business_information': business_information,
            'business_history': business_history,
            'business_ethics': business_ethics,
            'business_objectives': business_objectives,
            'business_services': business_services,
            'business_fqa': business_fqa
        }

    def get_business_information(self, page: Page):
        path = '/nuestra-historia-anterior/mision-vision-valores/'
        page.goto(self.base_url + path)
        elements = page.query_selector_all('.infobox-content p')
        mission_element = elements[0]
        vision_element = elements[1]
        mission = mission_element.inner_text()
        vision = vision_element.inner_text()
        elements = page.query_selector_all('.infobox-content')
        elements = elements[2:]
        values = []
        for element in elements:
            title = element.query_selector('.title').inner_text()
            description_elements = element.query_selector_all('p')
            description = ''
            for description_element in description_elements:
                description += description_element.inner_text()
            values.append({
                'title': title,
                'description': description
            })

        return {
            'mision': mission,
            'vision': vision,
            'values': values
        }

    def get_business_history(self, page: Page):
        path = '/nuestra-historia/'
        page.goto(self.base_url + path)
        elements = page.query_selector_all('.twae-content')
        scraped_data = []
        for element in elements:
            date = element.query_selector('.twae-title').inner_text()
            description = element.query_selector(
                '.twae-description').inner_text()
            scraped_data.append({
                'date': date,
                'description': description
            })
        return scraped_data

    def get_business_ethics(self, page: Page):
        path = '/nuestra-historia-anterior/ideario-etico/'
        page.goto(self.base_url + path)
        elements = page.query_selector_all('.elementor-price-table')
        scraped_data = [
        ]
        for element in elements:
            topic = element.query_selector(
                '.elementor-price-table__header').inner_text()
            items = element.query_selector_all(
                '.elementor-price-table__features-list li')
            items = [item.inner_text() for item in items]
            scraped_data.append({
                'topic': topic,
                'items': items
            })
        return scraped_data

    def get_business_objectives(self, page: Page):
        pass

    def get_business_services(self, browser: Browser):
        # page = browser.new_page()
        url = 'https://personeriaenlinea.personeriamedellin.gov.co/Servicio/GetServicio/'
        paths = [
            'Tutela',
            'ImpugnacionTutela',
            'DerechoPeticion',
            'Asesoria',
            'IncidenteDesacato',
            'IncidenteDesacato',
            'ReclamacionDerechosConsumidor',
            'ReposicionVictimasConflictoArmado',
            'PQRSRD'
        ]

        services = []

        for path in [paths[0]]:
            response = requests.get(url + path)
            response_json = response.json()
            name = response_json['data']['nombre']
            description = response_json['data']['descripcion']
            response_time = response_json['data']['tiempoMaximoSolucion']

            services.append({
                'name': name,
                'description': description,
                'response_time': response_time
            })
        return services

    def get_business_fqa(self, page: Page):
        path = '/preguntas-frecuentes/'
        page.goto(self.base_url + path)
        containers = page.query_selector_all(
            '.eael-accordion-list')
        faqs = []

        for container in containers:
            question_container = container.query_selector(
                '.elementor-tab-title')
            question = question_container.inner_text()
            response_container = container.query_selector(
                '.eael-accordion-content')
            response = response_container.inner_text()

            faqs.append({
                'question': question,
                'response': response
            })

        return faqs

    def transform():
        pass

    def load():
        pass


if __name__ == '__main__':
    scraper = Scraper()

    scraper.run()

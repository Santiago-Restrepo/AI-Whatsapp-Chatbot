from playwright.sync_api import sync_playwright, Page, Browser
from bs4 import BeautifulSoup
import requests
import json


class Scraper:
    def __init__(self):
        self.base_url = "https://www.personeriamedellin.gov.co"

    def run(self):

        extracted_data = self.extract()

        transformed_data = self.transform(extracted_data)

        self.load(transformed_data)

    def extract(self):
        with sync_playwright() as playwright:
            chromium = playwright.chromium  # or "firefox" or "webkit".
            browser = chromium.launch()
            page = browser.new_page()

            business_information = self.get_business_information(page)
            business_history = self.get_business_history(page)
            business_ethics = self.get_business_ethics(page)
            business_services = self.get_business_services()
            business_fqa = self.get_business_fqa(page)

            browser.close()

        return {
            'business_information': business_information,
            'business_history': business_history,
            'business_ethics': business_ethics,
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

    def get_business_services(self):
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

        for path in paths:
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

    def transform_business_information(self, business_information):
        prompts = []
        mission_prompt = {
            'prompt': '¿Cuál es la misión de la Personería de Medellín?',
            'response': business_information['mision']
        }
        vision_prompt = {
            'prompt': '¿Cuál es la visión de la Personería de Medellín?',
            'response': business_information['vision']
        }
        values_response = [
            value['title']
            for value in business_information['values']
        ]
        values_prompt = {
            'prompt': '¿Cuales son los valores de la Personería de Medellín?',
            'response': ', '.join(values_response)
        }
        prompts.append(mission_prompt)
        prompts.append(vision_prompt)
        prompts.append(values_prompt)
        for value in business_information['values']:
            prompt = {
                'prompt': '¿Cómo gestiona la Personería de Medellín su valor de {}?'.format(value['title']),
                'response': value['description']
            }
            prompts.append(prompt)
        return prompts

    def transform_business_history(self, business_history):
        prompts = []
        prompt = {
            'prompt': '¿Cual es la historia de la Personería de Medellín?',
            'response': '\n'.join(['En {}, {}'.format(item['date'], item['description']) for item in business_history])
        }
        prompts.append(prompt)
        prompt = {
            'prompt': 'Cuáles fueron las épocas de la historia de la Personería de Medellín?',
            'response': '\n'.join([item['date'] for item in business_history])
        }
        prompts.append(prompt)
        prompt = {
            'prompt': '¿Cual es la evolución de la Personería de Medellín?',
            'response': '\n'.join(['En {}, {}'.format(item['date'], item['description']) for item in business_history])
        }
        prompts.append(prompt)
        for item in business_history:
            prompt = {
                'prompt': '¿Qué sucedió en {}, en el contexto de la Personería de Medellín?'.format(item['date']),
                'response': item['description']
            }
            prompts.append(prompt)
        return prompts

    def transform_business_ethics(self, business_ethics):
        prompts = []
        questions = [
            '¿Cuál es el código ético de la personería de medellín {}',
            '¿Cómo se comporta la Personería de Medellín {}',
            '¿Cuál es el código de ética de la Personería de Medellín {}',]
        for question in questions:
            for item in business_ethics:
                prompt = {
                    'prompt': question.format(item['topic']),
                    'response': '\n'.join(item['items']).strip()
                }
                prompts.append(prompt)
        return prompts

    def transform_business_services(self, business_services):
        prompts = []
        questions = [
            '¿Cual es el tiempo de respuesta para solicitar {}?',
            '¿Cuánto se demoran en responder a la solicitud {}?',
        ]
        for service in business_services:
            name = service['name']
            for question in questions:
                prompt = {
                    'prompt': question.format(name),
                    'response': service['response_time']
                }
                prompts.append(prompt)

        questions = [
            '¿Qué servicios ofrece la Personería de Medellín?',
            '¿Cuáles son los servicios que ofrece la Personería de Medellín?',
            'Servicios'
        ]
        for question in questions:
            prompt = {
                'prompt': question,
                'response': ','.join([item['name'] for item in business_services])
            }
            prompts.append(prompt)
        questions = [
            '¿Cómo gestiona la Personería de Medellín el servicio de {}?',
            '¿Quiero saber más sobre el servicio de {}?'
        ]
        for service in business_services:
            name = service['name']
            html_description = service['description']
            soup = BeautifulSoup(html_description, 'html.parser')
            description = soup.get_text()
            for question in questions:
                prompt = {
                    'prompt': question.format(name),
                    'response': description
                }
                prompts.append(prompt)

        return prompts

    def transform_business_fqa(self, business_fqa):
        prompts = [
            {
                'prompt': item['question'],
                'response': item['response']
            }
            for item in business_fqa
        ]
        return prompts

    def transform(self, scraped_data):
        transformed_business_data = self.transform_business_information(
            scraped_data['business_information'])
        transformed_business_history = self.transform_business_history(
            scraped_data['business_history'])

        transformed_business_ethics = self.transform_business_ethics(
            scraped_data['business_ethics'])

        transformed_business_services = self.transform_business_services(
            scraped_data['business_services'])

        transformed_business_fqa = self.transform_business_fqa(
            scraped_data['business_fqa'])

        prompts = transformed_business_data + transformed_business_history + \
            transformed_business_ethics + transformed_business_services + transformed_business_fqa

        return prompts

    def load(self, transformed_data):
        with open('data/transformed.json', 'w') as f:
            json.dump(transformed_data, f)


if __name__ == '__main__':
    scraper = Scraper()

    scraper.run()

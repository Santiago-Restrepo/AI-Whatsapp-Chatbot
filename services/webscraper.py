from playwright.sync_api import sync_playwright, Page


class Scraper:
    def __init__(self):
        self.base_url = "https://www.personeriamedellin.gov.co"

    def run(self):
        self.extract()
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
            # business_objectives = self.get_business_objectives(page)
            business_services = self.get_business_services()
            business_fqa = self.get_business_fqa()

            browser.close()

        return business_information, business_history, business_ethics, business_objectives, business_services, business_fqa

    def get_business_information(self, page: Page):
        path = '/nuestra-historia-anterior/mision-vision-valores/'
        page.goto(self.base_url + path)
        elements = page.query_selector_all('.infobox-content p')
        scraped_data = [
            element.inner_text()
            for element in elements
        ]
        return scraped_data

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

    def get_business_objectives(self):
        pass

    def get_business_services(self):
        pass

    def get_business_fqa(self):
        pass

    def transform():
        pass

    def load():
        pass


if __name__ == '__main__':
    scraper = Scraper()

    scraper.run()

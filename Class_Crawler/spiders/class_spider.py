import scrapy
from scrapy import Selector


class ClassSpider(scrapy.Spider):
    name = "classes"
    # will allow selection of start URL from cmd line later
    start_urls = ['https://fas.calendar.utoronto.ca/section/Computer-Science']

    custom_settings = {'AUTOTHROTTLE_ENABLED': True}

    def parse(self, response):
        for title, description in zip(
                response.xpath(
                    '//div[contains(concat(" ",normalize-space(@class)," "),"view-id-courses")]//h3/text()'
                ).getall(),
                response.xpath(
                    '//div[contains(concat(" ",normalize-space(@class)," "),"view-id-courses")]/div/div[descendant::span]'
                ).getall()):
            title = title.strip()
            description_sel = Selector(text=description)

            exclusion_hrefs = description_sel.xpath(
                '//span[contains(concat(" ", normalize-space(@class), " "), "views-field-field-exclusion1")]//a/@href'
            ).getall()
            exclusion_courses = description_sel.xpath(
                '//span[contains(concat(" ", normalize-space(@class), " "), "views-field-field-exclusion1")]//a/text()'
            ).getall()
            exclusion_courses = "None" if not exclusion_courses else exclusion_courses

            prerequisite_hrefs = description_sel.xpath(
                '//span[contains(concat(" ", normalize-space(@class), " "), "views-field-field-prerequisite1")]//a/@href'
            ).getall()
            prerequisite_courses = description_sel.xpath(
                '//span[contains(concat(" ", normalize-space(@class), " "), "views-field-field-prerequisite1")]//a/text()'
            ).getall()
            prerequisite_courses = "None" if not prerequisite_courses else prerequisite_courses

            corequisite_hrefs = description_sel.xpath(
                '//span[contains(concat(" ", normalize-space(@class), " "), "views-field-field-corequisite1")]//a/@href'
            ).getall()
            corequisite_courses = description_sel.xpath(
                '//span[contains(concat(" ", normalize-space(@class), " "), "views-field-field-corequisite1")]//a/text()'
            ).getall()
            corequisite_courses = "None" if not corequisite_courses else corequisite_courses
            yield {
                'title': title,
                'exclusions': exclusion_courses,
                'prerequisite': prerequisite_courses,
                'corequisite': corequisite_courses
            }

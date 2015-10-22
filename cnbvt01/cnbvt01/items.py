# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#Emisora,Clasificación CNBV,Familia,Categoría Yahoo!Finanzas,Categoría Morningstar,Fecha Inicio,Benchmark Fondos,Benchmark Morningstar,Morningstar.com.mx,Yahoo! Finanzas
class Cnbvt01Item(scrapy.Item):
    # define the fields for your item here:
    a_emisora = scrapy.Field()
    b_clas_cnbv = scrapy.Field()
    c_familia = scrapy.Field()
    d_adquiriente = scrapy.Field()
    e_cat_cnbv = scrapy.Field()
    f_cat_fondos = scrapy.Field()
    g_fecha_inicio = scrapy.Field()
    h_benchmark_fondos = scrapy.Field()
    i_benchmark_morningstar = scrapy.Field()
    j_link_cnbv = scrapy.Field()
    k_link_morningstar = scrapy.Field()
    l_link_yahoofinanzas1 = scrapy.Field()
    m_link_yahoofinanzas2 = scrapy.Field()

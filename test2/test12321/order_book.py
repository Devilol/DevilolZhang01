# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
本文档的作用：提供币对类 运行本文件将更新文件中的币对列表
如何使用：
    >> python currency_pairs.py
"""
import requests
import os
import pickle


class CurrencyPairs(object):
    def __init__(self):
        self.currency_pair_list_path = os.path.dirname(__file__) + '/' + 'currency_pair_list.pkl'
        self.mapping_dict_file_path = os.path.dirname(__file__) + '/' + 'currency_pair_mapping_dict.pkl'
        self.symbolUrl = 'https://api.huobi.pro/market/symbols'
        self.currency_pair_list = None
        self.currency_pair_mapping_dict = None
        self.valid_base_currency = ['usdt', 'btc', 'eth', 'ht']
        # 如果本地数据不存在，则网上获取
        if not os.path.exists(self.currency_pair_list_path) or not os.path.exists(self.mapping_dict_file_path):
            self.update()
        with open(self.currency_pair_list_path, 'rb') as f:
            self.currency_pair_list = pickle.load(f)
        with open(self.mapping_dict_file_path, 'rb') as f:
            self.currency_pair_mapping_dict = pickle.load(f)

    def get_currency_pair_list(self):
        return self.currency_pair_list

    def get_currency_pair_mapping_dict(self):
        return self.currency_pair_mapping_dict

    def update(self):
        """
        获取币对列表并序列化到本地
        :return: None
        """
        symbolsResponse = requests.get(self.symbolUrl)
        if symbolsResponse.status_code is not 200:
            raise RuntimeError('error in request currency_pair_list!', symbolsResponse.status_code, symbolsResponse.reason)
        json_response = symbolsResponse.json()
        currency_pair_list = [x for x in json_response['data'].keys()]
        currency_pair_mapping_dict = {}
        for currency_pair in json_response['data'].keys():
            for base_currency in self.valid_base_currency:
                index = currency_pair.find(base_currency);
                if  index > 0:
                    currency_pair_mapping_dict.update({currency_pair : (currency_pair[0:index], currency_pair[index:len(currency_pair)])})
                    break
        with open(self.currency_pair_list_path, 'wb') as f:
            pickle.dump(currency_pair_list, f)
        with open(self.mapping_dict_file_path, 'wb') as f:
            pickle.dump(currency_pair_mapping_dict, f)


if __name__ == '__main__':
    c = CurrencyPairs()
    c.update()
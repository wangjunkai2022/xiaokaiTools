#!/bin/sh
cookies="sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkchannel=%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D; user_locale=zh-CN; oschina_new_user=false; Hm_lvt_24f17767262929947cc3631f99bfd274=1687419771,1687423647,1687424597; user_return_to_0=%2F; tz=Asia%2FSaigon; gitee_user=true; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2213072600%22%2C%22first_id%22%3A%22188e2498cc3b86-05ef44563f11c4c-1b525634-2007040-188e2498cc414fd%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTg4ZTIwZTRjZDZhYTItMDZkOWVmMDBlOWJjNmY4LTFiNTI1NjM0LTIwMDcwNDAtMTg4ZTIwZTRjZDcxMWZjIiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMTMwNzI2MDAifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%2213072600%22%7D%2C%22%24device_id%22%3A%22188e20e4cd6aa2-06d9ef00e9bc6f8-1b525634-2007040-188e20e4cd711fc%22%7D; csrf_token=AxMVOEQ5m3u5EwQAm6bbMIS5kfFc3eBxGpG8mtHkoAgCyqDePcBZ1BxOAJJiBQoO1r0paoUylWzWIURGex67mQ%3D%3D; Hm_lpvt_24f17767262929947cc3631f99bfd274=1687425155; remote_way=http; gitee-session-n=NGZsMmVQcUhtZFpWNkZjTDNlMTlRNURIY2ZjUXFLK3RzbFNHRWVLTExRdXhpU2YyemExeDJxbVFpdWhEblBkcTNWaWFXbW1zUmFrOEdxeWdPdGYrUFV1aEFzSmFzc0I0Y240eFAyS1RZcCtqR2RZdzlubUl0SzE3RHdlbmZsQnVpQk4rd2JDMlBVRzlCTE42L29ybEIweWR6MmRRZ21TMHZVeENaVVRsTys4T2xBNFZyMDJYUURxaWZKRzhNNFVwK2w2aGFsM0h5Q1hnS2tEQWFKUy8wL0Y5cGprOVdyaHdERHNNOVdLYTB1WVVqeGY2QXVvemtGeUFycEFNTmRaQWFNSUEyTVpmc1ZuMHV5TnhkMGpRb3JMb1lLUVFhUnp6eTJTS0I4UXVzRVdEeW9xdTFlUitsZHA0cFAxQnR4K2hvVUFwYjRMWHRHQlo3QldOZ2c2Ymg3M3E0d3FINnZSdXNTU1pNOFd3RGZ4RDFxdGdwNStMTXZLdEh1aHBJUTUreVd6WC9hSEF2Ymt3VG1Tbzh4bWxFOGw2Uis2UFpFV2R2VmtkL3BzMTRoeE1MQmtaZ0gxbXJPNzRra3RVc1lvbS9TT0xaWnNYTU5ySHZmNzcvL0tQMXhwV295STJxWmRYdi9lc1NoRk96ZW9XYXM4VlRQWVhXWWdaSkhsN1BnTWVZekZlN2dWaWxkRlJjZGVzaW9qaHFsWnVudEQ5VFFNblRmcHVYSHJTK1BrU29wYTRWSW1xaEJKb3V2b09lcEVQWUF2a2lOTmYvUXRsNm9DNHNUNmhmcm9MWldxbThFSlVYazZQM0huUEhHUU5uclJYK3l5TFFmbGVDemJHSUJYeS0tMGtBeTJQdWhpaUdlL0FWSjBNSTBodz09--bf7a91b19dfad0e796d14539ed1373d95a8ae60d"
curl -O -b "$cookies" https://gitee.com/kaikai2024/test/raw/master/config.json
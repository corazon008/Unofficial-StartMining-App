import requests
import threading
from datetime import timedelta, date

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from data import pools_name, Datas


class StartMiningScreen(Screen):
    Builder.load_file('startminingscreen.kv')
    decimal = 9

    def on_enter(self, *args):
        self.refresh()

    def refresh(self):
        Datas.refresh()
        thread1 = threading.Thread(target=self.live_reward, name="thread_live_reward")
        thread2 = threading.Thread(target=self.total_payout, name="thread_total_payout")
        thread3 = threading.Thread(target=self.get_earnings, name="thread_get_earnings")
        thread4 = threading.Thread(target=self.next_payout, name="thread_next_payout")

        thread1.start()
        thread2.start()
        thread3.start()

        Datas.home_threads = [thread1, thread2, thread3]

        thread4.start()

    def live_reward(self):
        reward = "0"
        try:
            response = requests.get(f"https://cruxpool.com/api/btc/miner/{Datas.btc_wallet}/balance")
            satoshi = response.json()["data"]["balance"]
            reward = str(int(float(satoshi)) / 10 ** 8)
        except Exception as e:
            print("An error occured in live_reward : ", e)
        self.ids.live_rewards.text = reward[:self.decimal]

    def get_earnings(self):
        btc = [0] * len(pools_name)
        try:
            for thread in Datas.data_threads:
                thread.join()

            for i, pool_name in enumerate(pools_name):
                r = requests.get(f"https://cruxpool.com/api/btc/miner/{Datas.addresses[pool_name]}")
                perMin = r.json()["data"]["coinPerMins"]
                perDay = perMin * 60 * 24

                btc[i] = perDay / int(Datas.all_stakers[pool_name]) * int(Datas.my_stake[pool_name])

        except Exception as e:
            print("An error occured in get_earnings : ", e)
        self.ids.earnings.text = str(sum(btc))[:self.decimal]

    def total_payout(self):
        total = [0]
        try:
            response = requests.get(f"https://cruxpool.com/api/btc/miner/{Datas.btc_wallet}/payments")
            payments = response.json()["data"]["payments"]
            total = [payment["amount"] / 10 ** 8 for payment in payments]
        except Exception as e:
            print("An error occured in total_payout : ", e)

        self.ids.totalpayout.text = str(sum(total))[:self.decimal]

    def next_payout(self):
        for thread in Datas.home_threads:
            thread.join()
        payout_day = "None"
        try:
            earnings = float(self.ids.earnings.text)
            rewards = float(self.ids.live_rewards.text)
            payout = 0.005
            days2wait = (payout - rewards) // earnings

            payout_day = date.today() + timedelta(days=days2wait)
            payout_day = payout_day.strftime("%d/%m/%y")
        except Exception as e:
            print("An error occured in next_payout : ", e)
        self.ids.next_payout.text = str(payout_day)
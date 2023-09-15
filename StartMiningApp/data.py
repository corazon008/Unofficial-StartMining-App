import pickle
import requests
import threading

pools_name = ["origin", "genesis", "north_pool"]


def nb_all_stake(pool_id):
    r = requests.get(
        "https://api.etherscan.io/api?module=proxy&action=eth_call&to=0xb4a3c079acbd57668bf5292c13878f9225678381&data=0x03501951000000000000000000000000000000000000000000000000000000000000000{}&tag=latest&apikey=ZS4NECH7KXSBFJCUTPAKBWXWSH1PSPVX72".format(
            pool_id))
    data = r.json()["result"]
    data = data[2:]
    start = [data[i:i + 64] for i in range(0, len(data), 64)]
    start_num = [int(e, 16) for e in start]
    nb = len(start_num)
    return nb - 2


def nb_my_stake(pool_id, wallet):
    r = requests.get(
        "https://api.etherscan.io/api?module=proxy&action=eth_call&to=0xb4a3c079acbd57668bf5292c13878f9225678381&data=0xbfafa378000000000000000000000000000000000000000000000000000000000000000{}000000000000000000000000{}&tag=latest&apikey=ZS4NECH7KXSBFJCUTPAKBWXWSH1PSPVX72".format(
            pool_id, wallet[2:]))
    data = r.json()["result"]
    data = data[2:]
    start = [data[i:i + 64] for i in range(0, len(data), 64)]
    nb = len([int(e, 16) for e in start])
    return nb - 2


class Datas:
    file_name = "datas.pkl"
    btc_wallet = ""
    eth_wallet = ""
    my_stake = {"origin": 0, "genesis": 0, "north_pool": 0}
    all_stakers = {"origin": 0, "genesis": 0, "north_pool": 0}
    addresses = {
        "origin": "bc1qdzcgvennnjzv4jry38s0krjtl3x9n374302c75",
        "genesis": "bc1p94llwnug0zv9zvk8lj9g43s6ul5nssf9yl5pn8sdlyqj3rdy90qq34ck00",
        "north_pool": "bc1qyjp7kadrtr8j7gvvs9jej9c790jpmal4cwehle",
    }

    data_threads = []
    home_threads = []

    @classmethod
    def refresh(cls):
        cls.data_threads = []
        cls.home_threads = []
        thread1 = threading.Thread(target=cls.staker_per_pool)
        thread2 = threading.Thread(target=cls.my_stake_per_pool)
        thread1.start()
        thread2.start()
        cls.data_threads = [thread1, thread1]

    @classmethod
    def store_data(cls):
        data_to_store = {
            'btc_wallet': cls.btc_wallet,
            'my_stake': cls.my_stake,
        }
        with open(cls.file_name, 'wb') as file:
            pickle.dump(data_to_store, file)

    @classmethod
    def load_data(cls):
        with open(cls.file_name, 'rb') as file:
            data = pickle.load(file)
        cls.btc_wallet = data['btc_wallet']
        cls.my_stake = data['my_stake']

    @classmethod
    def staker_per_pool(cls):
        for i, name in enumerate(cls.all_stakers.keys()):
            cls.all_stakers[name] = nb_all_stake(i + 1)

    @classmethod
    def my_stake_per_pool(cls):
        for i, name in enumerate(cls.my_stake.keys()):
            cls.my_stake[name] = nb_my_stake(i + 1, cls.eth_wallet)
